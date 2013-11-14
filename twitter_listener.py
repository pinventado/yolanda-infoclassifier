from TwitterAPI import TwitterAPI
import redis
import settings, utils

if __name__ == "__main__":
	redis_con=redis.StrictRedis(settings.REDIS_HOST,settings.REDIS_PORT, password=settings.REDIS_PASSWORD)

	twitter = TwitterAPI(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
	req = twitter.request('statuses/filter',{'track':settings.TOPICS})
	for tweet in req.get_iterator():
		print tweet
		redis_con.publish(settings.REDIS_CHANNEL,tweet)
