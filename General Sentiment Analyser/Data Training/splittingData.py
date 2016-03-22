import csv

tweets_path = 'F:\\IIT Delhi\\Semester 4\\Natural Language Processing\\Assignment\\training.csv'
new_tweets_path = 'F:\\IIT Delhi\\Semester 4\\Natural Language Processing\\Assignment\\train80.csv'
testing_path = 'F:\\IIT Delhi\\Semester 4\\Natural Language Processing\\Assignment\\testing20.csv'

file1 = open(tweets_path, 'r')
file2 = open(new_tweets_path, 'w')
file3 = open(testing_path, 'w')
i=1
for line in file1:
    #print line
    if(i<=640000 or (i>800000 and i<=1440000)):
        file2.write(line)
    else:
        file3.write(line)
    i = i+1
file1.close()
file2.close()

print "Done"