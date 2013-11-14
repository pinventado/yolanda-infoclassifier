from TwitterAPI import TwitterAPI
#import redis
import os, utils
#uncomment when working locally; provide settings.py file
#import settings 

#comment when working locally
###Server code###
import imp
imp.load_source('settings', os.environ['OPENSHIFT_DATA_DIR']+'/settings.py')
###End of server code###

class TwitterListener:
	def __init__(self):
		self.listeners = []
		self.twitter = TwitterAPI(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)

	def register(self, listener):
		self.listeners.append(listener)

	def start(self):
		# add functionality to reload topic list
		req = self.twitter.request('statuses/filter',{'track':settings.TOPICS})
		for tweet in req.get_iterator():
			for listener in self.listeners:
				listener(tweet)
def test(tweet):
	print "::"+str(tweet)


if __name__ == "__main__":
	t = TwitterListener()
	t.register(a)
	t.start()
	#redis_con=redis.StrictRedis(settings.REDIS_HOST,settings.REDIS_PORT, password=settings.REDIS_PASSWORD)

	#req = twitter.request('statuses/filter',{'track':settings.TOPICS})
	#for tweet in req.get_iterator():
	#	print tweet
	#	redis_con.publish(settings.REDIS_CHANNEL,tweet)
