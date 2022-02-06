import networkx as nx
import numpy as np
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from matplotlib import collections
import collections

# Import database and create the graph
dataBase = open("bit3.txt", "r")
Lines = dataBase.readlines()
AllUsers = nx.DiGraph()
for line in range(0, 24186):
    (x, y, z) = Lines[line].split("\t")
    x = int(x)
    y = int(y)
    z = int(z)
    # print(x,y,z)
    AllUsers.add_nodes_from([x, y])
    AllUsers.add_edge(x, y, weight=z)
# for (x, y, z) in AllUsers.edges.data('weight'):

allNodes = list(AllUsers.nodes)  # List of all nodes
allEdges = list(AllUsers.edges)  # List of all edges

print("The num of nodes: ", nx.number_of_nodes(AllUsers))
print("The num of edges:", nx.number_of_edges(AllUsers))
nx.draw(AllUsers, with_labels=False)
plt.show()

############################### Distributions ###########################################

# Distribution of weights on edges
listOfW = []
weightD = AllUsers.edges.data("weight")
# print(weightD)
[listOfW.append(item[2]) for item in weightD]
weightCount = collections.Counter(listOfW)
weg, countD = zip(*weightCount.items())
# print(weg, countD)
fig, ax = plt.subplots()
plt.bar(weg, countD, width=0.30, color="#9BCD9B")
plt.title("Weight Distribution")
plt.ylabel("Count")
plt.xlabel("weight")
plt.xscale("linear")
plt.yscale("log")
plt.show()

# Degree Distribution
DegreeSequence = sorted([d for n, d in AllUsers.degree()], reverse=True)
degreeCount = collections.Counter(DegreeSequence)
deg, countD = zip(*degreeCount.items())
# print("deg", deg)
# print("count", countD)
fig, ax = plt.subplots()
plt.bar(deg, countD, width=0.50, color="#9BCD9B")
plt.title("Degree Distribution")
plt.ylabel("Count")
plt.xlabel("Degree")
plt.xscale("log")
plt.yscale("log")
plt.show()

# In-Degree Distribution
inDegreeSequence = sorted([d for n, d in AllUsers.in_degree()], reverse=True)
degreeCount = collections.Counter(inDegreeSequence)
deg, countD = zip(*degreeCount.items())
fig, ax = plt.subplots()
plt.bar(deg, countD, width=0.30, color="#9BCD9B")
plt.title("in-Degree Distribution")
plt.ylabel("Count")
plt.xlabel("Degree")
plt.xscale("log")
plt.yscale("log")
plt.show()

# Out-Degree Distribution
outDegreeSequence = sorted([d for n, d in AllUsers.out_degree()], reverse=True)
degreeCount = collections.Counter(outDegreeSequence)
deg, countD = zip(*degreeCount.items())
fig, ax = plt.subplots()
plt.bar(deg, countD, width=0.30, color="#9BCD9B")
plt.title("out-Degree Distribution")
plt.ylabel("Count")
plt.xlabel("Degree")
plt.xscale("log")
plt.yscale("log")
plt.show()

################################### AllUsers Graph #######################################
# Reputation = (each rating * the number of users rated in the same rating) \ the number of ratings
# Calculate the reputation of each node
listW = AllUsers.edges.data("weight")
for i in AllUsers:
    numOfRate = AllUsers.in_degree(i)
    listWi = []
    [listWi.append(item[2]) for item in listW if item[1] == i]
    degreeCount = collections.Counter(listWi)
    sumD = 0
    for key, value in degreeCount.items():
        sumD += key * value
    if numOfRate == 0:
        AllUsers.nodes[i]['reputation'] = 0
    else:
        AllUsers.nodes[i]['reputation'] = sumD / numOfRate

# Calculate the average reputation of the network
sum = 0
for i in AllUsers.nodes:
    sum = sum + AllUsers.nodes[i]['reputation']
print("memu", sum/3783)

cheater = []
moniCheaterBefore = []
reliable = []
moniReliableBefore = []
# Check how many are reliable
# Check how many cheaters there are

for i in AllUsers:
    if AllUsers.nodes[i]['reputation'] < 0:
        mon = AllUsers.nodes[i]['reputation']
        cheater.append(i)
        moniCheaterBefore.append(mon)
    if AllUsers.nodes[i]['reputation'] > 0:
        mon = AllUsers.nodes[i]['reputation']
        reliable.append(i)
        moniReliableBefore.append(mon)

# list of tuples of cheater nodes and its reputation
cheaterMon = list(zip(cheater, moniCheaterBefore))
stateCheaterBefore = sorted(sorted(((key, value) for (key, value) in cheaterMon), reverse=True))

# list of tuples of reliable nodes and its reputation
reliableMon = list(zip(reliable, moniReliableBefore))
stateBeforeReliable = sorted(sorted(((key, value) for (key, value) in reliableMon), reverse=True))

# plot a graph of reliable and cheater nodes

print("num of reliable", len(reliable))
print("num of cheater", len(cheater))

nodes_color = []
for i in AllUsers:
    if i in reliable:
        nodes_color.append('#0000ff')  # כחול
    elif i in cheater:
        nodes_color.append('#ff0000')  # אדום
    else:  # reputation==0
        nodes_color.append('grey')  # אפור
