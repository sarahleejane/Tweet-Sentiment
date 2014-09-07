import sys
import json
import operator
from collections import defaultdict

def parse(fp1, fp2):
    #STEP 1: Create tweet sentiment dictionary called scores
    scores = {} # initialize an empty dictionary
    new_scores = defaultdict(list)
    saved_tweets = defaultdict(list)
    state_av = {} # initialize an empty dictionary

    states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
    }

    states2 = dict((y,x) for x,y in states.iteritems())

    #Build dictionary using sentiment file
    for line in fp1:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    #Loop through all tweets
    for line in fp2:
        tweet_score = 0
        tweets = json.loads(line)

        #Check if location can be determined, else skip tweet
        tweet_sentence = str(tweets)
        posn_start_full_name_part1 = 0
        posn_start_full_name_part1 = tweet_sentence.find("u'full_name'")+16
        if posn_start_full_name_part1 != 0:

            posn_end_full_name_part1 = tweet_sentence.find(',', posn_start_full_name_part1)
            posn_start_full_name_part2 = posn_end_full_name_part1 + 2
            posn_end_full_name_part2 = posn_start_full_name_part2 + 2

            state_guess1 = tweet_sentence[posn_start_full_name_part1:posn_end_full_name_part1]
            state_guess2 = tweet_sentence[posn_start_full_name_part2:posn_end_full_name_part2]

            #only check second part if country code US
            if tweet_sentence.find("u'country_code': u'US'") != 0:
                #only check second part if letters capital
                if not state_guess2.isupper():
                    state_guess2 = "Do not use"

            state_check = 0
            if state_guess1 in states2:
                state = states2[state_guess1]
                state_check = 1
            elif state_guess2 in states:
                state = state_guess2
                state_check = 1

            if state_check == 1:
                #Check line is a tweet, else skip line
                if 'text' in tweets:
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
                        
                        #Put tweet into array, along with location, for later use
                        saved_tweets[state].append(item)
                        
                        if item in scores:
                            tweet_score = tweet_score + scores[item]

                    for item in tweet_words:
                        if item not in scores:
                            new_scores[item].append(tweet_score)

    #Add new terms to dictionary
    for item in new_scores:
        new_word_score_sum = 0
        word_count = 0
        for item_score in new_scores[item]:
            word_count+=1
            new_word_score_sum = new_word_score_sum + item_score

            new_word_score_av = float(new_word_score_sum) / word_count
            scores[item] = new_word_score_av

    #For each state, fine average sentiment score
    for item in saved_tweets:
        state_score = 0
        word_count = 0
        for a in saved_tweets[item]:
            word_count+=1
            state_score = state_score + scores[a]

        state_av[item] = float(state_score)/word_count

    #Find highest average sentiment scored state
    max_state_av = max(state_av.iteritems(), key=operator.itemgetter(1))[0]
    print max_state_av



def main():
    sentiment_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    parse(sentiment_file, tweet_file)

if __name__ == '__main__':
    main()
