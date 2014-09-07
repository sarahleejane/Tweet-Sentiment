import sys
import json

def parse(fp1, fp2):
    scores = {} # initialize an empty dictionary
    for line in fp1:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    for line in fp2:
        tweet_score = 0
        tweets = json.loads(line)
        if 'text' in tweets:
            #store in string variable
            tweet_sentence = str(tweets)

            #trim string from "text": to "source":
            posn_start_tweet = tweet_sentence.find("'text':")+9
            posn_end_tweet = tweet_sentence.find("'source':")
            

            tweet_trimmed = tweet_sentence[posn_start_tweet:posn_end_tweet]

            #clean up variable - convert it to lowercase, remove punctuation
            tweet_sentence_lowercase = tweet_trimmed.lower()

            punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            tweet_sentence_no_punctuation = ""
            for char in tweet_sentence_lowercase:
                if char not in punctuations:
                    tweet_sentence_no_punctuation = tweet_sentence_no_punctuation + char

            #check if each word appears in sentiment dictionary using split and loop
            tweet_words = tweet_sentence_no_punctuation.split(" ")
            for item in tweet_words:
                tweet_word = item

                if tweet_word in scores:
                    tweet_score = tweet_score + scores[tweet_word]
        #print tweet_score
        print tweet_sentence_no_punctuation

def main():
    sentiment_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    parse(sentiment_file, tweet_file)

if __name__ == '__main__':
    main()
