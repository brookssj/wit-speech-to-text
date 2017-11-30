#!/usr/bin/env python

import sys
import rospy
from std_msgs.msg import String
import requests
import json
from Recorder import record_audio, read_audio
 
# Wit speech API endpoint
API_ENDPOINT = 'https://api.wit.ai/speech'
 
# Wit.ai api access token
wit_access_token = 'BMYORVSUUOLBANBF6OMPVJUBC2DCAR2J'

if len(sys.argv) == 2:
    wit_access_token = sys.argv[1]

class speechHandler:
    def __init__(self):
        self.text_pub = rospy.Publisher('wit/init_text', String, queue_size = 1)
    
    def RecognizeSpeech(self, AUDIO_FILENAME, num_seconds = 5):
 
        # record audio of specified length in specified audio file
        record_audio(num_seconds, AUDIO_FILENAME)
 
        # reading audio
        audio = read_audio(AUDIO_FILENAME)
 
        # defining headers for HTTP request
        headers = {'authorization': 'Bearer ' + wit_access_token,
               'Content-Type': 'audio/wav'}
 
        # making an HTTP post request
        resp = requests.post(API_ENDPOINT, headers = headers,
                         data = audio)
 
        # converting response content to JSON format
        data = json.loads(resp.content)
 
        # get text from data
        text = data['_text']
 
        print("\nYou said: {}".format(text))
        self.text_pub.publish(str(text))

def main(args):
    speech = speechHandler()
    rospy.init_node("speech_to_text", anonymous=True)
    speech.RecognizeSpeech('myspeech.wav', 4)

if __name__ == "__main__":
    main(sys.argv)