# nx.draw(AllUsers, node_color=nodes_color,node_size=20,with_labels=False,edge_color='black',width=0.2)
# plt.show()

# Reputation distribution
listM = []
for i in AllUsers:
    listM.append(AllUsers.nodes[i]['reputation'])
reputationCount = collections.Counter(listM)
rep, countD = zip(*reputationCount.items())
print(rep, countD)
fig, ax = plt.subplots()
plt.bar(rep, countD, width=0.1, color="#9BCD9B")
plt.title("Reputation Distribution")
plt.ylabel("Count")
plt.xlabel("reputation")
plt.xscale("linear")
plt.yscale("log")
# plt.show()

# Finding the TOP 50 by the highest in_degree
nodeAndDegree = AllUsers.in_degree()
findTheTopFifty = sorted(((value, key) for (key, value) in nodeAndDegree), reverse=True)
weightD = AllUsers.edges.data("weight")
print("weightD", weightD)
print("The top 50 popular:")

topFifty = []
topFiftyMon = []
for i in range(0, 100):
    if AllUsers.nodes[findTheTopFifty[i][1]]['reputation'] > 0:
        topFifty.append(findTheTopFifty[i][1])
        topFiftyMon.append(AllUsers.nodes[findTheTopFifty[i][1]]['reputation'])
    if len(topFifty) == 50:
        break

monOfTopFiftyBefore = list(zip(topFifty, topFiftyMon))  # (node, monB)
print("monOfTopFiftyBefore", len(monOfTopFiftyBefore), monOfTopFiftyBefore)

# Finding the Liars: Those who voted for the TOP 50 rate <0
liars = []

[liars.append(item[0]) for item in weightD
 if item[0] not in topFifty
 if item[1] in topFifty and
 item[2] < 0]

liars = list(dict.fromkeys(liars))

print("num of liars", len(liars), liars)
print("num of reliable", len(reliable))
print("num of cheater", len(cheater))

# Drawing of the graph with an emphasis on liars
node_size = []
nodes_color = []
for i in AllUsers:
    if i in liars:
        nodes_color.append('orange')  # שקרנים בכתום
        node_size.append(150)
    elif i in reliable:
        nodes_color.append('#0000ff')  # אמינים בכחול
        node_size.append(10)
    elif i in cheater:
        nodes_color.append('#ff0000')  # רמאים באדום
        node_size.append(10)
    else:
        nodes_color.append('grey')  # ניטרלים באפור
        node_size.append(20)
nx.draw(AllUsers, node_color=nodes_color,node_size=node_size,with_labels=False,edge_color='black', width=0.1)
plt.show()

############################### AllNoLiars Graph ##############################################

# Create a sub-graph - take down the liars and create a new one
noLiars = [k for k in allNodes if k not in liars]
AllNoLiars = AllUsers.subgraph(noLiars)
print("The num of nodes:", nx.number_of_nodes(AllNoLiars))
print("The num of edges:", nx.number_of_edges(AllNoLiars))

# Calculate the reputation of each node
listW = AllNoLiars.edges.data("weight")
for i in AllNoLiars:
    numOfRate = AllNoLiars.in_degree(i)
    listWi = []
    [listWi.append(item[2]) for item in listW if item[1] == i]
    degreeCount = collections.Counter(listWi)
    sumD = 0
    for key, value in degreeCount.items():
        sumD += key * value
    if numOfRate == 0:
        AllNoLiars.nodes[i]['reputation'] = 0
    else:
        AllNoLiars.nodes[i]['reputation'] = sumD / numOfRate


# Calculate the average reputation of the network
sum = 0
for i in AllNoLiars.nodes:
    sum = sum + AllNoLiars.nodes[i]['reputation']
print("memu", sum/3687)

# For the TOP 50 we check the reputation
newFifty = []
monFiftyAfter1 = []
for i in range(0, 50):
    if topFifty[i] not in liars:
        newFifty.append(topFifty[i])
        monFiftyAfter1.append(AllNoLiars.nodes[topFifty[i]]['reputation'])

monOfTopFiftyAfter1 = list(zip(newFifty, monFiftyAfter1))
print("monOfTopFiftyAfter1", len(monOfTopFiftyAfter1), monOfTopFiftyAfter1)

# Comparison between reputation before and reputation of TOP 50 after removing liars

x1 = [item[0] for item in monOfTopFiftyBefore]
x2 = [item[0] for item in monOfTopFiftyAfter1]
y1 = [item[1] for item in monOfTopFiftyBefore]
y2 = [item[1] for item in monOfTopFiftyAfter1]

fig, ax1 = plt.subplots()

# Draw a simple arrow between two points in axes coordinates
# within a single axes.
for i in range(0, len(x1)):
    xyA = (x1[i], y1[i])
    xyB = (x2[i], y2[i])
    coordsA = "data"
    coordsB = "data"
    con = ConnectionPatch(xyA, xyB, coordsA, coordsB,
                          arrowstyle='-|>', shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc="w")
    ax1.plot([xyA[0], xyB[0]], [xyA[1], xyB[1]], "o")
    ax1.add_artist(con)
plt.show()

cheaterAfter = []
moniCheaterAfter = []
reliableAfter = []
moniReliableAfter = []

