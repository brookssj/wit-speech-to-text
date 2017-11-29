#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from wit import Wit

import sys
import rospy
from std_msgs.msg import String

with open("recognized_input.doc") as f:
	data = f.read()
	print(data.splitlines())
possible_inputs = data.splitlines()

class Speech_Corrector:

	def __init__(self):
		self.text_sub = rospy.Subscriber("/wit/init_text", String, self.callback)
		self.text_pub = rospy.Publisher('wit/final_text', String, queue_size = 1)

	def callback(self, data): #assumes only one part is given, only one location is given
		mess = client.message(str(data))
		print("Recieved this message: " + str(mess))
		important_info = mess['entities']
		if len(important_info) != 0:
			for entity in important_info:
				print(entity + ": " + important_info[entity][0]['value'])

	#def correct(self, data):
			percentage_dict = {}
			for line in possible_inputs:
				matching = 0
				for word in line:
					if word in data:
						matching += 1
					elif word == "ROOM" and 'room' in important_info:
						matching += 1
					elif word == "COLOR" and 'color' in important_info:
						matching += 1
				if matching/max([len(data), len(line)]) in percentage_dict:
					percentage_dict[max([len(data), len(line)])].append(line)
				else:
					percentage_dict[max([len(data), len(line)])] = [line]

			max_percent = -1
			max_percent_val = None
			for key in percentage_dict:
				if key > max_percent:
					max_percent = key
					max_percent_val = percentage_dict[key][0]
			for word in max_percent_val:
				if word == "ROOM":
					word = important_info['room'][0]['value']
				elif word == "COLOR":
					word = important_info['color'][0]['value']
			self.text_pub.publish(max_percent_val)
		else:
			self.text_pub.publish(data)


def main(args):
    corrector = Speech_Corrector()
    rospy.init_node("speech_corrector", anonymous=True)

    rospy.spin()

