import SyntheticNetwork as sn
import os
import networkx as nx

''' Variables '''




''' Methods   '''
def findTrueNodeCount():
    while True:
        try:
            numberOfNodes = int(raw_input("Enter the number of nodes in the actual network being modeled."))
            break
        except ValueError:
            print "That was not an integer number, Please try again"
    return numberOfNodes

def findNodeCount():
    while True:
        try:
            numberOfNodes = int(raw_input("Enter the number of nodes in the desired synthetic network."))
            break
        except ValueError:
            print "That was not an integer number, Please try again"
    return numberOfNodes

def findCorePercent():
    while True:
        try:
            percentOfCore = float(
                raw_input("What percent of the core is the actual network you are modeling between 0 and 1?"))
            break
        except ValueError:
            print "That was not a percentage in the right format, try something like 0.53."
    return percentOfCore

def corePercentageCheck(percentage):
    if percentage >=1:
        print "The value entered is greater than 1. Input a value between 0 and 1"
        return False
    else:
        return True

def findNumberOfCommunities():
    while True:
        try:
            numberOfCommunities = int(raw_input("Enter the number of Communities in the actual network."))
            break
        except ValueError:
            print "That was not an integer number, Please try again"
    return numberOfCommunities

def findAverageMean():
    while True:
        try:
            meanValue = float(raw_input("What is the mean for the exponential distribution?"))
            break
        except ValueError:
            print "That was not a useable number, Please try again"
    return meanValue

''' Main      '''
# actualNetwork = nx.read_gexf("BokoTrust.gexf")
# print "Number of nodes: ", actualNetwork.edges()
# kCore = nx.k_core(actualNetwork)
# print "K-Core = ", kCore

print "Welcome to the Synthetic Terrorist Network Generator"
# actualNodes = findTrueNodeCount()
# numberOfNodes = findNodeCount()
# switch = False
# while switch == False:
#     percentOfCore = findCorePercent()
#     switch = corePercentageCheck(percentOfCore)
# numberOfCommunities = findNumberOfCommunities()
# averageMean = findAverageMean()

syntheticNetworkName = "NoordinKnowledgeSynthetic_Network5.21.gexf"
# network1 = sn.SyntheticNetwork(numberOfNodes,1,percentOfCore,numberOfCommunities,averageMean,actualNodes)
# network1 = sn.SyntheticNetwork(139, 1, .0935, 37, 6.0143885, 139) # Nordin Trust
# network1 = sn.SyntheticNetwork(139, 1, .0719, 26, 5.5107914, 139) # Nordin LOC
network1 = sn.SyntheticNetwork(139, 1, .1799, 41, 17.079137, 139) # Nordin Knowledge
nx.write_gexf(network1.graph, syntheticNetworkName)
print "Congratulations, ", syntheticNetworkName, " has been written to the current directory"
# print nx.average_degree_connectivity(network1.graph)