# Check how many are reliable
# Check how many cheaters there are
for i in AllNoLiars:
    if AllNoLiars.nodes[i]['reputation'] < 0:
        monn = AllNoLiars.nodes[i]['reputation']
        cheaterAfter.append(i)
        moniCheaterAfter.append(monn)
    if AllNoLiars.nodes[i]['reputation'] > 0:
        monn = AllNoLiars.nodes[i]['reputation']
        reliableAfter.append(i)
        moniReliableAfter.append(monn)

# list of tuples of cheater nodes and its reputation
cheaterMonA = list(zip(cheaterAfter, moniCheaterAfter))
stateAfterCheater = sorted(sorted(((key, value) for (key, value) in cheaterMonA), reverse=True))

# list of tuples of reliable nodes and its reputation
reliableMonA = list(zip(reliableAfter, moniReliableAfter))
stateAfterReliable = sorted(sorted(((key, value) for (key, value) in reliableMonA), reverse=True))

print("cheaterAfter:", len(cheaterAfter))
print("reliableAfter:", len(reliableAfter))

# plot a graph of reliable and cheater nodes
nodes_color = []
for i in AllNoLiars:
    if i in reliableAfter:
        nodes_color.append('#0000ff')  # אמינים בכחול
    elif i in cheaterAfter:
        nodes_color.append('#ff0000')  # רמאים באדום
    else:
        nodes_color.append('grey')  # ניטרלים באפור
# nx.draw(AllNoLiars, node_color=nodes_color,node_size=20,with_labels=False,edge_color='black', width=0.2)
# plt.show()

############################################################################################
# After removing the liars we have 4 types of users we would like to look at:

# Type 1 : Were cheaters and still cheaters

# Finding those who remained cheaters
stayCheater = []
for item in stateCheaterBefore:  # לקודקודים יש את המוניטין של לפני
    if item[0] in cheaterAfter:
        stayCheater.append(item)

stayCheaterKey = [i[0] for i in stayCheater]

# List of new reputations
monAfterStayCheater = []
for i in stayCheaterKey:
    monAfterStayCheater.append(AllNoLiars.nodes[i]['reputation'])

# list of tuple [(node,reputation before, reputation after)...]
repOfStayCheater = [stayCheater[i] + (monAfterStayCheater[i],) for i in range(len(stayCheater))]
print("repOfStayCheater", len(repOfStayCheater), repOfStayCheater)

# Type 2: Were reliable and became cheaters

# Finding those who became cheaters
becomeCheater = [i for i in stateAfterCheater if  # לקודקודים יש את המוניטין של אחרי
                 i[0] in reliable]

becomeCheaterKey = [i[0] for i in becomeCheater]

# List of new reputations
moniAfterBecomeCheater = []
for i in becomeCheaterKey:
    for j in stateBeforeReliable:
        if i == j[0]:
            moniAfterBecomeCheater.append(j[1])

# list of tuple [(node,reputation after, reputation before )...]
repOfBecomeCheater = [becomeCheater[i] + (moniAfterBecomeCheater[i],) for i in range(len(becomeCheater))]
print("repOfBecomeCheater", len(repOfBecomeCheater), repOfBecomeCheater)

# Type 3: Were cheaters and became reliable

# Finding those who became reliable
becomeReliable = [i for i in stateCheaterBefore if  # לקודקודים יש את המוניטין של לפני
                  i[0] not in cheaterAfter and
                  i[0] not in liars]  # מי שהיה לא אמין לפני ואחרי הורדת השקרנים הפך לאמין

becomeReliableKey = [i[0] for i in becomeReliable]

# List of new reputations
moniAfterBecomeReliable = []
for i in becomeReliableKey:
    moniAfterBecomeReliable.append(AllNoLiars.nodes[i]['reputation'])

# list of tuple [(node,reputation before, reputation after)...]
repOfBecomeReliable = [becomeReliable[i] + (moniAfterBecomeReliable[i],) for i in range(len(becomeReliable))]
print("repOfBecomeReliable", len(repOfBecomeReliable), repOfBecomeReliable)

# Type 4 : Were reliable and still reliable

# Finding those who stay reliable
stayReliable = []
for item in stateBeforeReliable:
    if item[0] in reliableAfter and item[0] not in newFifty:
        stayReliable.append(item)  # לכל קודקוד יש את המוניטין של לפני

stayReliableKey = [i[0] for i in stayReliable]

# List of new reputations
monAfterStayReliable = []
for i in stayReliableKey:
    monAfterStayReliable.append(AllNoLiars.nodes[i]['reputation'])

# list of tuple [(node,reputation before, reputation after)...]
repOfStayReliable = [stayReliable[i] + (monAfterStayReliable[i],) for i in range(len(stayReliable))]
print("repOfStayReliable", len(repOfStayReliable), repOfStayReliable)

# Comparisons between pre-reputation and post-reputation for each type of user

# Type 1 : Were Cheater and still Cheater

x1 = [item[0] for item in repOfStayCheater]
x2 = [item[0] for item in repOfStayCheater]
y1 = [item[1] for item in repOfStayCheater]
y2 = [item[2] for item in repOfStayCheater]

fig, ax1 = plt.subplots()

