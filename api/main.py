import json
import paho.mqtt.client as mqtt
from rpi_ws281x import Color
import sys
sys.path.insert(0, '../lib')
from lib.truss import truss
import time
import requests

# MQTT Configuration
BROKER = "10.205.10.7"
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

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    try:
        received_message = json.loads(payload)
        command = received_message.get("command")
        value = received_message.get("value", None)

        print(f"Received message: {received_message} on topic: {msg.topic}")

        # Ensure value is a proper list of RGB values
        def parse_color(value):
            if isinstance(value, list) and len(value) == 3:
                return Color(value[0], value[1], value[2])
            return None

        # Command Mapping
        command_map = {
            "ON": truss.show,
            "OFF": truss.clear_all,
            "WHITE_ALL": lambda: truss.set_color_all(Color(255, 255, 255)),
            "COLOR_ALL": lambda: truss.set_color_all(parse_color(value)) if value else None,
            "BRIGHTNESS": lambda: truss.set_brightness(value) if value else None,
            "COLOR_WIPE": lambda: truss.color_wipe(parse_color(value)) if value else truss.color_wipe(Color(255, 0, 0)),
            "RAINBOW": truss.rainbow,
            "RAINBOW_CYCLE": truss.rainbow_cycle,
            "SPARKLE": lambda: truss.sparkle(parse_color(value)) if value else truss.sparkle(Color(255, 255, 255)),
            "SPARKLE_MULTICOLOR": truss.sparkle_multicolor,
            "THEATER_CHASE": lambda: truss.theater_chase(parse_color(value)) if value else truss.theater_chase(Color(0, 255, 0)),
            "THEATER_CHASE_RAINBOW": truss.theater_chase_rainbow,
            "GLOW": lambda: truss.glow(parse_color(value)) if value else truss.glow(Color(255, 0, 255)),
            "WAVE": lambda: truss.wave(parse_color(value)) if value else truss.wave(Color(0, 255, 255)),
            "COLOR_FADE": lambda: truss.color_fade(parse_color(value[0]), parse_color(value[1])) if value and len(value) == 2 else None,
            "SET_COLOR_RANGE_PERCENT": lambda: truss.set_color_range_percent(parse_color(value[0]), value[1], value[2]) if value and len(value) == 3 else None,
            "SET_COLOR_RANGE_EXACT": lambda: truss.set_color_range_exact(parse_color(value[0]), value[1], value[2]) if value and len(value) == 3 else None,
            "RUNNING": truss.running,  # Running effect
            "BITCOIN": truss.bitcoin,
            }

        if command in command_map:
            command_map[command]()
            client.publish(f"{TOPIC_PREFIX}/status", json.dumps({"status": "OK", "command": command}))
            print(f"Command {command} executed successfully")
        else:
            print(f"Unknown command: {command}")
            client.publish(f"{TOPIC_PREFIX}/status", json.dumps({"status": "ERROR", "command": command}))

    except Exception as e:
        print(f"Error processing message: {e}")
        client.publish(f"{TOPIC_PREFIX}/status", json.dumps({"status": "ERROR", "command": command}))

# MQTT Setup
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.username_pw_set("mqtt", "123456789")
mqttc.connect(BROKER, 1883, 60)
mqttc.loop_forever()