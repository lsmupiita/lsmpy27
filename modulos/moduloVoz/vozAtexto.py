import argparse
import io
import os


import json
import requests
from pprint import pprint



'''
# Loads the audio into memory
with io.open('./record/test.wav', 'rb') as audio_file:
	content = audio_file.read()
	sample = speech_client.sample(
		content,
		source_uri=None,
		encoding='LINEAR16',
		sample_rate_hertz=44100)

# Detects speech in the audio file
alternatives = sample.recognize('es-MX')

for alternative in alternatives:
	print('Transcript: {}'.format(alternative.transcript))

API_KEY = 'AIzaSyC37p0BfrHuDsYgnRXaFv7nA1tG-_-KfXQ'

def speechPost(filename=''):
	url = 'https://speech.googleapis.com/v1/speech:recognize?key=' + API_KEY
	# leerAudio = open('./record/test.wav', 'rb')

	# Informacion que va al post
	data = {
		"config": {
		    "encoding": "LINEAR16",
		    "sampleRateHertz": 44100,
		    "languageCode": "es-MX"
		}
	}
	files = {
		"audio": {
		   	"content": open('./record/test.wav', 'rb')
		}
	}
	files = {
		"config": {
		    "encoding": ('', "LINEAR16"),
		    "sampleRateHertz": 44100,
		    "languageCode": ('', "es-MX")
		},
		"audio": {
		   	"content": open('./record/test.wav', 'rb')
		}
	}
	config = {
	    "encoding": "LINEAR16",
	    "sampleRateHertz": 44100,
	    "languageCode": "es-MX"
	}
	data = {'config': json.dumps(config)}
	# print (type(files))
	# pprint (files)
	# req = requests.post(url, data=data, files=files)
	req = requests.post(url, data=data, headers={
	                    'Content-Type':'application/json'})
	respuesta = req.json()
	pprint(respuesta)
	print (req.status_code)
'''


def terminoEscribir(filename):
	 # If there is no error when trying to read the file, then it has completely loaded
	return True


def transcribe_file(filename):
    return "El perro come manzana"
# [END speech_transcribe_sync]



# print transcribe_file('blob.wav')
# speechPost()