# Draw a simple arrow between two points in axes coordinates
# within a single axes.
for i in range(0, len(x1)):
    xyA = (x1[i], y1[i])
    xyB = (x2[i], y2[i])
    coordsA = "data"
    coordsB = "data"
    con = ConnectionPatch(xyA, xyB, coordsA, coordsB,
                          arrowstyle='-|>', shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc="w")
    ax1.plot([xyA[0], xyB[0]], [xyA[1], xyB[1]], "o")
    ax1.add_artist(con)

plt.show()

# Type 2: Were reliable and became cheaters

x1 = [item[0] for item in repOfBecomeCheater]
x2 = [item[0] for item in repOfBecomeCheater]
y1 = [item[2] for item in repOfBecomeCheater]
y2 = [item[1] for item in repOfBecomeCheater]

fig, ax1 = plt.subplots()

# Draw a simple arrow between two points in axes coordinates
# within a single axes.
for i in range(0, len(x1)):
    xyA = (x1[i], y1[i])
    xyB = (x2[i], y2[i])
    coordsA = "data"
    coordsB = "data"
    con = ConnectionPatch(xyA, xyB, coordsA, coordsB,
                          arrowstyle='-|>', shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc="w")
    ax1.plot([xyA[0], xyB[0]], [xyA[1], xyB[1]], "o")
    ax1.add_artist(con)

plt.show()

# Type 3: Were cheaters and became reliable

x1 = [item[0] for item in repOfBecomeReliable]
x2 = [item[0] for item in repOfBecomeReliable]
y1 = [item[1] for item in repOfBecomeReliable]
y2 = [item[2] for item in repOfBecomeReliable]

fig, ax1 = plt.subplots()

# Draw a simple arrow between two points in axes coordinates
# within a single axes.
for i in range(0, len(x1)):
    xyA = (x1[i], y1[i])
    xyB = (x2[i], y2[i])
    coordsA = "data"
    coordsB = "data"
    con = ConnectionPatch(xyA, xyB, coordsA, coordsB,
                          arrowstyle='-|>', shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc="w")
    ax1.plot([xyA[0], xyB[0]], [xyA[1], xyB[1]], "o")
    ax1.add_artist(con)

plt.show()

# Type 4 : Were reliable and still reliable

x1 = [item[0] for item in repOfStayReliable]
x2 = [item[0] for item in repOfStayReliable]
y1 = [item[1] for item in repOfStayReliable]
y2 = [item[2] for item in repOfStayReliable]

fig, ax1 = plt.subplots()

# Draw a simple arrow between two points in axes coordinates
# within a single axes.
for i in range(0, len(x1)):
    xyA = (x1[i], y1[i])
    xyB = (x2[i], y2[i])
    coordsA = "data"
    coordsB = "data"
    con = ConnectionPatch(xyA, xyB, coordsA, coordsB,
                          arrowstyle='-|>', shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc="w")
    ax1.plot([xyA[0], xyB[0]], [xyA[1], xyB[1]], "o")
    ax1.add_artist(con)

plt.show()

################################ Calculating the gap ###########################################
# calculate the gap that exists between reputation before and reputation
# for each type of user


# Type 1 : Were Cheater and still Cheater

gap = []
repChange = []
for i in repOfStayCheater:
    b = i[1]  # -8
    a = i[2]  # -1
    # y=0
    if b > a:  # decreased
        gapp = a - b  # (-8--1=-7)
        repChange.append(-1)
    elif b < a:  # increased
        gapp = -(b - a)  # (-(-8-(-1))=7)
        repChange.append(1)
    else:  # a=b
        gapp = 0  # not changed
        repChange.append(0)
    gap.append(gapp)

monChangeCount = collections.Counter(repChange)
gapi, countD = zip(*monChangeCount.items())
print(gapi, countD)
fig, ax = plt.subplots()
plt.bar(gapi, countD, width=0.05, color="#9BCD9B")
plt.title("Gap Distribution")
plt.ylabel("Count")
plt.xlabel("Gap")
plt.xscale("linear")
plt.yscale("linear")
plt.show()

# Add the gap to the tuple
repOfStayCheater = [repOfStayCheater[i] + (gap[i],) for i in range(len(repOfStayCheater))]
print("repOfStayCheater", len(repOfStayCheater), repOfStayCheater)

# Sort by the gap
repOfStayCheater.sort(key=lambda item: item[3])
print("repOfStayCheater sorted", repOfStayCheater)

# Type 2: Were reliable and became cheaters

gap = []
for i in repOfBecomeCheater:
    b = i[2]  # 5
    a = i[1]  # -6
    if b > a:  # decreased
        gapp = -(b - a)
    gap.append(gapp)

monChangeCount = collections.Counter(gap)
gapi, countD = zip(*monChangeCount.items())
print(gapi, countD)
fig, ax = plt.subplots()
plt.bar(gapi, countD, width=0.05, color="#9BCD9B")
plt.title("Gap Distribution")
plt.ylabel("Count")
plt.xlabel("Gap")
plt.xscale("linear")
plt.yscale("linear")
plt.show()

# Add the gap to the tuple
repOfBecomeCheater = [repOfBecomeCheater[i] + (gap[i],) for i in range(len(repOfBecomeCheater))]
print("repOfBecomeCheater", len(repOfBecomeCheater), repOfBecomeCheater)

