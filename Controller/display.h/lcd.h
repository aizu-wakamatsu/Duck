/*
 * lcd.h
 * shinchokuer: tari
 * 
 */

#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7735.h>

#define TFT_CS         5
#define TFT_RST        4
#define TFT_DC         2


void init_lcd(){
    
}

/*
* disp_nw
* call after initiarize Wi-Fi!!
*/

void disp_nw() {
  tft.setCursor(0, 10);
  tft.setTextSize(1);
  tft.print("SSID: ");
  tft.print(ssid_wifis);
}

void disp_direc(int direc) {
   tft.setCursor(0, 10);
   tft.setTextSize(4);
  switch (direc) {
    case 1:
      tft.println(" |");
      tft.println(" O ");
      tft.println("");
      break;
    case 2:
      tft.println("\\");
      tft.println(" O ");
      tft.println("");
      break;
    case 3:
      tft.println("  /");
      tft.println(" O ");
      tft.println("");
      break;
    case 4:
      tft.println("");
      tft.println(" O ");
      tft.println("|");
      break;
    case 5:
      tft.println("");
      tft.println(" O ");
      tft.println("/");
      break;
    case 6:
      tft.println("");
      tft.println(" O ");
      tft.println("  \\");
      break;
    case 0:
    default:
      tft.println("");
      tft.println(" O ");
      tft.println("");
      break;
  }
}
