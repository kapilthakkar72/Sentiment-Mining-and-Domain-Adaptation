from sets import Set
import csv
import re
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from sklearn.externals import joblib
import pickle
  
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

primary_feature_list_file_path = "kt"
primary_feature_list = []
for feature in open(primary_feature_list_file_path,'r'):
    primary_feature_list.append(feature.strip())

hillary_primary_features = []    
primary_feature_list_file_path = "TwitterWordsOfHillary"
for feature in open(primary_feature_list_file_path,'r'):
	if(len(feature.strip()) > 1):
		hillary_primary_features.append(feature.strip())

feature_dict  = dict()
i = 0
for element in primary_feature_list:
    feature_dict[element] = i
    i=i+1
print i
hillary_primary_features_dict  = Set()
for element in hillary_primary_features:
    hillary_primary_features_dict.add(element)

print "Starting"

f = open('General_Classifier.pickle', 'rb')
general_classifier = pickle.load(f)
f.close()

x_dict= []
y = []

i= 0 
tweets_path = 'training80.csv'
with open(tweets_path, 'r') as csvfile:
    tweets = csv.reader(csvfile, delimiter=",")
    for tweet in tweets:
        i = i+1
        if(i % 100000 == 0):
            print i
        tt = removeAtTheRate(tweet[1])
        tt = tt.lower()
        D = dict()
        tt2 = tt
        # Lets make prediction from General classifier as feature
        T = []
        features_exist = False
        feature_vector = [0] * len(primary_feature_list)
        while(True):
            match = re.search(r'([A-Za-z\']+)', tt2)
            if match :                
                start = match.start()
                end = match.end()
                word = tt2[start:end]
                tt2 = tt2[0:start] + tt2[end:]
                if word in feature_dict:
                    feature_vector[feature_dict[word]] = 1
                    features_exist = True
            else:
                break
        # Make Prediction
        T.append(feature_vector)
        prediction =  general_classifier.predict(T)
        prediction = prediction[0]
        while(True):
            match = re.search(r'([A-Za-z\']+)', tt)
            if match :                
                start = match.start()
                end = match.end()
                hashtag = False
                names = False
                word = tt[start:end]        
                tt = tt[0:start] + tt[end:]
                if word in hillary_primary_features_dict:
                    D[word] = 1
            else:
                break    
        if(len(D) == 0):
            continue
        elif(features_exist == True):
            D['old_prediction'] = prediction
        elif(features_exist == False):
            D['old_prediction'] = 2
        x_dict.append(D)
        #y.append(int(tweet[0]))
        y.append(tweet[0])


from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn import svm

clf = LogisticRegression()
#clf = svm.LinearSVC()
v = DictVectorizer(sparse=True)
X = v.fit_transform(x_dict)
#print X
clf.fit(X, y)
f = open('Hillary.pickle','wb')


print "Done Training"

features = v.get_feature_names()
fo = open("ktPlusHillary", "w")
for feature in features:
    fo.write(feature + '\n')
fo.close()

pickle.dump(clf,f)
f.close()