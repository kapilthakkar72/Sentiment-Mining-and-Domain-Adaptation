import csv
import re
from sets import Set

#This Function removes names tagged in the tweets
def removeAtTheRate(s):
    match = re.search(r'@([A-Za-z0-9_]+)', s)
    if match :
        start = match.start()
        end = match.end()
        s = s[0:start] + s[end:]
        return removeAtTheRate(s)
    else:
        return removeURLs(s)


#This Function removes URLs tagged in the tweets
def removeURLs(s):
    match = re.search(r'((www\.[^\s]+)|(https?://[^\s]+))',s)
    if match :
        start = match.start()
        end = match.end()
        s = s[0:start] + s[end:]
        return removeAtTheRate(s)
    else:
        return cleanTweet(re.sub(r'(.)\1{2,}', r'\1', s)) # To replce loooveee : love
        #return s

def cleanTweet(s):
    s = re.sub("'[nN][tT]", " not ",s)
    s = re.sub("'[vV][eE] ", " have ",s)
    s = re.sub("'[dD] ", " would ",s)
    s = re.sub("['][sS] ", " is ",s)
    s = re.sub("[sS]['] ", " 's ",s)
    s = re.sub("['][lL][lL] ", " will ",s)
    s = re.sub("['][mM] ", " am ",s)
    s = re.sub("['][lL][lL] ", " will ",s)
    s = re.sub("[wW][oO][nN]['][tT] ", " will not ",s)
    s = re.sub("[sS][hH][nN]['][tT] ", " shall not ",s)
    s = re.sub("[cC][aA][nN]['][tT] ", " can not ",s)
    s = re.sub("[nN]['][tT] ", " not ",s)
    s = re.sub("['][rR][eE] ", " are ",s)
    s = re.sub("\\t"," ",s)
    s = re.sub("/ {2,}/g", " ",s)
    return s

stop_words = Set()
stop_words_file_path = "stopWords.txt"
for feature in open(stop_words_file_path,'r'):
    stop_words.add(feature.strip())

features_dict = dict()

# Read Tweets from Training data...
tweets_path = 'F:\\IIT Delhi\\Semester 4\\Natural Language Processing\\Assignment\\training.csv'
# Labels
# Feature List from Twitter
with open(tweets_path, 'r') as csvfile:
    tweets = csv.reader(csvfile, delimiter=",")
    i = 1
    for tweet in tweets:
        tt = removeAtTheRate(tweet[1])
        tt = tt.lower()
        ############################################
        # Check if feature is present or not
        ###########################################
        while(True):
            match = re.search(r'([A-Za-z\']+)', tt)
            if match :                
                start = match.start()
                end = match.end()
                word = tt[start:end]
                # print "Word:" + word
                tt = tt[0:start] + tt[end:]
                if word not in stop_words:
                    if word not in features_dict:
                        features_dict[word] = 1
                    else:
                        features_dict[word] = features_dict[word] + 1
            else:
                break
'''
tweets_path = 'F:\\IIT Delhi\\Semester 4\\Natural Language Processing\\Assignment\\rudraksh\\new_test_set.csv'
# Labels
# Feature List from Twitter
with open(tweets_path, 'r') as csvfile:
    tweets = csv.reader(csvfile, delimiter=",")
    i = 1
    for tweet in tweets:
        tt = removeAtTheRate(tweet[1])
        tt = tt.lower()
        ############################################
        # Check if feature is present or not
        ###########################################
        while(True):
            match = re.search(r'([A-Za-z\']+)', tt)
            if match :                
                start = match.start()
                end = match.end()
                word = tt[start:end]
                # print "Word:" + word
                tt = tt[0:start] + tt[end:]
                if word not in stop_words:
                    if word not in features_dict:
                        features_dict[word] = 1
                    else:
                        features_dict[word] = features_dict[word] + 1
            else:
                break

'''
features_with_freq = []
for key in features_dict:
    features_with_freq.append((key,features_dict[key]))

features_with_freq.sort(key=lambda tup: tup[1])
    
for x in features_with_freq:
    print x[0] + "," + str(x[1])
