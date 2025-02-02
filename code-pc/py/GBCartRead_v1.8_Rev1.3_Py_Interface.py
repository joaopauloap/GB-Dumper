# GBCartRead - Arduino Interface
# Version: 1.8
# Author: Alex from insideGadgets (http://www.insidegadgets.com)
# Created: 18/03/2011
# Last Modified: 21/03/2016
# Optimized: 03/10/2022 by WodoWiesel

import os
import sys
import time
import string
import serial
import atexit

# Change COM to the port the Arduino is on.
# You can lower the baud rate of 400Kbit if you have issues connecting to the Arduino or the ROM has checksum errors
ser = serial.Serial('COM3', 57600, timeout=1) # /dev/ttyACM0 (old) or ttyS0 (newer via usb) for linux-based systems

sys.stdout.write('\nGBCartRead v1.8 Rev1.3 by wodowiesel\n')
sys.stdout.write('###################################\n')
sys.stdout.flush()

time.sleep(1)

waitInput = 1
userInput = '0'

while (waitInput == 1):
    sys.stdout.write('\nSelect an option below\n0. Read Header\n1. Dump ROM\n2. Save RAM\n3. Write RAM\n4. Exit\n')
    sys.stdout.write('>')
    sys.stdout.flush()
    userInput = input()

    if (userInput == '0'):
        ser.write('HEADER'.encode())
        sys.stdout.write('\n')
        sys.stdout.write('Game title: ')
        gameTitle = ascii(ser.readline())
        #print (gameTitle)
        gameTitle = gameTitle[2:(len(gameTitle)-5)]
        if (gameTitle != None):
            print (gameTitle)
        else:
            print ('Not found')

        sys.stdout.write('MBC type: ')
        cartridgeType = ascii(ser.readline())
        cartridgeType = cartridgeType[2:(len(cartridgeType)-5)]
        if (cartridgeType == 0):
            print ('ROM ONLY')
        elif (cartridgeType == 1):
            print ('MBC1')
        elif (cartridgeType == 2):
            print ('MBC1+RAM')
        elif (cartridgeType == 3):
            print ('MBC1+RAM+BATTERY')
        elif (cartridgeType == 5):
            print ('MBC2')
        elif (cartridgeType == 6):
            print ('MBC2+BATTERY')
        elif (cartridgeType == 8):
            print ('ROM+RAM')
        elif (cartridgeType == 9):
            print ('ROM+RAM+BATTERY')
        elif (cartridgeType == 11):
            print ('MMM01')
        elif (cartridgeType == 12):
            print ('MMM01+RAM')
        elif (cartridgeType == 13):
            print ('MMM01+RAM+BATTERY')
        elif (cartridgeType == 15):
            print ('MBC3+TIMER+BATTERY')
        elif (cartridgeType == 16):
            print ('MBC3+TIMER+RAM+BATTERY')
        elif (cartridgeType == 17):
            print ('MBC3')
        elif (cartridgeType == 18):
            print ('MBC3+RAM')
        elif (cartridgeType == 19):
            print ('MBC3+RAM+BATTERY')
        elif (cartridgeType == 21):
            print ('MBC4')
        elif (cartridgeType == 22):
            print ('MBC4+RAM')
        elif (cartridgeType == 23):
            print ('MBC4+RAM+BATTERY')
        elif (cartridgeType == 25):
            print ('MBC5')
        elif (cartridgeType == 26):
            print ('MBC5+RAM')
        elif (cartridgeType == 27):
            print ('MBC5+RAM+BATTERY')
        elif (cartridgeType == 28):
            print ('MBC5+RUMBLE')
        elif (cartridgeType == 29):
            print ('MBC5+RUMBLE+RAM')
        elif (cartridgeType == 30):
            print ('MBC5+RUMBLE+RAM+BATTERY')
        elif (cartridgeType == 99):
            print ('WISDOM TREE MAPPER')
        elif (cartridgeType == 252):
            print ('Gameboy Camera')
        else:
            print ('Not found')

        sys.stdout.write('ROM size: ')
        romSize = ascii(ser.readline())
        romSize = romSize[2:(len(romSize)-5)] #int()
        if (romSize == 0):
            print ('32 KByte (no ROM banking)')
        elif (romSize == 1):
            print ('64 KByte (4 banks)')
        elif (romSize == 2):
            print ('128 KByte (8 banks)')
        elif (romSize == 3):
            print ('256 KByte (16 banks)')
        elif (romSize == 4):
            print ('512 KByte (32 banks)')
        elif (romSize == 5 and (cartridgeType == 1 or cartridgeType == 2 or cartridgeType == 3)):
            print ('1 MByte (63 banks)')
        elif (romSize == 5):
            print ('1 MByte (64 banks)')
        elif (romSize == 6 and (cartridgeType == 1 or cartridgeType == 2 or cartridgeType == 3)):
            print ('2 MByte (125 banks)')
        elif (romSize == 6):
            print ('2 MByte (128 banks)')
        elif (romSize == 7):
            print ('4 MByte (256 banks)')
        elif (romSize == 82):
            print ('1.1 MByte (72 banks)')
        elif (romSize == 83):
            print ('1.2 MByte (80 banks)')
        elif (romSize == 84):
            print ('1.5 MByte (96 banks)')
        else:
            print('Not found')

        sys.stdout.write('RAM size: ')
        ramSize = ascii(ser.readline())
        ramSize = ramSize[2:(len(ramSize)-5)]
        if (ramSize == 0 and cartridgeType == 6):
            print ('512 bytes (nibbles)')
        elif (ramSize == 0):
            print ('None')
        elif (ramSize == 1):
            print ('2 KBytes')
        elif (ramSize == 2):
            print ('8 KBytes')
        elif (ramSize == 3):
            print ('32 KBytes (4 banks of 8Kbytes)')
        elif (ramSize == 4):
            print ('128 KBytes (16 banks of 8Kbytes)')
        else:
            print ('Not Found')

        sys.stdout.write('Logo Check: ')
        logoCheck = ascii(ser.readline())
        logoCheck = logoCheck[2:(len(logoCheck)-5)]
        print (logoCheck)
        if (logoCheck == 1):
            print ('OK')
        elif (logoCheck == 0):
            print ('Failed')

    elif (userInput == '1'):
        sys.stdout.write('\nDumping ROM to ' + gameTitle + '.gb')
        readBytes = 0
        inRead = 1
        Kbytesread = 0;
        ser.write('READROM'.encode())
        f = open(gameTitle+'.gb', 'wb')
        while 1:
            if inRead == 1:
                line = ser.read(64)
                if len(line) == 0:
                    break
                readBytes += 64
                f.write(line)
            if readBytes % 1024 == 0 and readBytes != 0:
                sys.stdout.write('#')
                sys.stdout.flush()
            if readBytes % 32768 == 0 and readBytes != 0:
                Kbytesread = Kbytesread + 1
                Kbytesprint = Kbytesread * 32
                sys.stdout.write('%sK' % Kbytesprint)
                sys.stdout.flush()
        sys.stdout.write('\nFinished\n\n')
        sys.stdout.flush()
        f.close()

    elif (userInput == '2'):
        sys.stdout.write('\nDumping RAM to ' + gameTitle + '.sav')
        readBytes = 0
        inRead = 1
        Kbytesread = 0
        ser.write('READRAM'.encode())
        f = open(gameTitle+'.sav', 'wb')
        while 1:
            if inRead == 1:
                line = ser.read(64)
                if len(line) == 0:
                    break
                readBytes += 64
                f.write(line)
            if readBytes % 256 == 0 and readBytes != 0:
                sys.stdout.write('#')
                sys.stdout.flush()
            if readBytes % 1024 == 0 and readBytes != 0:
                Kbytesread = Kbytesread + 1
                sys.stdout.write('%sK' % Kbytesread)
                sys.stdout.flush()
        sys.stdout.write('\nFinished\n\n')
        sys.stdout.flush()
        f.close()

    elif (userInput == '3'):
        sys.stdout.write('\nGoing to write to RAM from ' + gameTitle + '.sav')
        sys.stdout.write('\n*** This will erase the save game from your Gameboy Cartridge ***')
        sys.stdout.write('\nPress y to continue or any other key to abort.')
        sys.stdout.write('\n')
        userInput2 = input()

        if (userInput2 == "y"):
            sys.stdout.write('\nWriting to RAM from ' + gameTitle + '.sav')
            fileExists = 1
            doExit = 0
            printHash = 0
            Kbyteswrite = 0
            try:
                f = open(gameTitle+'.sav', 'rb')
            except IOError:
                sys.stdout.write('No save file found, aborted.\n\n')
                fileExists = 0
            if (fileExists == 1):
                ser.write('WRITERAM'.encode())
                time.sleep(1); # Wait for Arduino to setup
                while 1:
                    if printHash % 4 == 0 and printHash != 0: # 256 / 64 = 4
                        sys.stdout.write('#')
                        sys.stdout.flush()
                    if printHash % 16 == 0 and printHash != 0:
                        Kbyteswrite = Kbyteswrite + 1
                        sys.stdout.write('%sK' % Kbyteswrite)
                        sys.stdout.flush()
                    printHash += 1

                    line1 = f.read(64) # Read 64bytes of save file
                    if not line1:
                        break
                    ser.write(line1)
                    time.sleep (0.005); # Wait 5ms for Arduino to process the 64 bytes

                sys.stdout.write('\nFinished\n\n')
                sys.stdout.flush()
            f.close()
        else:
            sys.stdout.write('Aborted.\n\n')
            sys.stdout.flush()

    elif (userInput == '4'):
        waitInput = 0

    else:
        sys.stdout.write('\nOption not recognised, please try again.\n\n')
ser.close()
#EOF
