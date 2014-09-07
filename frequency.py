import sys
import json
from collections import defaultdict

def parse(fp1):
    individual_terms = defaultdict(list)
    total_word_count=0

    for line in fp1:
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

            #add words to dictionary
            tweet_words = tweet_sentence_no_punctuation.split(" ")
            for item in tweet_words:
                individual_terms[item].append("a")
                total_word_count+=1
    
    for item in individual_terms:
        word_count = 0
        for a in individual_terms[item]:
            word_count+=1

        word_freq = float(word_count) / total_word_count

        print item + ' ' + str(word_freq)

            
def main():
    tweet_file = open(sys.argv[1])
    parse(tweet_file)

if __name__ == '__main__':
    main()