# Sort by the gap
repOfBecomeCheater.sort(key=lambda item: item[3])
print("repOfBecomeCheater sorted", repOfBecomeCheater)

# Type 3: Were cheaters and became reliable

gap = []
for i in repOfBecomeReliable:
    b = i[1]  # -1
    a = i[2]  # 9
    if b < a:  # increased
        gapp = a - b
    gap.append(gapp)

monChangeCount = collections.Counter(gap)
gapi, countD = zip(*monChangeCount.items())
print(gapi, countD)
fig, ax = plt.subplots()
plt.bar(gapi, countD, width=0.1, color="#9BCD9B")
plt.title("Gap Distribution")
plt.ylabel("Count")
plt.xlabel("Gap")
plt.xscale("linear")
plt.yscale("linear")
plt.show()

# Add the gap to the tuple
repOfBecomeReliable = [repOfBecomeReliable[i] + (gap[i],) for i in range(len(repOfBecomeReliable))]
print("repOfBecomeReliable", len(repOfBecomeReliable), repOfBecomeReliable)

# Sort by the gap
repOfBecomeReliable.sort(key=lambda item: item[3], reverse=True)
print("repOfBecomeReliable sorted", repOfBecomeReliable)

# Type 4 : Were reliable and still reliable

gap = []
repChange = []
for i in repOfStayReliable:
    b = i[1]  # -8
    a = i[2]  # -1
    y = 0
    if b > a:  # decreased
        gapp = a - b  # (-8--1=-7)
        repChange.append(-1)
    elif b < a:  # increased
        gapp = -(b - a)  # (-(-8-(-1))=7)
        repChange.append(1)
    else:  # a=b
        gapp = 0  # not changed
        repChange.append(0)
    gap.append(gapp)

monChangeCount = collections.Counter(repChange)
gapi, countD = zip(*monChangeCount.items())
print(gapi, countD)
fig, ax = plt.subplots()
plt.bar(gapi, countD, width=0.05, color="#9BCD9B")
plt.title("Gap Distribution")
plt.ylabel("Count")
plt.xlabel("Gap")
plt.xscale("linear")
plt.yscale("linear")
plt.show()

# Add the gap to the tuple

repOfStayReliable = [repOfStayReliable[i] + (gap[i],) for i in range(len(repOfStayReliable))]
print("repOfStayReliable", len(repOfStayReliable), repOfStayReliable)

# Sort by the gap
repOfStayReliable.sort(key=lambda item: item[3])
print("repOfStayReliable sorted", repOfStayReliable)

########################## Finding more liars ##################################

# Any user whose reputation has dropped after downloading the liars -
# we conclude that the liars supported them and therefore are "suspicious as liars"
# So anyone whose reputation has dropped significantly
# we would like to remove it from the network
# as well and see its impact on the network,
# and we would like to check if he has voted for the TOP 50.

liarInBecomeCheater = [item[0] for item in weightD
                       if item[1] in newFifty and
                       item[0] in becomeCheaterKey]

liarInBecomeCheater = list(dict.fromkeys(liarInBecomeCheater))
print(len(liarInBecomeCheater), liarInBecomeCheater)

liarInStayCheater = []
j = 0
for item in weightD:
    if item[1] in newFifty and item[0] in stayCheaterKey:
        for j in range(0, len(stayCheaterKey)):
            if repOfStayCheater[j][0] == item[0] and repOfStayCheater[j][3] < 0:
                liarInStayCheater.append(item[0])

liarInStayCheater = list(dict.fromkeys(liarInStayCheater))
print(len(liarInStayCheater), liarInStayCheater)

newLiars = liarInStayCheater + liarInBecomeCheater

# Drawing of the graph with an emphasis on newliars

node_size = []
nodes_color = []
for i in AllNoLiars:
    if i in newLiars:
        nodes_color.append('orange')  # שקרנים בכתום
        node_size.append(150)
    elif i in reliableAfter:
        nodes_color.append('#0000ff')  # אמינים בכחול
        node_size.append(10)
    elif i in cheaterAfter:
        nodes_color.append('#ff0000')  # רמאים באדום
        node_size.append(10)
    else:
        nodes_color.append('grey')  # ניטרלים באפור
        node_size.append(20)
nx.draw(AllNoLiars, node_color=nodes_color,node_size=node_size,with_labels=False,edge_color='black', width=0.1)
plt.show()

############################## AllNoLiars2 Graph ##############################################

allNoLiarsNodes = list(AllNoLiars.nodes)
noLiars2 = [k for k in allNoLiarsNodes if k not in liarInBecomeCheater and k not in liarInStayCheater]
print("len", len(noLiars2))

AllNoLiars2 = AllNoLiars.subgraph(noLiars2)
print("The num of nodes: ", nx.number_of_nodes(AllNoLiars2))
print("The num of edges:", nx.number_of_edges(AllNoLiars2))

# Calculate the reputation of each node

