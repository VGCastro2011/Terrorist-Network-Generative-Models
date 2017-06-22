import networkx as nx
import operator
import random
import numpy as np
import math

class SyntheticNetwork:
    def __init__(self, nodeCount, graph=1, corePercent=0.0935, communities=37, mean=6.0143885, actual=105):
        self.graph = nx.Graph()
        self.nodeDict = {}
        self.zeroNodes = []
        self.percentOfCore = corePercent
        self.numOfCommunities = communities
        self.meanValue = mean
        self.actualNodeCount = actual
        self.degreeDistr = []
        self.unusedEdges = 0
        self.graphType = graph
        self.nodeCount = nodeCount
        for num in range(0,self.nodeCount):
            self.graph.add_node(num)
            self.nodeDict[num] = 0
        self.assignDegreeDistribution()
        # self.designateDegrees()
        self.buildGraph()

    def assignDegreeDistribution(self):
        if self.graphType == 1: # This is trust
            self.calculateDegreeDistribution(0, self.meanValue) # 6.0143885
        if self.graphType == 2: # This is LOC
            self.calculateDegreeDistribution(0, 0.4)
        if self.graphType == 3: # This is Knowledge
            self.calculateDegreeDistribution(24.978829, 1.7784218)

    def calculateDegreeDistribution(self, shape, other=float(0)):
        for node in range(0, self.nodeCount):
            if self.graphType == 1:
                degree  = abs(int(random.expovariate(1/other)))
            elif self.graphType == 2:
                degree = abs(int(random.expovariate(1/other)))
            elif self.graphType == 3:
                degree = abs(int(random.weibullvariate(shape, other)))
            print "Node: Degree ", node, degree
            self.nodeDict[node] = degree
            if (degree == 0) or (degree == 1):
                self.zeroNodes.append(node)
        # if self.graphType == 3:
        #     sortedDict = sorted(self.nodeDict.items(), key=operator.itemgetter(1), reverse=False)
        #     print "Sorted Dict", sortedDict
        #     for node in range(0, int(self.nodeCount * .27338129)): # .27338129 is the percentage of nodes with 0 or 1 in real graph
        #         key = sortedDict[node][0]
        #         value = random.random()
        #         if value <= .86842015:
        #             self.nodeDict[key] = 0
        #         else:
        #             self.nodeDict[key] = 1
        for node in self.zeroNodes:
            chance = random.uniform(0,1)
            if chance <= 0.50:
                self.nodeDict[node] = 2
            else:
                self.nodeDict[node] = 3
        print "New NodeDict items", sorted(self.nodeDict.items(), key=operator.itemgetter(1), reverse=False)

    def designateDegrees(self):
        '''Used when manually entering degrees in a list.'''
        # choose which nodes are going to be what degree
        counter = 0
        for tple in self.degreeDistr:
            for num in range(0, tple[0]):
                self.nodeDict[counter] = tple[1]
                counter += 1

    def determineIfEnoughNodesForCore(self, coreSize):
        minimumDegreeCount = coreSize
        counter = 0
        for node in self.nodeDict:
            if (self.nodeDict[node]) > minimumDegreeCount:
                counter += 1
        if counter >= coreSize:
            return (True, counter)
        else:
            return (False, counter)

    def modifyNodeDictToAccomodateFullCore(self,coreSize, currentCoreSize):
        nodesNeededToBeIncreased = coreSize - currentCoreSize
        for node in range(0,nodesNeededToBeIncreased):
            randNum = random.randint(0, (self.nodeCount))
            if (self.nodeDict[randNum]) < coreSize:
                self.nodeDict[randNum] = coreSize + 1

    def buildCore(self, srtList):
        sizeOfCore = self.findCoreSize() # .1799 is the % of nodes in the core of dataset
        # determine if there are enough nodes to construct a core
        enoughToFillNode = self.determineIfEnoughNodesForCore(sizeOfCore)
        # If there aren't enough nodes to build a core, modify nodes at random to fill it in.
        if enoughToFillNode[0] == False:
            self.modifyNodeDictToAccomodateFullCore(sizeOfCore, enoughToFillNode[1])
        # print "Size of core is: ", sizeOfCore
        returnList = []
        # returnList.append(srtList[0][0]) # this adds largest to core, we don't want that
        while len(returnList) != sizeOfCore:
            # print " len of return list: len of core: ", len(returnList), sizeOfCore
            #print "Finding randNum"
            randNum = (random.randint(1,(self.nodeCount))) -1
            # print "Found randNum and it's value is", randNum, self.nodeDict[randNum]
            if ((self.nodeDict[randNum]) >= sizeOfCore) and (randNum not in returnList) and (randNum > 0):
                #print "Entered if statement"
                returnList.append(randNum)
            #print "len of return list and core is: ", len(returnList), sizeOfCore
            '''If it is stuck in the while loop, most likely there aren't enough nodes with degrees large enough
            to fill it'''
        return returnList # returns a list made up of single elements representing nodes

    def findCoreSize(self):
        if self.graphType == 1:
            coreSize = int(self.percentOfCore * len(self.nodeDict)) # where .0935 is % of nodes seen in core from dataset
        if self.graphType == 2:
            coreSize = int(.0719 * len(self.nodeDict))
        if (self.graphType == 3) or (self.graphType == 4):
            coreSize = int(.1799 * len(self.nodeDict))
        return coreSize

    def findLeaders(self, communities, sortedDict):
        leaderList = []
        # pull out the top nodes and place into leader list
        for node in range(0,communities):
            leaderList.append(sortedDict[node])
        # now permute the leader list and return it
        permutedLeaders = np.random.permutation(leaderList)
        return permutedLeaders

    def updateSortedList(self, sortedList, core):
        newSort = sortedList
        for node in core:
            nodeLocation = [x for x, y in enumerate(newSort) if y[0] == node] # finding node in the tuple and its index
            del newSort[nodeLocation[0]]
        return newSort

    def buildCommunityStructure(self, sortedDict, coreNodes):
        returnList = []
        numOfCommunities = self.findNumOfCommunites()
        for comm in range(0, numOfCommunities):
            community = []
            returnList.append(community)
        updatedSortedList = self.updateSortedList(sortedDict, coreNodes)
        leaders = self.findLeaders(numOfCommunities, updatedSortedList)
        leaderList = []
        for leader in leaders:
            leaderList.append(leader[0])
        pogList = self.updateSortedList(updatedSortedList, leaderList)
        permutedPogList = np.random.permutation(pogList)
        pogs = []
        for pog in permutedPogList:
            pogs.append(pog[0])
        # at this point the core, leaders, and POGs have been separated.
        for comm in returnList:
            # First assign a leader to each community and remove from list of available leaders
            comm.append(leaderList[0])
            del leaderList[0]
            # Now choose 9 other pogs to add to the community
            if len(pogs) >= 19:
                for node in range(0, 19):
                    comm.append(pogs[0])
                    del pogs[0]
            else:
                nodesLeft = len(pogs)
                for node in range(0, nodesLeft):
                    comm.append(pogs[0])
                    del pogs[0]
        return returnList # returns list of lists. The lists are nodes, they are single elements

    def findNumOfCommunites(self):
        if self.graphType == 1:
            numCommunities = int((self.nodeCount * self.numOfCommunities) / self.actualNodeCount)
        elif self.graphType == 2:
            numCommunities = int((self.nodeCount * 25) / 105)
        elif self.graphType == 3:
            numCommunities = int((self.nodeCount * 39) / 105)
        return numCommunities

    def buildGraph(self):
        hasEdgesAddedToGraph = set()
        sortedDict = sorted(self.nodeDict.items(), key=operator.itemgetter(1), reverse=True)
        coreNodes = self.buildCore(sortedDict)
        print coreNodes
        communityList = self.buildCommunityStructure(sortedDict, coreNodes)
        core = self.connectCore(coreNodes)
        for node in core:
            hasEdgesAddedToGraph.add(node)
        counter = 0
        counter1 = 0
        for comm in communityList:
            # if it's the first community, it's going to try and attach to the core.
            if counter == 0:
                if self.graphType == 3:
                    graphAdditions = self.connectCommunity3(comm, core, core)
                else:
                    graphAdditions = self.connectCommunity(comm, core, core)
                    for node in graphAdditions:
                        hasEdgesAddedToGraph.add(node)
            # For subsequent communities, look at the nodes and attach leader to the greatest node count or core.
            if counter >= 1:
                if self.graphType == 3:
                    graphAdditions = self.connectCommunity3(comm, core, core)
                else:
                    graphAdditions = self.connectCommunity(comm, hasEdgesAddedToGraph, core)
                    for node in graphAdditions:
                        hasEdgesAddedToGraph.add(node)
            counter1 += 1
            print "Completed community: ", counter1
        print "Printed all communites"
        # Now add the rest of the edges to the graph
        self.assignRest(coreNodes, (self.pullLeadersFromCommunityList(communityList)))

    def pullLeadersFromCommunityList(self, communities):
        leaders = []
        for community in communities:
            leaders.append(community[0])
        return leaders # returns list of leaders of all communities

    def connectCommunityConnectionStatus(self, comparison, actual):
        count = 0
        for node in comparison:
            for partner in actual:
                if (self.graph.has_edge(node, partner) == False) and (node != partner):
                    count += 1
        return count

    def findMaxValueNode(self, nodesWithEdgesInGraph):
        maxValNode = (0,0)
        for node in nodesWithEdgesInGraph:
            if node in self.nodeDict:
                if self.nodeDict[node] >= maxValNode[1]:
                    maxValNode = (node, self.nodeDict[node])
        return maxValNode


    def connectCommunity(self, community, nodesWithEdgesInGraph, core):
        # First find the person the community is going to connect to.
        addedEdgesToGraph = set()
        # maxValueNode = (0, 0)
        communityLength = len(community)
        connectionDict = {}
        maxValueNode = self.findMaxValueNode(nodesWithEdgesInGraph)
        # for node in nodesWithEdgesInGraph:
        #     if self.nodeDict[node] >= maxValueNode[1]:
        #         maxValueNode = (node, self.nodeDict[node])
        # Per node, figure out how many people to connect to within community
        for node in community:
            availableEdges = self.nodeDict[node]
            # max edges to use is a clique, min edges is 0
            if availableEdges >= communityLength:
                randomNum = random.randint((int(.8 * communityLength)), communityLength) - 1
                connectionDict[node] = randomNum
            elif availableEdges == 0:
                connectionDict[node] = 0
            elif availableEdges <= communityLength:
                randomNum = random.randint((int(.8 * availableEdges)), availableEdges)
                connectionDict[node] = randomNum
        # Now, connect people to the community
        totalEdges = self.findTotalEdges(connectionDict)  # Finds total edges available to community members
        nodesInGraph = community
        while totalEdges > 0:
            for node in nodesInGraph:
                partner = random.choice(nodesInGraph)
                if self.nodeDict[node] == 0:
                    del self.nodeDict[node]
                    nodesInGraph.remove(node)
                else:
                    if self.graph.has_edge(node, partner) == False:
                        if node in self.nodeDict and partner in self.nodeDict:
                            if ((self.nodeDict[node]) > 0) and ((self.nodeDict[partner]) > 0) and (node != partner):
                                self.graph.add_edge(node, partner)
                                self.nodeDict[node] = (self.nodeDict[node]) - 1
                                self.nodeDict[partner] = (self.nodeDict[partner]) - 1
                                connectionDict[node] = (connectionDict[node]) - 1
                                connectionDict[partner] = (connectionDict[partner]) - 1
                                totalEdges = self.findTotalEdges(connectionDict)
                                # print "Total Edges in while statement: ", totalEdges
                                addedEdgesToGraph.add(node)
                                addedEdgesToGraph.add(partner)
        # Now connect leader
        if self.graph.has_edge(community[0], maxValueNode[0]) == False:
            if ((self.nodeDict[community[0]]) > 0) and ((self.nodeDict[maxValueNode[0]]) > 0) and (
                community[0] != maxValueNode[0]):
                self.graph.add_edge(community[0], maxValueNode[0])
                self.nodeDict[community[0]] = (self.nodeDict[community[0]]) - 1
                self.nodeDict[maxValueNode[0]] = (self.nodeDict[maxValueNode[0]]) - 1
                addedEdgesToGraph.add(community[0])
                addedEdgesToGraph.add(maxValueNode[0])
        # Now connect two more
        # sortedCommunity = sorted(connectionDict.items(), key=operator.itemgetter(1), reverse=True)
        # coreMembers = list(core)
        # if len(sortedCommunity) >= 2 :
        #     for num in range(0,2):
        #         sortedNode = sortedCommunity[num]
        #         maxValueNode = self.findMaxValueNode(nodesWithEdgesInGraph)
        #         coreMember = random.choice(coreMembers)
        #         probability = random.uniform(0,1)
        #         probToForm = random.uniform(0,1)
        #         if probToForm <= 0.80:
        #             if probability <= 0.70:
        #                 self.connectToLeader(sortedNode[0], maxValueNode[0])
        #                 addedEdgesToGraph.add(sortedNode[0])
        #                 addedEdgesToGraph.add(maxValueNode[0])
        #             else:
        #                 self.connectToLeader(sortedNode[0], coreMember)
        #                 addedEdgesToGraph.add(sortedNode[0])
        #                 addedEdgesToGraph.add(coreMember)
        self.closeTriangles(connectionDict)
        # IF there aren't many common neighbors, then create some triangles
        self.createTriangles(connectionDict)
        return addedEdgesToGraph

    def connectToLeader(self, node, maxNode):
        if self.graph.has_edge(node, maxNode) == False:
            if ((self.nodeDict[node]) > 0) and ((self.nodeDict[maxNode]) > 0) and (node != maxNode):
                self.graph.add_edge(node, maxNode)
                self.nodeDict[node] = (self.nodeDict[node]) - 1
                self.nodeDict[maxNode] = (self.nodeDict[maxNode]) - 1


    def createTriangles(self, connections):
        trianglesCreated = 0
        for node in connections:
            if (self.graph.has_node(node) == True) and (node not in self.zeroNodes) :
                neighborlist = self.graph.neighbors(node)
                for neighbor in neighborlist:
                    if (self.graph.has_node(neighbor) == True) and (neighbor not in self.zeroNodes):
                        neighborsNeighbors = self.graph.neighbors(neighbor)
                        # choose a rand number to set prob of creating a triangle between node, neighbor, and closer
                        rand = random.uniform(0,1)
                        closer = random.choice(neighborsNeighbors)
                        counter = 0
                        if node not in self.nodeDict:
                            self.nodeDict[node] = 0
                        if neighbor not in self.nodeDict:
                            self.nodeDict[neighbor] = 0
                        if closer not in self.zeroNodes:
                            if closer not in self.nodeDict:
                                self.nodeDict[closer] = 0
                            if (rand <= 0.95) and (closer != node):
                                if self.graph.has_edge(node, closer) == False:
                                    print "Triangle not complete from node"
                                    self.nodeDict[node] = (self.nodeDict[node]) + 1
                                    self.nodeDict[closer] = (self.nodeDict[closer]) + 1
                                    self.graph.add_edge(node, closer)
                                    self.nodeDict[node] = (self.nodeDict[node]) - 1
                                    self.nodeDict[closer] = self.nodeDict[closer] - 1
                                    if self.nodeDict[node] <= 0:
                                        del self.nodeDict[node]
                                    if self.nodeDict[closer] <= 0:
                                        del self.nodeDict[closer]
                                    counter += 1
                                if self.graph.has_edge(neighbor, closer) == False:
                                    "Triangle not complete from neighbor"
                                    self.nodeDict[neighbor] = (self.nodeDict[neighbor]) + 1
                                    self.nodeDict[closer] = (self.nodeDict[closer]) + 1
                                    self.graph.add_edge(neighbor, closer)
                                    self.nodeDict[neighbor] = (self.nodeDict[neighbor]) - 1
                                    self.nodeDict[closer] = (self.nodeDict[closer]) - 1
                                    if self.nodeDict[node] <= 0:
                                        del self.nodeDict[node]
                                    if self.nodeDict[closer] <= 0:
                                        del self.nodeDict[closer]
                                    counter += 1
                        if counter > 0:
                            trianglesCreated += 1
                    counter = 0
        print "Triangles Created: ", trianglesCreated


    def closeTriangles(self, connections):
        trianglesClosed = 0
        for node in connections:
            if self.graph.has_node(node) == True:
                neighborList = self.graph.neighbors(node)
                for neighbor in neighborList:
                    if self.graph.has_node(neighbor) == True:
                        neighborsNeighbors = self.graph.neighbors(neighbor)
                        # now we have two neighbor lists. Find the intersection of the lists and those are the common nodes
                        intersectionList = [nb for nb in neighborList if nb in neighborsNeighbors]
                        # now for each node in the intersection, check if the edges to that node exist from node and neighbor nd add it
                        if len(intersectionList) > 0:
                            counter = 0
                            for closer in intersectionList:
                                if self.graph.has_edge(node, closer) == False:
                                    print "Triangle not complete from node"
                                    self.nodeDict[node] = (self.nodeDict[node]) + 1
                                    self.nodeDict[closer] = (self.nodeDict[closer]) + 1
                                    self.graph.add_edge(node, closer)
                                    self.nodeDict[node] = (self.nodeDict[node]) - 1
                                    self.nodeDict[closer] = (self.nodeDict[closer]) - 1
                                    counter += 1
                                if self.graph.has_edge(neighbor, closer) == False:
                                    "Triangle not complete from neighbor"
                                    self.nodeDict[neighbor] = (self.nodeDict[neighbor]) + 1
                                    self.nodeDict[closer] = (self.nodeDict[closer]) + 1
                                    self.graph.add_edge(neighbor, closer)
                                    self.nodeDict[neighbor] = (self.nodeDict[neighbor]) - 1
                                    self.nodeDict[closer] = (self.nodeDict[closer]) - 1
                                    counter += 1
                                if counter > 0:
                                    trianglesClosed += 1
                                counter = 0
        print "Triangles closed in this community: ", trianglesClosed


    def connectCommunity3(self, community, nodesWithEdgesInGraph, core):
        # First find the person the community is going to connect to.
        addedEdgesToGraph = set()
        maxValueNode = (0,0)
        # communityLength = len(community)
        connectionDict = {}
        for node in nodesWithEdgesInGraph:
            if self.nodeDict[node] >= maxValueNode[1]:
                maxValueNode = (node, self.nodeDict[node])
        # First populate the connectionDictionary with the members of that dictionary.
        for node in community:
            connectionDict[node] = self.nodeDict[node]
        # put nodes in a list to use in next loop
        actualCommunity = []
        for node in connectionDict:
            actualCommunity.append(node)
        # Then take out all of the zero nodes to see how many people will actually connect in the community
        for node in actualCommunity:
            if connectionDict[node] == 0:
                del connectionDict[node]
        # New community length is the length of the connectionDict at tbis point.
        communityLength = len(connectionDict)
        actualCommunity = []
        for node in connectionDict:
            actualCommunity.append(node)
        # Per node, figure out how many people to connect to within community
        for node in actualCommunity:
            availableEdges = self.nodeDict[node]
            # max edges to use is a clique, min edges
            if availableEdges >= communityLength:
                randomNum = random.randint(1, communityLength)
                connectionDict[node] = randomNum
            elif availableEdges == 0:
                connectionDict[node] = 0
            elif availableEdges <= communityLength:
                randomNum = random.randint(1, availableEdges)
                connectionDict[node] = randomNum
        # Now, connect people to the community
        totalEdges = self.findTotalEdges(connectionDict)  # Finds total edges available to community members
        nodesInGraph = actualCommunity
        switch = False
        while switch == False :
            if len(connectionDict) == 1:
                break
            comparisonDict = connectionDict
            for node in nodesInGraph:
                partner = random.choice(nodesInGraph)
                if connectionDict[node] == 0:
                    del connectionDict[node]
                    nodesInGraph.remove(node)
                    continue
                else:
                    # print "Entered else statement"
                    if self.graph.has_edge(node, partner) == False:
                        if node in self.nodeDict and partner in self.nodeDict:
                            if ((connectionDict[node]) > 0) and ((connectionDict[partner]) > 0) and (node != partner):
                                self.graph.add_edge(node, partner)
                                self.nodeDict[node] = (self.nodeDict[node]) - 1
                                self.nodeDict[partner] = (self.nodeDict[partner]) - 1
                                connectionDict[node] = (connectionDict[node]) - 1
                                connectionDict[partner] = (connectionDict[partner]) - 1
                                totalEdges = self.findTotalEdges(connectionDict)
                                # print "Total Edges in while statement: ", totalEdges
                                addedEdgesToGraph.add(node)
                                addedEdgesToGraph.add(partner)
                    else:
                        print "comparison", comparisonDict
                        print "actual", connectionDict
                        allConnectionsMadeStatus = self.connectCommunityConnectionStatus(comparisonDict, connectionDict)
                        print "all connection status", allConnectionsMadeStatus
                        if (totalEdges == 0) or (allConnectionsMadeStatus == 0) or (len(connectionDict) == 1):
                            switch = True
        # Now connect leader
        if self.graph.has_edge(community[0], maxValueNode[0]) == False:
            if ((self.nodeDict[community[0]]) > 0) and ((self.nodeDict[maxValueNode[0]]) > 0) and (community[0] != maxValueNode[0]):
                self.graph.add_edge(community[0], maxValueNode[0])
                self.nodeDict[community[0]] = (self.nodeDict[community[0]]) - 1
                self.nodeDict[maxValueNode[0]] = (self.nodeDict[maxValueNode[0]]) - 1
                addedEdgesToGraph.add(community[0])
                addedEdgesToGraph.add(maxValueNode[0])
                print "added a leader"
        self.closeTriangles(connectionDict)
        self.createTriangles(connectionDict)
        return addedEdgesToGraph

    def addNode(self, node, partner):
        if self.graph.has_edge(node, partner) == False:
            if node in self.nodeDict and partner in self.nodeDict:
                if ((self.nodeDict[node]) > 0) and ((self.nodeDict[partner]) > 0) and (node != partner):
                    self.graph.add_edge(node, partner)
                    self.nodeDict[node] = (self.nodeDict[node]) - 1
                    self.nodeDict[partner] = (self.nodeDict[partner]) - 1

    def assignRest(self, core, leaders):
        availableMembers = self.findAvailableMembers()
        garbage = []
        switch = False
        while switch == False:
            comparisonDict = self.nodeDict
            allConnectionsStatus = self.determineIfAllConnectionsMade(comparisonDict)
            # print "enter while loop"
            if (len(self.nodeDict) == 0) or (allConnectionsStatus == 0):
                self.unusedEdges = self.determineUnusedEdges()
                switch = True
                break
            for node in availableMembers:
                if self.nodeDict[node] == 0:
                    del self.nodeDict[node]
                    garbage.append(node)
                    availableMembers.remove(node)
                else:
                    if self.nodeDict[node] > 0:
                        if node in core:
                            chanceToConnectToLeader = random.random()
                            if chanceToConnectToLeader >= float(.3):
                                partner = random.choice(leaders)
                                self.addNode(node, partner)
                            else:
                                partner = random.choice(availableMembers)
                                self.addNode(node, partner)
                        elif node in leaders:
                            chanceToConnectToCore = random.random()
                            if chanceToConnectToCore >= float(.3):
                                partner = random.choice(core)
                                self.addNode(node, partner)
                            else:
                                partner = random.choice(availableMembers)
                                self.addNode(node, partner)
                        else:
                            partner = random.choice(availableMembers)
                            self.addNode(node, partner)
            for node in garbage:
                if node in availableMembers:
                    availableMembers.remove(node)
            # print "nodeDict is :", self.nodeDict

    def determineIfAllConnectionsMade(self, comparison):
        count = 0
        for node in comparison:
            for partner in self.nodeDict:
                if (self.graph.has_edge(node, partner) == False) and (node != partner):
                    count += 1
        return count

    def determineUnusedEdges(self):
        unusedEdges = 0
        for node in self.nodeDict:
            unusedEdges += self.nodeDict[node]
        return unusedEdges


    def findAvailableMembers(self):
        members = []
        for node in self.nodeDict:
            members.append(node)
        return members

    def findTotalEdges(self, community):
        totalEdges = 0
        for node in community:
            totalEdges += community[node]
        return totalEdges

    def connectCore(self, core):
        addedEdgesToGraph = set()
        for node in core:
            if self.nodeDict[node] != 0:
                for partner in core:
                    if self.nodeDict[partner] != 0:
                        if node != partner:
                            if self.graph.has_edge(node, partner) == False:
                                self.graph.add_edge(node, partner)
                                self.nodeDict[node] = (self.nodeDict[node]) - 1
                                self.nodeDict[partner] = (self.nodeDict[partner]) - 1
                                addedEdgesToGraph.add(node)
                                addedEdgesToGraph.add(partner)
        return addedEdgesToGraph

############# Main ################

# network1 = SyntheticNetwork(139)
# print network1.graph.edges()
# print "Unused edges in network 1 total to: ", network1.unusedEdges
# nx.write_gexf(network1.graph, "trustSynthetic4.gexf")
# #
# network2 = SyntheticNetwork(139, 2)
# print network2.graph.edges()
# print "Unused edges in network 2 total to: ", network2.unusedEdges
# nx.write_gexf(network2.graph, "LOCSynthetic4.gexf")

# network3 = SyntheticNetwork(139, 3)
# print network3.graph.edges()
# print "Unused edges in network 3 total to: ", network3.unusedEdges
# nx.write_gexf(network3.graph, "KnowledgeSynthetic4.gexf")

# network4 = SyntheticNetwork(139, 4)
# print network4.graph.edges()
# print "Unused edges in network 4 total to: ", network4.unusedEdges
# nx.write_gexf(network4.graph, "MonoplexSynthetic2.gexf")