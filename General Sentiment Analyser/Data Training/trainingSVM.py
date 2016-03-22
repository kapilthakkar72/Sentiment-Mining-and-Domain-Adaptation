from sklearn import svm
import csv
import re
from sklearn.externals import joblib
#from rudraksh import removeAtTheRate

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


def getIndexIfWordIsPresent(feature_list,word):
    i = 0
    for feature in feature_list:
        match = re.search(r'('+feature[0:len(feature)-1] + ')[a-z]+',word)
        if match:
            return i
        else:
            i=i+1
    return -1

# Read Tweets from Training data...
tweets_path = 'train80.csv'
# Labels
labels = []
tweets = []
# Feature List
feature_list = []
features = open('filtered_added_forms')
some_not_words = open('some_not_words')
features_from_twitter = open('features_from_twitter')
for feature in features:
    feature_list.append(feature[0:len(feature)-1])
for feature in some_not_words:
    feature_list.append(feature[0:len(feature)-1])
for feature in features_from_twitter:
    feature_list.append(feature[0:len(feature)-1])

x = []
y = []

with open(tweets_path, 'r') as csvfile:
    tweets = csv.reader(csvfile, delimiter=",")
    i=0
    for tweet in tweets:
        #i=i+1
        #print i
        #if(i>2):
        #    break
        # Initialise array with number of features
        feature_for_this_tweet = [0] * len(feature_list)
        tt = removeAtTheRate(tweet[1])
        tt = tt.lower()
        tweet.append(tt)
        ############################################
        # Check what features are present in the tweet
        ###########################################
        while(True):
            match = re.search(r'([A-Za-z\']+)', tt)
            if match :                
                start = match.start()
                end = match.end()
                word = tt[start:end]
                # print "Word:" + word
                tt = tt[0:start] + tt[end:]
                b=getIndexIfWordIsPresent(feature_list,word)
                if(b != -1):
                    feature_for_this_tweet[b] = 1
            else:
                break    
        ##########################################
        x.append(feature_for_this_tweet)
        y.append(tweet[0])

print "Training Data"
for i in range(0,len(x)):
    print '"' + str(x[i]) + '","' + str(y[i]) + '"'


print "Feature List extracted... going for training"
#print x        
# Lets got for training....
clf = svm.LinearSVC()
clf.fit(x, y)
joblib.dump(clf, 'svm.pkl') 
# For Testing

training = 'testing20.csv'
with open(small_training, 'r') as csvfile:
    tweets = csv.reader(csvfile, delimiter=",")
    i=0
    for tweet in tweets:
        #print " Before"
        #i=i+1
        #if(i>2):
        #    break
        # Initialise array with number of features
        feature_for_this_tweet = [0] * len(feature_list)
        #print "..................."
        #print feature_for_this_tweet
        #print "..................."
        tt = removeAtTheRate(tweet[1])
        tt = tt.lower()
        tweet.append(tt)
        ############################################
        # Check what features are present in the tweet
        ###########################################
        while(True):
            match = re.search(r'([A-Za-z\']+)', tt)
            if match :                
                start = match.start()
                end = match.end()
                word = tt[start:end]
                # print "Word:" + word
                tt = tt[0:start] + tt[end:]
                b=getIndexIfWordIsPresent(feature_list,word)
                if(b != -1):
                    feature_for_this_tweet[b] = 1
            else:
                break        
        ##########################################
        x.append(feature_for_this_tweet)
        y.append(tweet[0])
        #print i

print "Testing Data"
for i in range(0,len(x)):
    print '"' + str(x[i]) + '","' + str(y[i]) + '"'

print "Predicting"
temp =  clf.predict(x)
correctPredicted = 0
negativePredictedPositive = 0
positivePredictedNegative = 0
for i in range(0,len(temp)):
    print str(y[i]) + "," + str(temp[i])
    if(y[i] == temp[i]):
        correctPredicted = correctPredicted+1
    elif(y[i] == 0):
        negativePredictedPositive = negativePredictedPositive +1
    else:
        positivePredictedNegative = positivePredictedNegative +1
            
print "Correct Predicted: " + str(correctPredicted)
print "negativePredictedPositive: " + str(negativePredictedPositive)
print "positivePredictedNegative: " + str(positivePredictedNegative)
print "Total: " + str(len(temp))
print "Done"