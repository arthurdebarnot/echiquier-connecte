"""
Principe :

Pour lire la valeur d'une case, on écrit sur le pin associé à la colonne.
On lit ensuite sur le pin associé à la ligne (il n'y en a que 6 car nous n'avions pas de multiplexeurs et nous sommes limités par le nombre de pin du Raspberry)
On allume la led si la case vaut 1.
"""


import RPi.GPIO as GPIO
from rpi_ws281x import PixelStrip, Color
import os
import time

# --- LED setup ---
LED_COUNT      = 64
LED_PIN        = 10
LED_FREQ_HZ    = 800000
LED_DMA        = 10
LED_BRIGHTNESS = 5
LED_INVERT     = False

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()

def set_led(led_index, color):
    strip.setPixelColor(led_index, color)

def clear_strip():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

# --- GPIO setup ---
PINS_LECTURE  = [32, 33, 36, 37, 29, 31]
PINS_ECRITURE = [7, 11, 12, 13, 15, 16, 18, 22]
TOUTES_PINS   = PINS_LECTURE + PINS_ECRITURE

# Configure les broches une seule fois
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
for pin in PINS_LECTURE:
    GPIO.setup(pin, GPIO.IN)
for pin in PINS_ECRITURE:
    GPIO.setup(pin, GPIO.OUT)

L_channel2 = PINS_ECRITURE
L_channel  = PINS_LECTURE

# Correspondance coordonnées -> numéro de led
Correspondance = [
    [15, 14, 13, 12, 11, 10,  9,  8],
    [16, 17, 18, 19, 20, 21, 22, 23],
    [31, 30, 29, 28, 27, 26, 25, 24],
    [32, 33, 34, 35, 36, 37, 38, 39],
    [47, 46, 45, 44, 43, 42, 41, 40],
    [48, 49, 50, 51, 52, 53, 54, 55],
]

board = [[0]*8 for _ in range(6)]

#Affichage du board dans le terminal
def afficher_board(board):
    os.system('clear')
    print("  " + "  ".join([str(j) for j in range(8)]))
    for i, ligne in enumerate(board):
        row = f"{i} "
        for val in ligne:
            if val == 1:
                row += "\033[42m  \033[0m "
            else:
                row += "\033[47m  \033[0m "
        print(row)

try:
    while True: 
        for i in range(6):
            for j in range(8):
                channel2 = L_channel2[j]
                channel  = L_channel[i]

                GPIO.output(channel2, GPIO.HIGH)
                s = sum(GPIO.input(channel) for _ in range(10))
                board[i][j] = round(s / 10)

                if board[i][j] == 1:
                    set_led(Correspondance[i][j], Color(0, 255, 0))  # vert s'il y a une pièce.
                else:
                    set_led(Correspondance[i][j], Color(0, 0, 0))    # éteint sinon.

                time.sleep(0.1)

                strip.show()
        afficher_board(board)

except KeyboardInterrupt:
    print("\nArrêt")
finally:
    clear_strip()
    GPIO.cleanup(TOUTES_PINS)