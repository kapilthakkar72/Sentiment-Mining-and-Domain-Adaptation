from sets import Set
import csv
import re
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from sklearn.externals import joblib
import random

# testingChunk = random.randint(1, 5)
# testingChunk_2 = random.randint(6,10)

testingChunk = 5
testingChunk_2 = 10

while(testingChunk == testingChunk_2):
    testingChunk_2 = random.randint(1,10)


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

# Primay Feature List
primary_feature_list_file_path = "filtered_features"
primary_feature_list = []
for feature in open(primary_feature_list_file_path,'r'):
    if(len(feature.strip()) >1 ):
        primary_feature_list.append(feature.strip())

# Adding Some "Not" words into filtered_features as well
some_not_words = "some_not_words"
for feature in open(some_not_words,'r'):
    primary_feature_list.append(feature.strip())

primary_feature_list_file_path = "temp1"
for feature in open(primary_feature_list_file_path,'r'):
    primary_feature_list.append(feature.strip())
    
# Getting All verbs
verb_file_path = "verbs"
base_verb = []
other_forms = []
for verb in open(verb_file_path,'r'):
    splitted = verb.split()
    base_verb.append(splitted[1].strip())
    other_forms.append((splitted[2].strip(),splitted[3].strip(),splitted[4].strip(),splitted[5].strip()))

print "primary_feature_list length:" + str(len(primary_feature_list))

# Ceating map
dict_of_features = dict()
i = 0
for feature in primary_feature_list:
    try:
        c = base_verb.index(feature)
    except ValueError:
        dict_of_features[feature] = i
        i = i+1
    else:
        dict_of_features[feature] = i
        dict_of_features[other_forms[c][0]] = i
        dict_of_features[other_forms[c][1]] = i
        dict_of_features[other_forms[c][2]] = i
        dict_of_features[other_forms[c][3]] = i
        i = i+1

# # Emoticons....
# emoticons_file_path = "emoticons"
# emoticons = Set()
# for emoticon in open(emoticons_file_path,'r'):
#     emoticons.add(emoticon.strip())
#     dict_of_features[emoticon.strip()] = i
# no_of_emoticons = 0
        
#print dict_of_features
print "Dictionary has total features : " + str(len(dict_of_features))
# Our map is ready now... Lets go for Training
x = []
y = []
feature_dict = []
for j in range(1,12):
    print "Chunk " + str(j)
    if(j==testingChunk or j==testingChunk_2):
        continue
    tweets_path = 'chunk'+ str(j) +'.csv'    
    with open(tweets_path, 'r') as csvfile:
        tweets = csv.reader(csvfile, delimiter=",")
        for tweet in tweets:
            i = i +1
            if(i%10000 == 0):
            #    break
                print i
            # Initialise array with number of features
            # feature_for_this_tweet = [0] * num_of_features
            tt = removeAtTheRate(tweet[1])
            tt = tt.lower()
            D = dict()
            
            # Check for presence of emoticons
            # for emoticon in emoticons:
            #     if(tt.find(emoticon) != -1):
            #         D[emoticon] = 1
            #         no_of_emoticons = no_of_emoticons +1
            
            while(True):
                match = re.search(r'([A-Za-z\']+)', tt)
                if match :                
                    start = match.start()
                    end = match.end()
                    word = tt[start:end]
                    tt = tt[0:start] + tt[end:]
                    if word in dict_of_features:
                        D[word] = 1
                else:
                    break
            #if(len(D) == 0):
            #    continue
            feature_dict.append(D)
            y.append(tweet[0])

v = DictVectorizer(sparse=True)
X = v.fit_transform(feature_dict)

print "Converted to Array"

print "Constructing Feature Map"
dict_of_features = dict()
# This returns array of features in the order which are used for training SVM, order generated by DictVectorizer
features = v.get_feature_names()

i = 0
for feature in features:
    dict_of_features[feature] = i
    i = i+1
num_of_features = len(dict_of_features)

# Write Features to file
fo = open("submission/features", "rw+")
for feature in features:
    fo.write(feature + "\n")
fo.close()

print "READY"

# Lets got for training....
clf = svm.LinearSVC()
clf.fit(X, y)
joblib.dump(clf, 'submission/svm.pkl') 

del X
del y
del features
del primary_feature_list
del feature_dict

print "SVM Trained.... Testing Data Creation"
print "Number of features ... " + str(num_of_features)
#print "Number of Emoticons in training: " + str(no_of_emoticons)

no_of_emoticons = 0

clf = 0
clf = svm.LinearSVC()

clf = joblib.load('submission/svm.pkl') 

T = []
y = []
temp = []

