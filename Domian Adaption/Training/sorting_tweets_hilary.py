import csv

tweets_list = []

hilary = 'hilary.csv'
with open(hilary, 'r') as csvfile:
    tweets = csv.reader(csvfile, delimiter=",")
    for tweet in tweets:
        tweets_list.append((int(tweet[0]),tweet[1]))
        
# Sort
tweets_list.sort(key=lambda tup: tup[0])

# Write output to file
fo = open("hillary_arranged.csv", "w")
for tweet in tweets_list:
    fo.write('"' + str(tweet[0]) + '","' + tweet[1] + '"\n')
fo.close()
    
# Seperating out data for training as well as testing (80+20)
f1 = open("training80.csv", "w")
f2 = open("testing20Tweets.txt", "w")
f3 = open("testing20Outputs.txt", "w")

for i in range(0,182):
    f1.write('"' + str(tweets_list[i][0]) + '","' + tweets_list[i][1] + '"\n')
for i in range(182,228):
    f2.write(tweets_list[i][1] + "\n")
    f3.write(str(tweets_list[i][0]) + "\n")
    
for i in range(228,583):
    f1.write('"' + str(tweets_list[i][0]) + '","' + tweets_list[i][1] + '"\n')
for i in range(583,672):
    f2.write(tweets_list[i][1] + "\n")
    f3.write(str(tweets_list[i][0]) + "\n")
    
for i in range(672,1015):
    f1.write('"' + str(tweets_list[i][0]) + '","' + tweets_list[i][1] + '"\n')
for i in range(1015,1101):
    f2.write(tweets_list[i][1] + "\n")
    f3.write(str(tweets_list[i][0]) + "\n")

f1.close()
f2.close()
f3.close()