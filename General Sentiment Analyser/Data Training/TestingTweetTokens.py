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
    
def tokenize(tt):
    tt = tt.lower()
    while(True):
        match = re.search(r'([A-Za-z\']+)', tt)
        if match :                
            start = match.start()
            end = match.end()
            word = tt[start:end]
            tt = tt[0:start] + tt[end:]
            print word
        else:
            break    
    pass

# tweet = "go watch &quot;paparazzi&quot; by lady gaga...it's a bit long...but...it's good.  "
# tokenize(tweet)

from nltk.corpus import stopwords
import csv
stop = stopwords.words('english')
with open('features_with_freq', 'r') as csvfile:
    features = csv.reader(csvfile, delimiter=",")
    for feature in features:
        word = feature[0]
        if(word not in stop):
            print word