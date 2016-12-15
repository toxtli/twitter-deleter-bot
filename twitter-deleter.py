# python twitter-deleter.py -c ../../config/twitter-config.txt

import sys
import time
import json
import getopt
import tweepy
import ConfigParser

reload(sys)  
sys.setdefaultencoding('utf8')

class TwitterController:
	screen_name = ""
	consumer_key = ""
	consumer_secret = ""
	access_token = ""
	access_token_secret = ""
	auth = None
	api = None
	user = None
	data = {}

	def deleteNotRepliedMessages(self):
		statuses = tweepy.Cursor(self.api.user_timeline).items(200)
		for status in statuses:
			print('Deleting tweet ...')
			print(status.id)
			self.api.destroy_status(status.id)

	def login(self):
		print('Logging in ...')
		self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.set_access_token(self.access_token, self.access_token_secret)
		self.api = tweepy.API(self.auth)
		self.user = self.api.get_user(self.screen_name)
		print('Logged in ...')
		return True

	def __init__(self, filename, incoming_callback=None):		
		config = ConfigParser.ConfigParser()
		config.read(filename)
		self.screen_name = config.get('credentials', 'screen_name')
		self.consumer_key = config.get('credentials', 'consumer_key')
		self.consumer_secret = config.get('credentials', 'consumer_secret')
		self.access_token = config.get('credentials', 'access_token')
		self.access_token_secret = config.get('credentials', 'access_token_secret')
		self.login()

def main(argv):
	configUser = None
	configMessenger = None
	opts, args = getopt.getopt(argv, "c:")
	if opts:
		for o, a in opts:
			if o == "-c":
				configUser = a
	twitter = TwitterController(configUser)
	twitter.deleteNotRepliedMessages()

if __name__ == "__main__":
    main(sys.argv[1:])