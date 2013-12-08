from TwitterAPI import TwitterAPI
from classifier import ReliefClassifier
import settings, utils, json, redis, random

if __name__ == "__main__":
	redis_con=redis.StrictRedis(settings.REDIS_HOST,settings.REDIS_PORT, password=settings.REDIS_PASSWORD)

	twitter = TwitterAPI(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
	req = twitter.request('statuses/filter',{'track':settings.TOPICS})
	classifier = ReliefClassifier()
	for tweet in req.get_iterator():
		print tweet['text']
		classifier.addDocument(tweet['text'],random.choice(['A','NA']))
		print classifier.predict([tweet['text']])
		redis_con.publish(settings.REDIS_CHANNEL,json.dumps(tweet))
