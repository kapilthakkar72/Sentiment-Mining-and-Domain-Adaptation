from sets import Set
import csv
import re
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from sklearn.externals import joblib
import sys
import pickle

###################################################
##########  Some Utility Functions    #############
###################################################

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
        #return re.sub(r"(.)\1+",r"\1",s) # To replce loooveee : love
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

#######################################################################
#######################################################################

# Getting input and output file names
input_file = sys.argv[1]
# output_file = sys.argv[2]

# Load SVM
# clf = svm.LinearSVC()
# clf = joblib.load('svm.pkl')

f = open('lr.pickle', 'rb')
clf = pickle.load(f)

# Load Feaature List
# Primay Feature List
primary_feature_list_file_path = "kt"
primary_feature_list = dict()
i = 0
for feature in open(primary_feature_list_file_path,'r'):
    if(len(feature)<1):
        continue
    primary_feature_list[feature.strip()] = i
    i= i+1
num_of_features = len(primary_feature_list)    

# Read Input file line by line and predict
for tweet in open(input_file,'r'):
    T = []
    # Initialise array with number of features
    feature_for_this_tweet = [0] * num_of_features
    tt = removeAtTheRate(tweet)
    tt = tt.lower()
    #print "Tweet:" + tt
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
            if word in primary_feature_list:
                #print "present"
                feature_for_this_tweet[primary_feature_list[word]] = 1
        else:
            break
    # Use trained Model to print output
    T.append(feature_for_this_tweet)
    #print T
    temp =  clf.predict(T)
    print temp[0]

