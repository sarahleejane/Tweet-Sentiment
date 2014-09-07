import sys
import json
import operator
from collections import defaultdict

def parse(fp1):
    hashtags = defaultdict(int)

    #Loop through all tweets
    for line in fp1:
        tweets = json.loads(line)

        #Check if hashtag exists, else skip tweet
        tweet_sentence = str(tweets)

        #Find hashtag code in tweet
        posn_start_hashtag_old = tweet_sentence.find("u'hashtags': [{u'indices': ")+30

        if posn_start_hashtag_old-30 != -1:

            #Loop to find any all hashtags
            posn_end_all_hashtags = tweet_sentence.find("}]", posn_start_hashtag_old)

            while True:            
                posn_start_hashtag = tweet_sentence.find(":", posn_start_hashtag_old)+4
                posn_end_hashtag = tweet_sentence.find("'}", posn_start_hashtag)

                if posn_end_all_hashtags < posn_end_hashtag or posn_end_hashtag == -1:
                    break

                hashtag = tweet_sentence[posn_start_hashtag:posn_end_hashtag]
                #for more than 1 hashtag, this will only find the right position every other loop
                if hashtag.find("u'text':")==-1:
                    #Put hashtag into array, along with counter
                    hashtags[hashtag] += 1

                posn_start_hashtag_old = posn_start_hashtag

    for hashtag, score in sorted(hashtags.iteritems(), key=lambda (k, v): (-v, k))[:10]:
        print hashtag, score

def main():
    tweet_file = open(sys.argv[1])
    parse(tweet_file)

if __name__ == '__main__':
    main()
