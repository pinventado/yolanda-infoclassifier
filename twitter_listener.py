from TwitterAPI import TwitterAPI
import settings
import utils

if __name__ == "__main__":
	twitter = TwitterAPI(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
	query = "#rescueph, #haiyan, #yolandaph"
	req = twitter.request('statuses/filter',{'track':query})
	for tweet in req.get_iterator():
		print tweet
