import time
import dht
import machine
import json
from umqtt.simple import MQTTClient

# Configurações do Sensor DHT11
DHT_PIN = 2  

# Configurações MQTT
TOKEN = "BBUS-hlBUrkvVHJaxNyHAsZ4zVQbo8hqNrA"
DEVICE_LABEL = "Rasp"
VARIABLE_LABEL_1 = "temperature"
VARIABLE_LABEL_2 = "humidity"
VARIABLE_LABEL_3 = "position"

MQTT_BROKER = "industrial.api.ubidots.com"
MQTT_PORT = 1883
MQTT_TOPIC = "/v1.6/devices/{}".format(DEVICE_LABEL)

# Inicializa o sensor DHT11
dht_sensor = dht.DHT11(machine.Pin(DHT_PIN))

def build_payload(variable_1, variable_2):
    dht_sensor.measure()
    temp = dht_sensor.temperature()  
    hum = dht_sensor.humidity()      



    payload = {
        variable_1: temp,
        variable_2: hum,
    }
    return payload

def main():
    client = MQTTClient(DEVICE_LABEL, MQTT_BROKER, port=MQTT_PORT, user=TOKEN, password="")
    client.connect()

    payload = build_payload(VARIABLE_LABEL_1, VARIABLE_LABEL_2)

    print("[INFO] Tentando enviar dados")
    client.publish(MQTT_TOPIC, json.dumps(payload))
    print("[INFO] Dados enviados")
    client.disconnect()

if __name__ == '__main__':
    while True:
        main()
        time.sleep(5)  