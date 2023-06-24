from umqtt.simple import MQTTClient
import network
from machine import Pin, PWM, ADC
import utime
from time import sleep
import time
import _thread

#upload it via thonny ide To Pico

# Constants
ADAFRUIT_IO_USERNAME = ""  # replace with your Adafruit IO username
ADAFRUIT_IO_KEY = ""  # replace with your Adafruit IO key
FEED_NAME = ""  # replace with your feed name

WifiName = "" # fill
WifiPassWord = "" #fill


led = machine.Pin('LED', machine.Pin.OUT) # buraya da başlangıç için 


# LDR pin connections
ldrBLPin = ADC(Pin(28)) # bottom left
ldrBRPin = ADC(Pin(26))  #  bottom right
ldrTPin = ADC(Pin(27))  #  top 


# Servo pin connections
dikey_servoPin = PWM(Pin(18))#24
yatay_servoPin = PWM(Pin(16))#22

# Defining motor pins

#OUT1  and OUT2
In1Pin=Pin(6,Pin.OUT) 
In2Pin=Pin(7,Pin.OUT)  
EN_APin=Pin(8,Pin.OUT)



#OUT3  and OUT4
In3Pin=Pin(4,Pin.OUT)  
In4Pin=Pin(3,Pin.OUT)  
EN_BPin=Pin(2,Pin.OUT)

led.toggle()

class Servo: # aslında bunu multi Class yapmak lazım INterface gibi 
    def __init__(self,PWMpin,servoTypeValue,freq=50): # need to divide _servoD ,_servoY according to the 
        self.servo = PWMpin
        self.servo.freq(freq)
        self.servoD_default = -5
        self.servoTypeValue = int(servoTypeValue)

    def set_angle(self,angle,multiplication=85):
        angle *=multiplication
        #print("angle"+str(angle))
        self.servo.duty_u16(angle)
        sleep(0.01)

    def set_servo_angle_D(self, angle,multiplication=85): # dikey olanda angle 1700 lerde filan ortada  3480 ler filan da sınır 
        angle *=multiplication
        #print("D angle"+str(angle))
        if angle > 3500:
            angle =3480
        self.servo.duty_u16(angle)
        sleep(0.01)

class LDR:
    def __init__(self,pinAdc):
        self.ldr = pinAdc
    
    def read(self):
        return  self.ldr.read_u16()

class SolarTracker:#Düzenlemeler yapıcaz 
    def __init__(self,yatay_servo, dikey_servo,ldrBL,ldrBR,ldrT,delay_time,tol=50):
        self.yatay_servo = yatay_servo
        self.dikey_servo = dikey_servo

        self.ldrBL = ldrBL
        self.ldrBR = ldrBR
        self.ldrT = ldrT

        self.tol = tol
        self.delay_time = delay_time
    
    def track(self,tplimit=700,multiplication =20): # will make with Thread here
        while True:
            br = self.ldrBR.read() # bottom right
            bl = self.ldrBL.read() # bottom left
            tp = self.ldrT.read() # TOp

            print("br -> "+str(br))
            print("bl -> "+str(bl))
            print("tp -> "+str(tp))

            dhoriz = bl - br # difference between left and right
            #print("dhoriz"+str(dhoriz))

            if dhoriz <= 0:
                if bl == br:
                    pass
                else:
                    self.yatay_servo.servoTypeValue += 1 #

                self.yatay_servo.set_angle(self.yatay_servo.servoTypeValue,multiplication)
            else:
                if br == bl:
                    pass
                else:
                    self.yatay_servo.servoTypeValue -= 1

                self.yatay_servo.set_angle(self.yatay_servo.servoTypeValue,multiplication)

            if tp <tplimit:
                self.dikey_servo.servoTypeValue-= 1#
                if self.dikey_servo.servoTypeValue<self.dikey_servo.servoD_default:
                    self.dikey_servo.servoTypeValue =self.yatay_servo.servoD_default# default değeri
             #   print("if self.dikey_servo.servoTypeValue"+str(self.dikey_servo.servoTypeValue))
                self.dikey_servo.set_servo_angle_D(self.dikey_servo.servoTypeValue,multiplication)
            else:
                self.dikey_servo.servoTypeValue += 1
              #  print("else self.dikey_servo.servoTypeValue"+str(self.dikey_servo.servoTypeValue))
                self.dikey_servo.set_servo_angle_D(self.dikey_servo.servoTypeValue,multiplication)


            #print('Ended')
            utime.sleep_ms(self.delay_time)

