from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import boto3
import base64
import json
import os

polly = boto3.client('polly')

myMQTTClient = AWSIoTMQTTClient("chris-test")
myMQTTClient.configureEndpoint("a1uto1ic4nrwqv-ats.iot.us-west-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials('root-CA.crt', 'chris-test.private.key', 'chris-test.cert.pem')
myMQTTClient.connect()

def callback(a, b, msg):
    payload = msg.payload.decode("utf-8")
    payload = json.loads(payload)
    print(payload["message"])
    response = polly.synthesize_speech(VoiceId="Brian", OutputFormat="mp3", Text=payload["message"])
    file = open('speech.mp3', 'wb')
    file.write(response['AudioStream'].read())
    file.close()
    os.system("afplay speech.mp3")
    os.remove("speech.mp3")

myMQTTClient.subscribe("chris-test/hello", 0, callback)

while True:
    time.sleep(0.5)
