#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from wit import Wit

import sys
import rospy
from std_msgs.msg import String

access_token = 'BMYORVSUUOLBANBF6OMPVJUBC2DCAR2J'

if len(sys.argv) == 2:
	access_token = sys.argv[1]

def send(request, response):
    print(response['text'])

actions = {
    'send': send,
    }   

client = Wit(access_token=access_token, actions=actions)

with open("recognized_input.doc") as f:
	data = f.read()
possible_inputs = data.splitlines()
will_pub = True

class Speech_Corrector:

	def __init__(self):
		self.text_sub = rospy.Subscriber("/wit/init_text", String, self.callback)
		self.text_pub = rospy.Publisher('wit/final_text', String, queue_size = 1)

	def callback(self, data): #assumes only one part is given, only one location is given
		words = data
		data = str(data).split()[1:]
		print(data)

		if 'rooms' in data:
			data[data.index('rooms')] = str('room')

		mess = client.message(str(words))
		print("Recieved this message: " + str(mess))

		important_info = mess['entities']

		if len(important_info) != 0:
			for entity in important_info:
				print(entity + ": " + str(important_info[entity][0]['value']))

			percentage_dict = {}
			for line in possible_inputs:
				matching = 0
				line = line.split()
				for word in line:
					if word in data:
						matching += 1
					elif word == "ROOM" and 'room' in important_info:
						matching += 1
					elif word == "COLOR" and 'color' in important_info:
						matching += 1
				if (matching/max([len(data), len(line)])) in percentage_dict:
					percentage_dict[(matching/max([len(data), len(line)]))].append(line)
				else:
					percentage_dict[(matching/max([len(data), len(line)]))] = [line]

			max_percent = -1
			max_percent_val = None
			for key in percentage_dict:
				if key > max_percent:
					max_percent = key
					max_percent_val = percentage_dict[key][0]

			for i in range(len(max_percent_val)):
				word = max_percent_val[i]
				if word == "ROOM":
					try:
						max_percent_val[i] = str(important_info['room'][0]['value'])
					except KeyError:
						print("Didn't quite understand...Can you try again")
						will_pub = False
						break
				elif word == "COLOR":
					try:
						max_percent_val[i] = str(important_info['color'][0]['value'])
					except KeyError:
						print("Didn't quite understand...Can you try again")
						will_pub = False
						break

			if will_pub:
				print(max_percent_val)
				self.text_pub.publish(' '.join(max_percent_val))
		else:
			print("Didn't quite understand...Can you try again")
			#self.text_pub.publish(' '.join(data))


def main(args):
    corrector = Speech_Corrector()
    rospy.init_node("speech_corrector", anonymous=True)

    rospy.spin()

if __name__ == '__main__':
    main(sys.argv)

