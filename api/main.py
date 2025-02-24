import json
import paho.mqtt.client as mqtt
#from rpi_ws281x import Color
import sys
# sys.path.insert(0, '../lib')
# from lib.truss import truss
import time
import requests

# MQTT Configuration
TOPIC_PREFIX = "home/truss"

class State:
    def __init__(self):
        self.state = "OFF"
        self.brightness = 125
        self.color = {"r": 255, "g": 255, "b": 255}  # Default white
        self.effect = None

    def to_dict(self):
        return {
            "state": self.state,
            "brightness": self.brightness,
            "color": self.color,
            "effect": self.effect
        }

    def update(self, new_state=None, brightness=None, color=None, effect=None):
        if new_state is not None:
            self.state = new_state
        if brightness is not None:
            self.brightness = brightness
        if color is not None:
            self.color = color
        if effect is not None and effect in EFFECT_MAP:
            self.effect = effect
        elif effect is not None:
            self.effect = None

# Initialize Truss Instance and State
# truss = truss()
current_state = State()

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully.")
        client.subscribe(f"{TOPIC_PREFIX}/#")
        # Publish current state on connect
        client.publish(f"{TOPIC_PREFIX}/state", json.dumps(current_state.to_dict()), qos=2, retain=True)
        print("Published initial state")
    else:
        print(f"Failed to connect, error code: {rc}")

# Define a dictionary to map effect names to functions
EFFECT_MAP = {
    "Rainbow": print("Rainbow"),#truss.rainbow,
    "Rainbow Cycle": print("Rainbow Cycle"),#truss.rainbow_cycle,
    "Sparkle": lambda color: print(f"Sparkle, color: {color}"),#truss.sparkle(Color(color['r'], color['g'], color['b'])),
    "Sparkle Multicolor": print("Sparkle Multicolor"),#truss.sparkle_multicolor,
    "Theater Chase": lambda color: print(f"Theater Chase, color: {color}"),#truss.theater_chase(Color(color['r'], color['g'], color['b'])),
    "Theater Chase Rainbow": print("Theater Chase Rainbow"),#truss.theater_chase_rainbow,
    "Glow": lambda color: print(f"Glow, color: {color}"),#truss.glow(Color(color['r'], color['g'], color['b'])),
    "Wave": lambda color: print(f"Wave, color: {color}"),#truss.wave(Color(color['r'], color['g'], color['b'])),
    "Color Wipe": lambda color: print(f"Color Wipe, color: {color}"),#truss.color_wipe(Color(color['r'], color['g'], color['b'])),
    "Bitcoin": print("Bitcoin"),#truss.bitcoin,
    "Running": print("Running")#truss.running
}

def on_message(client, userdata, msg):
    global current_state
    payload = msg.payload.decode()
    try:
        if not payload:
            return

        received_message = json.loads(payload)
        
        if msg.topic == f"{TOPIC_PREFIX}/command":
            print(f"Received command: {received_message}")
            
            state = received_message.get("state")
            brightness = received_message.get("brightness", 125)  # Default to 125 if not set
            color = received_message.get("color", {"r": 255, "g": 255, "b": 255})  # Default to white if not set
            effect = received_message.get("effect")

            # Update the state object
            current_state.update(state, brightness, color, effect)

            if state == "ON":
                if effect in EFFECT_MAP:
                    if "color" in received_message and callable(EFFECT_MAP[effect]):
                        print(f"Running effect: {effect} with color")
                        EFFECT_MAP[effect](color)
                    else:
                        print(f"Running effect: {effect}")
                        EFFECT_MAP[effect]

                else: 
                    print(f"Setting brightness to {brightness}")
                    #truss.set_brightness(brightness)
                    
                    print(f"Setting color to {color}")
                    #truss.set_color_all(Color(color['r'], color['g'], color['b']))
            else:
                print("Clearing all")
                #truss.clear_all()
                current_state.state = "OFF"

        # Always publish state for both /command and /state topics
        client.publish(f"{TOPIC_PREFIX}/state", json.dumps(current_state.to_dict()), qos=2, retain=True)
        
    except Exception as e:
        print(f"Error processing message: {e}")

# MQTT Setup
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.username_pw_set("mqtt", "123456789")
mqttc.connect("10.205.10.7", 1883, 60)

mqttc.loop_forever()