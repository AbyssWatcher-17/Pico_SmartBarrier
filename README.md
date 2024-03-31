# Pico_SmartBarrier

## Summary 

It's a Bachelor Course Project—a small prototype with Raspberry Pi Pico aiming to make barriers smart. The goal is to reduce traffic congestion when necessary and utilize space more efficiently.
(I recommend using a microcontroller with 4 Adc pinouts.It may be other Raspery Pi models or other ESP32 models maybe)

For Detailed Version look at here

![SmartBarrier](https://github.com/AbyssWatcher-17/Pico_SmartBarrier/assets/64128266/ed8ed0dd-523e-46d6-9e4e-a42b1e7b7c05)


#### It has 2 Main Parts :
* Web
  *  MQTT Cloud (AdaFruit)
  *  Flask Framework
* Robot
  * Hardware
  * Mechanical
  * Software



## -> Web:
* MQTT Cloud(AdaFruit)
  * Sign- up from https://io.adafruit.com/
  * Create a new Feed
* Flask FrameWork
  *  cd Flask
  *  python AdaFruit.py

## -> Robot
* Hardware
  * 1 Raspberry Pi Pico
  * 1 L298N
  * 2 DC Motors
  * 4 LDR sensors (I used 3 because Pico has 3 ADC pin to Read)
  * 1 Solar Panel (10x20 cm)
  * 1 Voltage Control USB Regulator:
  * 2 (3.7 V) Batteries
  * 1 LM 7805
  * 1 Copper Plate (Optional)
  
* Mechanical
  * 3D Printer https://drive.google.com/drive/folders/1hb0MZrVrAALZshriPRli9M9IU6Oxqj3v?usp=sharing

* Software
  * Upload MixAllPico.py to Raspberry Pi Pico and rename it main.py using Thonny IDE -> https://thonny.org/

Note: All Contributions will be welcomed.Don't Forget to give star :)