listW2 = AllNoLiars2.edges.data("weight")
for i in AllNoLiars2:
    numOfRate = int(AllNoLiars2.in_degree(i))
    listWi = []
    [listWi.append(item[2]) for item in listW2 if item[1] == i]
    # print("i", listWi)
    degreeCount = collections.Counter(listWi)
    # print(degreeCount)
    sumD = 0
    for key, value in degreeCount.items():
        sumD += key * value
    if numOfRate == 0:
        AllNoLiars2.nodes[i]['reputation'] = 0
    else:
        AllNoLiars2.nodes[i]['reputation'] = sumD / numOfRate

# Calculate the average reputation of the network
sum = 0
for i in AllNoLiars2.nodes:
    sum = sum + AllNoLiars2.nodes[i]['reputation']
print("memu", sum/3674)


# For the TOP 50 we check the reputation
newFifty2 = []
monFiftyAfter2 = []

for i in range(0, 50):
    if newFifty[i] not in newLiars:
        newFifty2.append(newFifty[i])
        monFiftyAfter2.append(AllNoLiars2.nodes[newFifty[i]]['reputation'])

monOfTopFiftyAfter2 = list(zip(newFifty2, monFiftyAfter2))
print("monOfTopFiftyAfter2", len(monOfTopFiftyAfter2), monOfTopFiftyAfter2)

# Comparison between reputation before and reputation of TOP 50 after removing liars

x1 = [item[0] for item in monOfTopFiftyAfter1]
x2 = [item[0] for item in monOfTopFiftyAfter2]
y1 = [item[1] for item in monOfTopFiftyAfter1]
y2 = [item[1] for item in monOfTopFiftyAfter2]

fig, ax1 = plt.subplots()

# Draw a simple arrow between two points in axes coordinates
# within a single axes.
for i in range(0, len(x1)):
    xyA = (x1[i], y1[i])
    xyB = (x2[i], y2[i])
    coordsA = "data"
    coordsB = "data"
    con = ConnectionPatch(xyA, xyB, coordsA, coordsB,
                          arrowstyle='-|>', shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc="w")
    ax1.plot([xyA[0], xyB[0]], [xyA[1], xyB[1]], "o")
    ax1.add_artist(con)

plt.show()

cheaterAfter2 = []
moniCheaterAfter2 = []
reliableAfter2 = []
moniReliableAfter2 = []
# Check how many are reliable
# Check how many cheaters there are

for i in AllNoLiars2:
    if AllNoLiars2.nodes[i]['reputation'] < 0:
        monn = AllNoLiars2.nodes[i]['reputation']
        cheaterAfter2.append(i)
        moniCheaterAfter2.append(monn)
    if AllNoLiars2.nodes[i]['reputation'] > 0:
        monn = AllNoLiars2.nodes[i]['reputation']
        reliableAfter2.append(i)
        moniReliableAfter2.append(monn)

# list of tuples of cheater nodes and its reputation
cheaterMonA2 = list(zip(cheaterAfter2, moniCheaterAfter2))
stateAfterCheater2 = sorted(sorted(((key, value) for (key, value) in cheaterMonA2), reverse=True))

# list of tuples of reliable nodes and its reputation
reliableMonA2 = list(zip(reliableAfter2, moniReliableAfter2))
stateAfterReliable2 = sorted(sorted(((key, value) for (key, value) in reliableMonA2), reverse=True))

print("cheaterAfter 2:", len(cheaterAfter2))
print("reliableAfter 2:", len(reliableAfter2))

# plot a graph of reliable and cheater nodes
nodes_color = []
for i in AllNoLiars2:
    if i in reliableAfter2:
        nodes_color.append('#0000ff')  # אמינים בכחול
    elif i in cheaterAfter2:
        nodes_color.append('#ff0000')  # רמאים באדום
    else:
        nodes_color.append('grey')  # ניטרלים באפור
nx.draw(AllNoLiars2, node_color=nodes_color,node_size=20,with_labels=False,edge_color='black', width=0.2)
plt.show()

############################################################################################
# After removing the liars we have 4 types of users we would like to look at:
# Type 1 : Were unreliable and still unreliable

# Finding those who remained cheaters
stayCheater2 = []
for item in stateAfterCheater:  # לקודקודים יש את המוניטין של לפני
    if item[0] in cheaterAfter2:
        stayCheater2.append(item)

stayCheater2Key = [i[0] for i in stayCheater2]

# List of new reputations
monAfterStayCheater2 = []
for i in stayCheater2Key:
    monAfterStayCheater2.append(AllNoLiars2.nodes[i]['reputation'])

# list of tuple [(node,reputation before, reputation after)...]
repOfStayCheater2 = [stayCheater2[i] + (monAfterStayCheater2[i],) for i in range(len(stayCheater2))]
print("repOfStayCheater2", len(repOfStayCheater2), repOfStayCheater2)

# Type 2: Were reliable and became cheaters

# Finding those who became cheaters
becomeCheater2 = [i for i in stateAfterCheater2
                  if i[0] in reliableAfter] # לקודקודים יש את המוניטין של אחרי

becomeCheater2Key = [i[0] for i in becomeCheater2]

# List of new reputations
moniAfterBecomeCheater2 = []
for i in becomeCheater2Key:
    for j in stateAfterReliable:
        if i == j[0]:
            moniAfterBecomeCheater2.append(j[1])

# list of tuple [(node,reputation after, reputation before )...]
repOfBecomeCheater2 = [becomeCheater2[i] + (moniAfterBecomeCheater2[i],) for i in range(len(becomeCheater2))]
print("repOfBecomeCheater", len(repOfBecomeCheater2), repOfBecomeCheater2)

