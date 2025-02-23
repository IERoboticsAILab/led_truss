import json
import paho.mqtt.client as mqtt
from rpi_ws281x import Color
import sys
sys.path.insert(0, '../lib')
from lib.truss import truss
import time
import requests

# MQTT Configuration
TOPIC_PREFIX = "home/truss"

# Initialize Truss Instance
truss = truss()

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully.")
        client.subscribe(f"{TOPIC_PREFIX}/#")
    else:
        print(f"Failed to connect, error code: {rc}")

# Define a dictionary to map effect names to functions
EFFECT_MAP = {
    "Rainbow": truss.rainbow,
    "Rainbow Cycle": truss.rainbow_cycle,
    "Sparkle": lambda color: truss.sparkle(Color(color['r'], color['g'], color['b'])),
    "Sparkle Multicolor": truss.sparkle_multicolor,
    "Theater Chase": lambda color: truss.theater_chase(Color(color['r'], color['g'], color['b'])),
    "Theater Chase Rainbow": truss.theater_chase_rainbow,
    "Glow": lambda color: truss.glow(Color(color['r'], color['g'], color['b'])),
    "Wave": lambda color: truss.wave(Color(color['r'], color['g'], color['b'])),
    "Color Wipe": lambda color: truss.color_wipe(Color(color['r'], color['g'], color['b'])),
    "Bitcoin": truss.bitcoin,
    "Running": truss.running
}

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    try:
        received_message = json.loads(payload)
        state = received_message.get("state")
        brightness = received_message.get("brightness")
        color = received_message.get("color")
        effect = received_message.get("effect")

        if state == "ON":
            truss.show()
            if brightness is not None:
                truss.set_brightness(int(brightness))
            if color is not None:
                truss.set_color_all(Color(color['r'], color['g'], color['b']))
            if effect in EFFECT_MAP:
                if "color" in received_message and callable(EFFECT_MAP[effect]):  
                    EFFECT_MAP[effect](received_message["color"])  # Pass color if needed
                else:
                    EFFECT_MAP[effect]()  # Call function without parameters
        elif state == "OFF":
            truss.clear_all()

        # Publish state back to Home Assistant
        client.publish(f"{TOPIC_PREFIX}/state", json.dumps(received_message), qos=1, retain=True)

    except Exception as e:
        print(f"Error processing message: {e}")      

# MQTT Setup
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.username_pw_set("mqtt", "123456789")
mqttc.connect("10.205.10.7", 1883, 60)

# Start MQTT loop in a separate thread
mqttc.loop_start()

try:
    while True:
        time.sleep(1)  # Keep main thread alive
except KeyboardInterrupt:
    print("Disconnecting MQTT...")
    mqttc.loop_stop()  # Stop the MQTT loop
    mqttc.disconnect()  # Disconnect cleanly