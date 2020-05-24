from network.udp import *
from network.tcp import * 
from control.process.image import *
from PIL import Image
import matplotlib.pyplot as plt
from control.ai.audio_model import *
from control.process.mfcc import *
from control.sensor.mic import Recorder
import numpy as np
import cv2
import time
import os


#画像処理初期化
fps, img_n = 0, 0
img_dir = "./img"
tcp = TCP("192.168.0.71", 8889, server_flag=True)
height, width, channel = int(480/8), int(640/8), 3
target_height, target_bottom = int(height/3), height-10
indexs_flat, indexs_dim = target_indexs(height, width, target_height=target_height)
if not os.path.exists(img_dir): os.mkdir(img_dir)


#インスタンス生成(レコード, モデル[決定木], UDP)
record = Recorder()
model = Model()
model.model_select("K-NN")

#音声認識[前と言ったら動きだす]
result = 1
print("start recoding")
while result:

	#レコードとMFCC
	outfile = record.record_voice(["a.wav"], overwrite=True)
	mfcc = MFCC("./control/audioSample/a.wav")
	features = mfcc.get_mfcc().reshape(1, -1)
	
	#音声認識
	result = model.predict(features)
	print(result)

#画像処理[ライントレース]
while True:
	
	#TCP画像受信
	start = time.time()
	receivedstr=tcp.receive(1024*4) 
	narray = np.fromstring(receivedstr,dtype='uint8')  
	raw_img = cv2.imdecode(narray,1).reshape((height, width, channel))
	
	#ライン検出
	grayFrame = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
	b_img = mean_binarize(grayFrame, indexs=indexs_flat)
	l_img = labeling(b_img, indexs=indexs_dim)
	r_img = compare_area(l_img)
	
	#画像から回転角度算出
	degree, top_feature_point, bottom_feature_point, tip, rear = image_line_degree(r_img)
	tcp.send(degree.to_bytes(4, 'big', signed=True))
	
	#検出したラインを緑表示
	img = raw_img.copy()
	img = img.reshape(width*height, channel)
	img[np.where(r_img.reshape(-1) == 1)] = [0, 255, 0]
	img = img.reshape(height, width, channel)
	
	#画像上に検出したライン角度と画像を表示
	img = cv2.resize(img, (width*2, height*2))
	img = cv2.putText(img, '%d'%(degree), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
	
	#画像表示
	cv2.imshow("",img)
	cv2.waitKey(1)
	
	#画像保存
	img_n += 1
	pil_img = Image.fromarray(cv2.cvtColor(cv2.resize(raw_img, (32, 32)), cv2.COLOR_BGR2RGB))
	pil_img.save('%s/img%d_%d.jpg'%(img_dir, img_n, degree))
	
	#FPS算出
	fps += 1/(time.time()-start)
	print(fps/img_n)

cv2.destroyAllWindows()