# Type 3: Were cheaters and became reliable

# Finding those who became reliable
becomeReliable2 = [i for i in stateAfterCheater if  # לקודקודים יש את המוניטין של לפני
                  i[0] not in cheaterAfter2 and
                  i[0] not in newLiars]  # מי שהיה לא אמין לפני ואחרי הורדת השקרנים הפך לאמין

becomeReliable2Key = [i[0] for i in becomeReliable2]

# List of new reputations
moniAfterBecomeReliable2 = []
for i in becomeReliable2Key:
    moniAfterBecomeReliable2.append(AllNoLiars2.nodes[i]['reputation'])

# list of tuple [(node,reputation before, reputation after)...]
repOfBecomeReliable2 = [becomeReliable2[i] + (moniAfterBecomeReliable2[i],) for i in range(len(becomeReliable2))]
print("repOfBecomeReliable 2", len(repOfBecomeReliable2), repOfBecomeReliable2)

# Type 4 : Were reliable and still reliable

# Finding those who stay reliable
stayReliable2 = []
for item in stateAfterReliable2:
    if item[0] in reliableAfter2 and item[0] not in newFifty2:
        stayReliable2.append(item)  # לכל קודקוד יש את המוניטין של לפני

stayReliable2Key = [i[0] for i in stayReliable2]

# List of new reputations
monAfterStayReliable2 = []
for i in stayReliable2Key:
    monAfterStayReliable2.append(AllNoLiars2.nodes[i]['reputation'])

# list of tuple [(node,reputation before, reputation after)...]
repOfStayReliable2 = [stayReliable2[i] + (monAfterStayReliable2[i],) for i in range(len(stayReliable2))]
print("repOfStayReliable", len(repOfStayReliable2), repOfStayReliable2)

# Comparisons between pre-reputation and post-reputation for each type of user

# Type 1 : Were Cheater and still Cheater

x1 = [item[0] for item in repOfStayCheater2]
x2 = [item[0] for item in repOfStayCheater2]
y1 = [item[1] for item in repOfStayCheater2]
y2 = [item[2] for item in repOfStayCheater2]

fig, ax1 = plt.subplots()

# Draw a simple arrow between two points in axes coordinates
# within a single axes.
for i in range(0, len(x1)):
    xyA = (x1[i], y1[i])
    xyB = (x2[i], y2[i])
    coordsA = "data"
    coordsB = "data"
    con = ConnectionPatch(xyA, xyB, coordsA, coordsB,
                          arrowstyle='-|>', shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc="w")
    ax1.plot([xyA[0], xyB[0]], [xyA[1], xyB[1]], "o")
    ax1.add_artist(con)

plt.show()

# Type 2: Were reliable and became cheaters

x1 = [item[0] for item in repOfBecomeCheater2]
x2 = [item[0] for item in repOfBecomeCheater2]
y1 = [item[2] for item in repOfBecomeCheater2]
y2 = [item[1] for item in repOfBecomeCheater2]

fig, ax1 = plt.subplots()

# Draw a simple arrow between two points in axes coordinates
# within a single axes.
for i in range(0, len(x1)):
    xyA = (x1[i], y1[i])
    xyB = (x2[i], y2[i])
    coordsA = "data"
    coordsB = "data"
    con = ConnectionPatch(xyA, xyB, coordsA, coordsB,
                          arrowstyle='-|>', shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc="w")
    ax1.plot([xyA[0], xyB[0]], [xyA[1], xyB[1]], "o")
    ax1.add_artist(con)

plt.show()

# Type 3: Were cheaters and became reliable

x1 = [item[0] for item in repOfBecomeReliable2]
x2 = [item[0] for item in repOfBecomeReliable2]
y1 = [item[1] for item in repOfBecomeReliable2]
y2 = [item[2] for item in repOfBecomeReliable2]

fig, ax1 = plt.subplots()

# Draw a simple arrow between two points in axes coordinates
# within a single axes.
for i in range(0, len(x1)):
    xyA = (x1[i], y1[i])
    xyB = (x2[i], y2[i])
    coordsA = "data"
    coordsB = "data"
    con = ConnectionPatch(xyA, xyB, coordsA, coordsB,
                          arrowstyle='-|>', shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc="w")
    ax1.plot([xyA[0], xyB[0]], [xyA[1], xyB[1]], "o")
    ax1.add_artist(con)

plt.show()

# Type 4 : Were reliable and still reliable

x1 = [item[0] for item in repOfStayReliable2]
x2 = [item[0] for item in repOfStayReliable2]
y1 = [item[1] for item in repOfStayReliable2]
y2 = [item[2] for item in repOfStayReliable2]

fig, ax1 = plt.subplots()

# Draw a simple arrow between two points in axes coordinates
# within a single axes.
for i in range(0, len(x1)):
    xyA = (x1[i], y1[i])
    xyB = (x2[i], y2[i])
    coordsA = "data"
    coordsB = "data"
    con = ConnectionPatch(xyA, xyB, coordsA, coordsB,
                          arrowstyle='-|>', shrinkA=5, shrinkB=5,
                          mutation_scale=20, fc="w")
    ax1.plot([xyA[0], xyB[0]], [xyA[1], xyB[1]], "o")
    ax1.add_artist(con)