training = 'chunk'+str(testingChunk)+'.csv'
with open(training, 'r') as csvfile:
    tweets = csv.reader(csvfile, delimiter=",")
    i=0
    for tweet in tweets:
        i = i +1
        T = []
        if(i%100000 == 0):
        #    break
            print i
        # Initialise array with number of features
        feature_for_this_tweet = [0] * num_of_features
        tt = removeAtTheRate(tweet[1])
        tt = tt.lower()
        
        # Check for presence of emoticons
        # for emoticon in emoticons:
        #     if(tt.find(emoticon) != -1):
        #         if emoticon in dict_of_features:
        #             no_of_emoticons = no_of_emoticons +1
        #             feature_for_this_tweet[dict_of_features[emoticon]] = 1
        #D = dict()
        ############################################
        # Check what features are present in the tweet
        ###########################################
        while(True):
            match = re.search(r'([A-Za-z\']+)', tt)
            if match :                
                start = match.start()
                end = match.end()
                word = tt[start:end]
                tt = tt[0:start] + tt[end:]
                if word in dict_of_features:
                    #print word + " " + str(dict_of_features[word])
                    feature_for_this_tweet[dict_of_features[word]] = 1
                    #D[word] = 1
            else:
                break    
        ##########################################
        #x.append(feature_for_this_tweet)
        T.append(feature_for_this_tweet)
        temp2 = clf.predict(T)
        temp.append(temp2[0])
        y.append(tweet[0])

training = 'chunk'+str(testingChunk_2)+'.csv'
with open(training, 'r') as csvfile:
    tweets = csv.reader(csvfile, delimiter=",")
    i=0
    for tweet in tweets:
        T = []
        i = i +1
        if(i%100000 == 0):
        #    break
            print i
        # Initialise array with number of features
        feature_for_this_tweet = [0] * num_of_features
        tt = removeAtTheRate(tweet[1])
        tt = tt.lower()
        # for emoticon in emoticons:
        #     if(tt.find(emoticon) != -1):
        #         if emoticon in dict_of_features:
        #             feature_for_this_tweet[dict_of_features[emoticon]] = 1
        #             no_of_emoticons = no_of_emoticons +1
        #D = dict()
        ############################################
        # Check what features are present in the tweet
        ###########################################
        while(True):
            match = re.search(r'([A-Za-z\']+)', tt)
            if match :                
                start = match.start()
                end = match.end()
                word = tt[start:end]
                tt = tt[0:start] + tt[end:]
                if word in dict_of_features:
                    #print word + " " + str(dict_of_features[word])
                    feature_for_this_tweet[dict_of_features[word]] = 1
                    #D[word] = 1
            else:
                break    
        ##########################################
        #x.append(feature_for_this_tweet)
        T.append(feature_for_this_tweet)
        temp2 = clf.predict(T)
        temp.append(temp2[0])
        y.append(tweet[0])
        
        
print "Predicting"
#print "Number of Emoticons in testing: " + str(no_of_emoticons)
#temp =  clf.predict(T)
correctPredicted = 0
negativePredictedPositive = 0
positivePredictedNegative = 0
for i in range(0,len(temp)):
    #print str(y[i]) + "," + str(temp[i])
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
print "Accuracy: " + str(float(correctPredicted) / float(len(temp)))
print "Done"



T = []
y = []
tweets_list = []
training = 'chunk11.csv'
with open(training, 'r') as csvfile:
    tweets = csv.reader(csvfile, delimiter=",")
    i=0
    for tweet in tweets:
        i = i +1
        if(i%100000 == 0):
        #    break
            print i
        # Initialise array with number of features
        feature_for_this_tweet = [0] * num_of_features
        tt = removeAtTheRate(tweet[1])
        tt = tt.lower()
        # for emoticon in emoticons:
        #     if(tt.find(emoticon) != -1):
        #         if emoticon in dict_of_features:
        #             feature_for_this_tweet[dict_of_features[emoticon]] = 1
        #tweets_list.append(tt)
        #D = dict()
        ############################################
        # Check what features are present in the tweet
        ###########################################
        while(True):
            match = re.search(r'([A-Za-z\']+)', tt)
            if match :                
                start = match.start()
                end = match.end()
                word = tt[start:end]
                tt = tt[0:start] + tt[end:]
                if word in dict_of_features:
                    #print word + " " + str(dict_of_features[word])
                    feature_for_this_tweet[dict_of_features[word]] = 1
                    #D[word] = 1
            else:
                break    
        ##########################################
        #x.append(feature_for_this_tweet)
        T.append(feature_for_this_tweet)
        y.append(tweet[0])
        
print "Predicting"
temp =  clf.predict(T)
correctPredicted = 0
negativePredictedPositive = 0
positivePredictedNegative = 0
for i in range(0,len(temp)):
    #print str(y[i]) + "," + str(temp[i])
    if(y[i] == temp[i]):
        correctPredicted = correctPredicted+1
    elif(y[i] == 0):
        negativePredictedPositive = negativePredictedPositive +1
        #print tweets_list[i]
    else:
        positivePredictedNegative = positivePredictedNegative +1
        #print tweets_list[i]
            
print "Correct Predicted: " + str(correctPredicted)
print "negativePredictedPositive: " + str(negativePredictedPositive)
print "positivePredictedNegative: " + str(positivePredictedNegative)
print "Total: " + str(len(temp))
print "Done"