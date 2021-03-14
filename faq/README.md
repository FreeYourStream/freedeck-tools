# Freedeck FAQ

## Ordering stage

### What components do I need

#### Through hole PCB (Adviced to starters in soldering)
You will need:
- PCB / Perfboard
- Arduino Pro Micro (32u4, 16MHz, 5V)
- 2x 4051 Multiplexers
- 6x SSD1306 0.96" OLED
- 6x 3x4x2mm SMD buttons
- SPI-SDcard reader (Micro SD form)

#### SMD varient (For advanced solderers)
See the BOM with the PCB you are using

### Where can I find resources
You can find resources in the various github repo's, or you can ask us in the [discord](https://discord.gg/sEt2Rrd)

### Where can I order the PCB
We do have a good experience with [JLCPCB](https://jlcpcb.com) (Not affilated). You can also find some other company like EuroCurcuits

### What do i need to order the PCB
The GERBER-file zip that you can find in the hardware github repo

## Manufaturing

### Is there a specific order to solder the components in?
Yes, we are currently making a guide on how to solder the components

### Some pins are harder to solder
Correct, the GND pins are harder to get to temperature. Have some patient, and let the solder flow. If it doesn't flow, the board might be bad on the long run.
(Insert pictures of good and bad soldering connections as example)

### I did something wrong, and now?
Try carefully to heat all the pins. What ever you do, **DO NOT FORCE IT, YOU WILL DAMAGE SOME PARTS**

## Programming

### Libraries are missing
In case the Arduino IDE says you're missing some libraries, please install the SD-FAT and HID-Project libraries. How? [Read this guide](https://www.arduino.cc/en/guide/libraries)

### Device / COM-port not found.
Unplug the device, wait 10 seconds, plug it in again. Select the right port and try to upload it.

## Hardware faults

### The screens don't turn on

#### software issue
Have you programmed it?

#### Check the voltage
The voltage between GND and VCC should be between 5V and 4V. At SCK and SDA it should be around 3V3. If one of these is not correct, you have some loose wire somewhere

### The screens are white
(Insert picture)
#### Formatting SD card
The SD card should be formatted mbt FAT32 (On windows, just FAT32)

#### config.bin file
Format the SD card, and put it as only file on the SD card, not in a folder or anything

#### Still issues?
Look at the software part

### One of the screens isn't turning on

#### Check the voltages. 
See above for the correct voltages

#### Boot delay
Increase the boot delay in software. Some screens take some more time with starting

#### Reset
For some strange reason, we haven't figured out yet, the screens wont turn on on boot, but will on a reset. Short the GND and RST pins on the arduino, they might turn on then.

#### Still not?
In the software you can play around with the I2C_delay (change it to 10, and slowly lower it).

### The screens are snowy, or display everything out of order

#### Out of order
In or descrease the IMG_CACHE_SIZE, this might resolve the issue

#### Snowy displays
Change the I2C_DELAY time to 10, and slowly decrease it untill it becomes unstable

#### Something else
Please visit us on Discord (Link somewhere on this page)

### The buttons don't work

#### Use the test sketch
We are currently working on a test sketch so you can test the buttons.

### General test

#### Test config.bin
There is a test config.bin, which checks almost all features of the freedeck, please try it, and report what does, and doesn't work

### My issue isn't on this list.
Please your our discord, ask for help in the #help channel. Please mention the follow things so we can help faster.
- Which PCB variant you are using
- What exactly doesn't work. The more details the better. And pictures speak a 1000 words!
- What software release you have.
- Possibly the config.bin files if you think they might be the issue.
- Results from the test config.bin and button test sketch (If relevant)

We are all volunteers, so it might take some time for us to respond, and find the issue.

## I have this amazing feature

### I want to add it. How?
You can fork the code, add the feature, and create a pull request.

### I would like, but I can't code
Ask around in the Discord. Maybe someone is already working on it.
You could also make a issue on the github, with a feature request.

## Something else which isn't covered in the FAQ
Then its a not that common issue. Ask it in the discord!

## How can i support this project?
Currently there is not really  a way, but you can always give us a star on Github

## Who are the contributors?
The main contributors are:
- Koriwi
- AdamWelchUk
- All of you the Freedeck users


## Configurator links

## 3D files links


