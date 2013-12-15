from gevent import monkey; monkey.patch_all()
from TwitterAPI import TwitterAPI
from classifier import ReliefClassifier
import settings, utils, json, redis, random, gevent, sys, traceback

class TwitterListener:
	def __init__(self, redis_con, classifier):
		self.redis_con = redis_con
		self.classifier = classifier
		self.twitter = TwitterAPI(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)

	def run(self):
		req = self.twitter.request('statuses/filter',{'track':settings.TOPICS})
		for tweet in req.get_iterator():
			if "retweeted_status" in tweet:
				text = 'RT @'+tweet['retweeted_status']['user']['screen_name']+': '+tweet['retweeted_status']['text']
			else:
				text =  tweet['text']
			sys.stdout.write(text+"\n")
			'''if(any([x.lower() in text.lower() for x in settings.AID_KEYWORDS])):
				label="A"
			else:
				label="NA"
			sys.stdout.write(label+"\n")
			sys.stdout.flush()
			self.classifier.addDocument(text,label)'''
			pred = self.classifier.predict([text])
			if pred != -1:
				sys.stdout.write(str(pred[0])+"\n")
				tweet['label']=pred[0]
				self.redis_con.publish(settings.REDIS_CLASSIFIED_CHANNEL,json.dumps(tweet))
				if pred[0]=='A':
					self.redis_con.publish(settings.REDIS_FILTERED_CHANNEL,json.dumps(tweet))
			else:
				sys.stdout.write("No prediction")
			sys.stdout.flush()
			gevent.sleep(0)

	def start(self):
		gevent.spawn(self.run)

class RedisListener:
	def __init__(self, redis_con, classifier):
		self.classifier = classifier
		self.redis_con=redis_con
		self.pubsub = self.redis_con.pubsub()
		self.pubsub.subscribe(settings.REDIS_TRAIN_CHANNEL)		

	def run(self):
		for item in self.pubsub.listen():
					if isinstance(item['data'],str):
						try:
							data = json.loads(item['data'])
							#print data['tweet']
							#print data['label']
							sys.stdout.write("Added doc: "+str(data['label'])+"\n")
							sys.stdout.flush()
							tweet = data['tweet']
							if "retweeted_status" in tweet:
								text = 'RT @'+tweet['retweeted_status']['user']['screen_name']+': '+tweet['retweeted_status']['text']
							else:
								text =  tweet['text']
							self.classifier.addDocument(text,data['label'])
						except:
							exc_type, exc_value, exc_traceback = sys.exc_info()
							traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
							sys.stdout.flush()
							print "error in data: "+str(item)
					gevent.sleep(0)

	def start(self):
		gevent.spawn(self.run)

if __name__ == "__main__":
	redis_con = redis.StrictRedis(settings.REDIS_HOST,settings.REDIS_PORT, password=settings.REDIS_PASSWORD)
	classifier = ReliefClassifier()
	t = TwitterListener(redis_con, classifier)
	r = RedisListener(redis_con, classifier)
	t.start()
	r.start()
	try:
		while(True):
			gevent.sleep(0)
	except KeyboardInterrupt:
		pass
