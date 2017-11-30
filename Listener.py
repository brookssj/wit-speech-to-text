#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from wit import Wit

import sys
import rospy
from std_msgs.msg import String

def send(request, response):
    print(response['text'])

actions = {
    'send': send,
    }   

if len(sys.argv) != 2:
    print('usage: python ' + sys.argv[0] + ' <wit-token>')
    exit(1)
access_token = sys.argv[1]

client = Wit(access_token=access_token, actions=actions)

class textHandler:

	def __init__(self):
		self.text_sub = rospy.Subscriber("/wit/final_text", String, self.callback)
		### Remember to create a publisher that gives commands eventually

	def callback(self, data): #assumes only one part is given, only one location is given
		mess = client.message(str(data))
		print("Recieved this message: " + str(mess))
		important_info = mess['entities']
		if len(important_info) != 0:
			for entity in important_info:
				print(entity + ": " + str(important_info[entity][0]['value']))

		#print(important_info) ###What should this be returned as?

def main(args):
    handler = textHandler()
    rospy.init_node("text_listener", anonymous=True)

    rospy.spin()
    

if __name__ == '__main__':
    main(sys.argv)