plt.show()

########################## Calculating the gap for second time ###########################################
# calculate the gap that exists between reputation before and reputation
# for each type of user


# Type 1 : Were Cheater and still Cheater

gap = []
repChange = []
for i in repOfStayCheater2:
    b = i[1]  # -8
    a = i[2]  # -1
    # y=0
    if b > a:  # decreased
        gapp = a - b  # (-8--1=-7)
        repChange.append(-1)
    elif b < a:  # increased
        gapp = -(b - a)  # (-(-8-(-1))=7)
        repChange.append(1)
    else:  # a=b
        gapp = 0  # not changed
        repChange.append(0)
    gap.append(gapp)

monChangeCount = collections.Counter(repChange)
gapi, countD = zip(*monChangeCount.items())
print(gapi, countD)
fig, ax = plt.subplots()
plt.bar(gapi, countD, width=0.05, color="blue")
plt.title("Gap Distribution")
plt.ylabel("Count")
plt.xlabel("Gap")
plt.xscale("linear")
plt.yscale("linear")
plt.show()

# Add the gap to the tuple
repOfStayCheater2 = [repOfStayCheater2[i] + (gap[i],) for i in range(len(repOfStayCheater2))]
print("repOfStayCheater2", len(repOfStayCheater2), repOfStayCheater2)

# Sort by the gap
repOfStayCheater2.sort(key=lambda item: item[3])
print("repOfStayCheater2 sorted", repOfStayCheater2)

# Type 2: Were reliable and became cheaters

# gap = []
# for i in repOfBecomeCheater2:
#     b = i[2]  # 5
#     a = i[1]  # -6
#     if b > a:  # המוניטין קטן
#         gapp = -(b - a)
#     gap.append(gapp)
#
# monChangeCount = collections.Counter(gap)
# gapi, countD = zip(*monChangeCount.items())
# print(gapi, countD)
# fig, ax = plt.subplots()
# plt.bar(gapi, countD, width=0.05, color="blue")
# plt.title("Gap Distribution")
# plt.ylabel("Count")
# plt.xlabel("Gap")
# plt.xscale("linear")
# plt.yscale("linear")
# plt.show()
#
# # Add the gap to the tuple
# repOfBecomeCheater2 = [repOfBecomeCheater2[i] + (gap[i],) for i in range(len(repOfBecomeCheater2))]
# print("repOfBecomeCheater 2", len(repOfBecomeCheater2), repOfBecomeCheater2)
#
# # Sort by the gap
# repOfBecomeCheater2.sort(key=lambda item: item[3])
# print("repOfBecomeCheater2 sorted", repOfBecomeCheater2)

# Type 3: Were cheaters and became reliable
#
# gap = []
# for i in repOfBecomeReliable2:
#     b = i[1]  # -1
#     a = i[2]  # 9
#     if b < a:  # המוניטין גדל
#         gapp = a - b
#     gap.append(gapp)
#
# monChangeCount = collections.Counter(gap)
# gapi, countD = zip(*monChangeCount.items())
# print(gapi, countD)
# fig, ax = plt.subplots()
# plt.bar(gapi, countD, width=0.05, color="blue")
# plt.title("Gap Distribution")
# plt.ylabel("Count")
# plt.xlabel("Gap")
# plt.xscale("linear")
# plt.yscale("linear")
# plt.show()
#
# # Add the gap to the tuple
# repOfBecomeReliable2 = [repOfBecomeReliable2[i] + (gap[i],) for i in range(len(repOfBecomeReliable2))]
# print("repOfBecomeReliable2 ", len(repOfBecomeReliable2), repOfBecomeReliable2)
#
# # Sort by the gap
# repOfBecomeReliable2.sort(key=lambda item: item[3], reverse=True)
# print("repOfBecomeReliable2 sorted", repOfBecomeReliable2)


# Type 4 : Were reliable and still reliable
gap = []
repChange = []
for i in repOfStayReliable2:
    b = i[1]  # -8
    a = i[2]  # -1
    y = 0
    if b > a:  # decreased
        gapp = a - b  # (-8--1=-7)
        repChange.append(-1)
    elif b < a:  # increased
        gapp = -(b - a)  # (-(-8-(-1))=7)
        repChange.append(1)
    else:  # a=b
        gapp = 0  # not changed
        repChange.append(0)
    gap.append(gapp)

monChangeCount = collections.Counter(repChange)
gapi, countD = zip(*monChangeCount.items())
print(gapi, countD)
fig, ax = plt.subplots()
plt.bar(gapi, countD, width=0.05, color="blue")
plt.title("Gap Distribution")
plt.ylabel("Count")
plt.xlabel("Gap")
plt.xscale("linear")
plt.yscale("linear")
plt.show()

# Add the gap to the tuple

repOfStayReliable2 = [repOfStayReliable2[i] + (gap[i],) for i in range(len(repOfStayReliable2))]
print("repOfStayReliable2", len(repOfStayReliable2), repOfStayReliable2)

# Sort by the gap
repOfStayReliable2.sort(key=lambda item: item[3])
print("repOfStayReliable2 sorted", repOfStayReliable2)

