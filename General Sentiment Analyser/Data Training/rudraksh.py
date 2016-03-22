import csv
import re

#This Function removes names tagged in the tweets
def removeAtTheRate(s):
    match = re.search(r'@([A-Za-z0-9_]+)', s)
    if match :
        start = match.start()
        end = match.end()
        s = s[0:start] + s[end:]
        return removeAtTheRate(s)
    else:
        return s

# Generate Feature List
# Words Defining Positiveness or Negativeness
vocab = 'F:\\IIT Delhi\\Semester 4\\Natural Language Processing\\Assignment\\rudraksh\\Pos_neg.csv'
feature_list = []
with open(vocab, 'r') as vocabfile:
    vocabs = csv.reader(vocabfile, delimiter=",")
    for word in vocabs:
        if(word[2]!="" or word[3]!=""):
            # Remove '#' if present
            x = word[0].find("#")
            if(x==-1):
                feature_list.append(word[0].lower())
            else:
                feature_list.append((word[0][0:x]).lower())        
# Remove first entry
feature_list.pop(0)
# Length of feature List
print len(feature_list)

feature_present = [False] * len(feature_list)

'''
# Printing Some of the Features
for i in range(0,10):
    print feature_list[i]
'''


'''
# Processing With Tweet data
# 1. Remove @ words, they do not represent anything
# 2. Convert tweet to lower-case
'''

# Read Tweets from Training data...
tweets_path = 'F:\\IIT Delhi\\Semester 4\\Natural Language Processing\\Assignment\\training.csv'
# Labels
labels = []
tweets = []
# Feature List from Twitter
features_from_twitter = []
features_from_twitter_freq = []
feature_list_freq = [0] * len(feature_list)
with open(tweets_path, 'r') as csvfile:
    tweets = csv.reader(csvfile, delimiter=",")
    i = 1
    for tweet in tweets:
        tt = removeAtTheRate(tweet[1])
        tt = tt.lower()
        tweet.append(tt)
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
                try:
                    b=feature_list.index(word)
                except ValueError:
                    # Not in feature list
                    # Search in Twitter words
                    try:
                        c = features_from_twitter.index(word)
                        #print "Searching for " + word + " in:" + str(features_from_twitter)
                    except ValueError:
                        # Not in Twitter feature list, add it
                        features_from_twitter.append(word)
                        features_from_twitter_freq.append(1)
                    else:
                        #print "and it found at location " + str(c)
                        features_from_twitter_freq[c] = features_from_twitter_freq[c] + 1
                else:
                    feature_present[b] = True
                    feature_list_freq[b] = feature_list_freq[b] + 1
            else:
                break        
        ##########################################
        labels.append(tweet[0])
        i = i+1
        if (i==(1600000*0.8)):
        #if (i==(5)):
            break

new_feature_list = []
for i in range(0,len(feature_list)):
    if(feature_present[i]):
        new_feature_list.append(feature_list[i])
        
print "\n\nNew Feature List..." + str(len(new_feature_list))

features_with_freq = []
n = len(feature_list)
for i in range(0,n):
    features_with_freq.append((feature_list[i],feature_list_freq[i]))
features_with_freq.sort(key=lambda tup: tup[1])

for i in range(0,n):
    print features_with_freq[i][0] + "," + str(features_with_freq[i][1])
    
twitter_features_with_freq = []
print "\n\nTwitter List..."    
for i in range(0,len(features_from_twitter)):
    twitter_features_with_freq.append((features_from_twitter[i],features_from_twitter_freq[i]))

twitter_features_with_freq.sort(key=lambda tup: tup[1])

for x in twitter_features_with_freq:
    print x[0] + "," + str(x[1])

print "Done"