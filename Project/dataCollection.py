import tweepy
from tweepy.streaming import StreamListener
import json
import time

class twitter_Stream(StreamListener):
    def __init__(self, threshold, outputPart):
        self.count = 0
        self.threshold = threshold
        self.outputPart = outputPart

    def on_data(self, data):
        if self.count % 50000 == 0:
            self.output = open('./output/' + self.outputPart + repr(time.time()) + '.output', 'w')
        datajson = json.loads(data)
        try:
            if datajson["user"]["location"] and datajson["lang"] == 'en':
                self.output.write('{}'.format(data))
                self.count += 1
                print self.count
        except KeyError as keyerr:
            print keyerr
        except:
            pass

        if self.count >= self.threshold:
            self.output.close()
            return False
        return True

    def on_error(self, status_code):
        print 'Error Code: {}'.format(status_code)
        return False

class data_Collect(object):
    def __init__(self, threshold, outputPart):
        self.threshold = threshold
        self.outputPart = outputPart

    def loadKey_Authorize(self, key_file):
        with open('./keysAuth/' + key_file + '.json', 'r') as keysjson:
            kf = json.load(keysjson)

        api_key = kf['api_key'].strip()
        api_secret = kf['api_secret'].strip()
        token = kf['token'].strip()
        token_secret = kf['token_secret'].strip()

        self.auth = tweepy.OAuthHandler(api_key, api_secret)
        self.auth.set_access_token(token, token_secret)

    def run_Stream(self, keywordsList):
        twiStrLis = twitter_Stream(threshold=self.threshold, outputPart=self.outputPart)
        twiStream = tweepy.Stream(self.auth, twiStrLis)
        twiStream.filter(track=keywordsList)


if __name__ == '__main__':

    part = 'part1'              # Available choices: part1, part2, part3, part4

    with open('./keywords/kwds_' + part, 'r') as f:
        keywordsList = [item.strip() for item in f]
    
    keyFiles = ['keys']         # Prefix of the key filename for Twitter's API authorization

    fail_count = 0
    while True:
        t0 = time.time()
        for keyjson in keyFiles:
            twitterData = data_Collect(threshold = 10**7, outputPart = part + '/')
            twitterData.loadKey_Authorize(key_file = keyjson)
            print 'Using {}'.format(keyjson)

            t1 = time.time()
            twitterData.run_Stream(keywordsList)
            t2 = time.time()
            print 'Elapsed Time: {}s'.format(t2-t1)
        t4 = time.time()
        if (t4 - t0) < 60*5:
            fail_count += 1
            print 'Sleeping, fail count: {}'.format(fail_count)
            time.sleep(60*2**fail_count)
