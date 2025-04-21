# Save this file as main.py in kidbright
import dht
import time
import json
import network
from machine import Pin, I2C
from bmp280 import BMP280
from umqtt.robust import MQTTClient
from config_home import WIFI_SSID, WIFI_PASS, MQTT_BROKER, MQTT_USER, MQTT_PASS
MINUTE = 300000
activate = True
timestamp = time.ticks_ms() - MINUTE
# Use ESP32 NodeMCU
i2c = I2C(0, sda=Pin(21), scl=Pin(22))
lat = 13.73874 # latitude near my house
lon = 100.42007 # longitude near my house
bmp = BMP280(i2c)
dht_sensor = dht.DHT11(Pin(18))
led_wifi = Pin(2, Pin.OUT)
led_wifi.value(0)
led_iot = Pin(4, Pin.OUT)
led_iot.value(0)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASS)
while not wlan.isconnected():
    time.sleep(0.5)
led_wifi.value(1)

mqtt = MQTTClient(client_id="",
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)
mqtt.connect()
led_iot.value(1)
def read_bmp280():
    """BMP280 publishes both temp and pressure."""
    try:
        temp = bmp.temperature
        pressure = bmp.pressure
        print("BMP280 → Temp:", temp, "°C, Pressure:", pressure, "mb or hPa")
        return temp, pressure
    except Exception as e:
        print("BMP280 error:", e)
        return None, None

def read_dht():
    """Less reliable temperature from dht so we will publish only humidity."""
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        print("DHT11 → Temp:", temp, "°C, Humidity:", hum, "%")
        return temp, hum
    except Exception as e:
        print("DHT11 error:", e)
        return None, None

while True:
    now = time.ticks_ms()
    # Wifi connection verification
    if not wlan.isconnected():
        led_wifi.value(0)
        wlan.disconnect()
        wlan.connect(WIFI_SSID, WIFI_PASS)
        time.sleep(10)
        continue
    else:
        led_wifi.value(1)

    # MQTT connection verification
    try:
        mqtt.check_msg()
        led_iot.value(1)
    except Exception as e:
        print("MQTT disconnected:", e)
        led_iot.value(0)
        try:
            mqtt.connect()
            led_iot.value(1)  # Reconnected
        except Exception as e:
            time.sleep(10)
            continue
    if time.ticks_diff(now,timestamp) >= MINUTE:
        if activate == True:
            temp, humid = read_dht();
            true_temp, pressure = read_bmp280();
            data = {
                "lat": lat,
                "lon": lon,
                "temp": true_temp,
                "humid": humid,
                "pressure":pressure,
                }
            mqtt.publish("b6610545308/team_project", json.dumps(data))
            activate = False
        else:
            data1 = {"ping":"pong"}
            mqtt.publish("b6610545308/ping", json.dumps(data1))
            activate = True
        timestamp = now
