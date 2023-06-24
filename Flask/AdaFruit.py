from flask import Flask, request, render_template, jsonify,redirect,url_for
import requests
import paho.mqtt.client as mqtt 
import ssl # source venv/bin/activate 

#YOUR_API_KEY="JQ35dWT_Me84vBQXxJZjwDhiK2Vjnkd2SG04g4BArBs"
#ilerleyen zamanda ben bunu haritalı versiyona da çevirecem


# Constants for AdaFruit
ADAFRUIT_IO_USERNAME = ""  # replace with your Adafruit IO username
ADAFRUIT_IO_KEY = ""  # replace with your Adafruit IO key
FEED_NAME = ""  # replace with your feed name
topic = f"{ADAFRUIT_IO_USERNAME}/feeds/{FEED_NAME}"

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def on_publish(client, userdata, mid):
    print("Message Published...")

# Create client and assign event callbacks
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Setup authentication and connect
client.username_pw_set(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
               tls_version=ssl.PROTOCOL_TLS, ciphers=None)
client.connect("io.adafruit.com", 8883, 60)

client.loop_start()

app = Flask(__name__)



LocationsPico = {
    " ": ' ',
    'D100-Kadıköy': '100 m Forward',   
    'D100-Koşuyolu': '100 m Backward',
}

@app.route('/')
def home():
    return render_template('index.html', locations=LocationsPico.keys())



@app.route('/send_to_pico', methods=['POST'])
def send_to_pico():
    message = request.form.get('message')
    # Insert your MQTT send_message code here
    selected_location = request.form.get('location')
    selected_location_Value = LocationsPico[selected_location]
    print(f"this is the message{selected_location_Value}")
    client.publish(topic, selected_location_Value)
    return jsonify({'status': 'OK'})


if __name__ == "__main__":
    app.run(debug=True)
