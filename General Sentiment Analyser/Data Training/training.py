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

primary_feature_list_file_path = "filtered_features"
primary_feature_list = []
for feature in open(primary_feature_list_file_path,'r'):
    primary_feature_list.append(feature.strip())
    
primary_feature_list_file_path = "temp1"
for feature in open(primary_feature_list_file_path,'r'):
	if(len(feature.strip()) > 1):
		primary_feature_list.append(feature.strip())
    
verb_file_path = "verbs"
base_verb = []
other_forms = []
for verb in open(verb_file_path,'r'):
    splitted = verb.split()
    base_verb.append(splitted[1].strip())
    other_forms.append((splitted[2].strip(),splitted[3].strip(),splitted[4].strip(),splitted[5].strip()))
    
# Ceating map
dict_of_features = Set()
i = 0
for feature in primary_feature_list:
    try:
        c = base_verb.index(feature)
    except ValueError:
        dict_of_features.add(feature)
        i = i+1
    else:
        dict_of_features.add(feature)
        dict_of_features.add(other_forms[c][0])
        dict_of_features.add(other_forms[c][1])
        dict_of_features.add(other_forms[c][2])
        dict_of_features.add(other_forms[c][3])
        i = i+1

feature_dict  = dict()
i = 0
for element in dict_of_features:
    feature_dict[element] = i
    # print element
    i= i+1

tweets_path = 'training.csv'
x_dict= []
y = []
with open(tweets_path, 'r') as csvfile:
    tweets = csv.reader(csvfile, delimiter=",")
    for tweet in tweets:
        tt = removeAtTheRate(tweet[1])
        tt = tt.lower()
        D = dict()
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
        if(len(D) == 0):
            continue
        x_dict.append(D)
        y.append(int(tweet[0]))
        #print tweet[0]

#save_model('svm.model', m)
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn import svm

clf = LogisticRegression()

v = DictVectorizer(sparse=True)

X = v.fit_transform(x_dict)
#print X
clf.fit(X, y)

f = open('General_Classifier.pickle','wb')

features = v.get_feature_names()
for feature in features:
	print feature
pickle.dump(clf,f)