class  ListenMQTT: # Shouldn't be thread 
    def __init__(self,userName,Key,FeedName,website = "io.adafruit.com"):
        self.userName = userName
        self.Key = Key
        self.FeedName = FeedName
        self.website = website
        self.client = MQTTClient(self.userName,website,user=self.userName,password=self.Key, ssl=True)
        self.Action = None
        self.station = None

    def connect_Wifi(self,WifiName,PassWord):
        station = network.WLAN(network.STA_IF)
        station.active(True)
        station.connect(WifiName, PassWord)
        # Wait for the connection to the WiFi
        while station.isconnected() == False:
            pass
        print('Connection successful')
        print(station.ifconfig())
        self.station = station
        
    
    def defineAction(self,Action):
        print("DcMotors Added As property")
        self.Action = Action

    def sub_cb(self,topic,msg): # burayı bi taşımam lazım galiba 
        #print(topic,msg)
        # convert bytes to string
        msg_str = msg.decode('utf-8')
        print("msg_str",msg_str)
        if self.Action is not None:
            if(msg_str.endswith("Forward")):
                self.Action.move_forward()
            elif(msg_str.endswith("Backward")):
                self.Action.move_backward()
        
            self.Action.stop()
        else:
            print("Action is not defined.")

    def connect_Feed(self):
        self.client.set_callback(self.sub_cb)
        self.client.connect()
        self.client.subscribe("{}/feeds/{}".format(self.userName, self.FeedName))
    

    def CheckingAllTime(self): # This won't be a thread
        while True:
            self.client.check_msg()






class DcMotor:
    def __init__(self,pinIn1,pinIn2,pinIn3,pinIn4,pinEN_A,pinEN_B): 
        self.In1 = pinIn1
        self.In2 = pinIn2
        self.In3 = pinIn3
        self.In4 = pinIn4
        self.EN_A = pinEN_A
        self.EN_B = pinEN_B
        
        self.EN_A.high()
        self.EN_B.high()

    def move_forward(self,sec=2):
        self.In1.high()
        self.In2.low()
        self.In3.high()
        self.In4.low()
        time.sleep(sec)

    def move_backward(self,sec=2):
        self.In1.low()
        self.In2.high()
        self.In3.low()
        self.In4.high()
        time.sleep(sec)

    def stop(self):
        self.In1.low()
        self.In2.low()
        self.In3.low()
        self.In4.low()


#BUradan itibaren de genel kodlar başlayacak ancak o dediğim thread olayları vs vs de var onlara da bi bakmam lazım

# #Panel (SolarTracker)
yatay_servo = Servo(dikey_servoPin,50) # 24
dikey_servo = Servo(yatay_servoPin,20) # #22

delay_timeForTracker =100
ldrBL = LDR(ldrBLPin) #bottom left
ldrBR = LDR(ldrBRPin) #bottom right
ldrT = LDR(ldrTPin) #top 

solarTrackerobject=SolarTracker(yatay_servo,dikey_servo,ldrBL,ldrBR,ldrT,delay_timeForTracker)


#DcMotor
dcMotors = DcMotor(In1Pin,In2Pin,In3Pin,In4Pin,EN_APin,EN_BPin)


#AdaFruit client
mqttClient = ListenMQTT(ADAFRUIT_IO_USERNAME,ADAFRUIT_IO_KEY,FEED_NAME,"io.adafruit.com")

led.toggle()

mqttClient.connect_Wifi(WifiName,WifiPassWord)
led.toggle()
if mqttClient.station is not None and mqttClient.station.isconnected() == True:
    print("mqttClient.connect_Wifi is true")    
    mqttClient.defineAction(dcMotors)
    mqttClient.connect_Feed()

led.toggle()
time.sleep(2)
led.toggle()

_thread.start_new_thread(solarTrackerobject.track,())
mqttClient.CheckingAllTime()