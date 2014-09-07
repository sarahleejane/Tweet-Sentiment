import sys
import json
from collections import defaultdict

def parse(fp1, fp2):
    scores = {} # initialize an empty dictionary
    new_scores = defaultdict(list)

    for line in fp1:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    for line in fp2:
        tweet_score = 0
        tweets = json.loads(line)

        if 'text' in tweets:
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

            for item in tweet_words:
                if item not in scores:
                    new_scores[item].append(tweet_score)
    
    for item in new_scores:

        new_word_score_sum = 0
        word_count = 0
        for item_score in new_scores[item]:
            word_count+=1
            new_word_score_sum = new_word_score_sum + item_score

        new_word_score_av = float(new_word_score_sum) / word_count

        print item + ' ' + str(new_word_score_av)

            
def main():
    sentiment_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    parse(sentiment_file, tweet_file)

if __name__ == '__main__':
    main()
