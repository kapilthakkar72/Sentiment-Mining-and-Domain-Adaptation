verbs = open('F:\\IIT Delhi\\Semester 4\\Natural Language Processing\\Assignment\\rudraksh\\verbs', 'r')
filtered = open('F:\\IIT Delhi\\Semester 4\\Natural Language Processing\\Assignment\\rudraksh\\filtered_features', 'r')

fil = []
for line in filtered:
    # print line
    fil.append(line[0:len(line)-1])
    
base_verb = []
other_forms = []

for verb in verbs:
    #print verb
    verb = verb[0:len(verb)-1]
    splitted = verb.split()
    #print splitted
    base_verb.append(splitted[1])
    other_forms.append((splitted[2],splitted[3],splitted[4],splitted[5]))

extra_forms = []

# Adding other forms
for feature in fil:
    #print feature
    try:
        c = base_verb.index(feature)
    except ValueError:
        if(feature == "thank"):
            print "Not #found"
        pass
    else:

        extra_forms.append(other_forms[c][0])
        extra_forms.append(other_forms[c][1])
        extra_forms.append(other_forms[c][2])
        extra_forms.append(other_forms[c][3])
        
from sets import Set
features = Set()
for feature in fil:
    features.add(feature)
for ef in extra_forms:
    features.add(ef)
    
for feature in features:
    print feature
