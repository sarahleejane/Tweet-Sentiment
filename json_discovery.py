import sys
import json

def parse(fp1):

    for line in fp1:
        tweets = json.loads(line)

        for key in tweets:
            print key

        ##Get tweets
        #if 'text' in tweets.keys():
        #    text = tweets['text'].encode('utf-8')
        #    print text

        #Get hashtags
        if 'entities' in tweets.keys():
            text = tweets['entities'].encode('utf-8')
            print text




def main():
    tweet_file = open(sys.argv[1])
    parse(tweet_file)

if __name__ == '__main__':
    main()
