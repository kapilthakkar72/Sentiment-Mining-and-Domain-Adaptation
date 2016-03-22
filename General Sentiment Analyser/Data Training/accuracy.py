T = []
y = []

import csv

training = 'testing20.csv'
with open(training, 'r') as csvfile:
    tweets = csv.reader(csvfile, delimiter=",")
    for tweet in tweets:
        y.append(int(tweet[0]))


training = 'testing10.csv'
with open(training, 'r') as csvfile:
    tweets = csv.reader(csvfile, delimiter=",")
    for tweet in tweets:
        y.append(int(tweet[0]))

op = "sample_output.txt"
temp = []
for feature in open(op,'r'):
    temp.append(int(feature.strip()))
        
correctPredicted = 0
negativePredictedPositive = 0
positivePredictedNegative = 0
for i in range(0,len(temp)):
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


print str(float(correctPredicted)/3200.0)
