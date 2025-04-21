from math import inf, ceil

### DO NOT CHANGE THIS FUNCTION
def load_dictionary(filename):
    infile = open(filename, encoding='utf-8')
    word, frequency = "", 0
    aList = []
    for line in infile:
        line.strip()
        if line[0:4] == "word":
            line = line.replace("word: ","")
            line = line.strip()
            word = line            
        elif line[0:4] == "freq":
            line = line.replace("frequency: ","")
            frequency = int(line)
        elif line[0:4] == "defi":
            index = len(aList)
            line = line.replace("definition: ","")
            definition = line.replace("\n","")
            aList.append([word,definition,frequency])

    return aList
    
class Trie:

    def __init__(self, Dictionary: list[list[str, str, int]]) -> None:
        """
        Function Description:
            Initialise the dictionary and trie. Record words in the dictionary into a trie for 
            easy retrieval.

        Approach Description:
            In addition to the usual 26 alphabet, by allocating 2 more index for dictionary index
            and total number of matches, we can have easy retrieval for the word and definition, as
            well as number of matches with the prefix.
            As we don't need an end point marker '$', we replace that with a dictionary index for 
            current highest frequency word for that particular prefix. 
            We also record num_matches as we register the word in the trie.

        Input:
            Dictionary: A list of list containing the string of the word, definition and 
            frequency of word used in int.

        Time Complexity: O(T), where T is the total number of characters in Dictionary.txt
        Aux Space Complexity: O(T), where T is the total number of characters in Dictionary.txt
        """
        self.dictionary = Dictionary                  # word, def, freq
        self.trie = [None for _ in range(27)] + [0]   # a-z, dictionary entry index, num_matches
        for i, entry in enumerate(self.dictionary):
            self.record_word(entry[0], 0, i, self.trie)

    def record_word(self, word: str, index: int, entry: int, arr: list) -> None:
        """
        Function Description: 
            Register a single letter from the index-th letter of input word into the trie.

        Approach Description: 
            Record the letter of each word one by one as described mostly in init and line comments.

        Input:
            word: string to be inputted into the trie
            index: index of word to be inputted
            entry: current word dictionary entry index
            arr: array of the current trie depth the word is to be recorded on

        Time Complexity: O(L) where L is the number of characters in the strings
        Aux Space Complexity: O(L) where L is the number of characters in the strings
        """
        arr[-1] += 1                                                        # increase num_matches
        if arr[-2] is None:                                                 # if there are no entries yet
            arr[-2] = entry
        elif arr[-2] != entry:
            if self.dictionary[entry][2] > self.dictionary[arr[-2]][2]:     # compares frequency
                arr[-2] = entry
            elif self.dictionary[entry][2] == self.dictionary[arr[-2]][2]:  # compares string
                if self.dictionary[entry][0][index:] < self.dictionary[arr[-2]][0][index:]: 
                    arr[-2] = entry                                # compares lesser string each time
        if len(word) == index:                                     # if there are no letters left
            return
        arr_index = ord(word[index]) - 97
        if arr[arr_index] is None:                                 # creates array if no entries yet
            arr[arr_index] = [None for _ in range(27)] + [0]
        self.record_word(word, index+1, entry, arr[arr_index])     # calls itself with updated parameters
    
    def prefix_search(self, prefix: str) -> list[str|None, str|None, int]:
        """
        Function Description:
            Searches for the word with the highest frequency that has prefix entered. Returns 
            the definition and number of matches for that prefix as well.

        Approach Description:
            Retrieves the last 2 index of the arr of the prefix, which contains information on 
            the word of highest frequency and number of matches for that prefix.
            Complexity is O(M+N), where M is the length of the prefix entered by the user and 
            N is the total number of characters in the word with the highest frequency and its definition.

        Input:
            prefix: prefix requested

        Output:
            list in the form [word, definition, num_matches]

        Time Complexity: O(M+N) 
        Aux Space Complexity: O(M+N)
        """
        result = self.prefix_search_aux(prefix, 0, self.trie)
        if result is None:                                      # if no result is found
            return [None, None, 0]
        return self.dictionary[result[0]][:2] + [result[1]]
    
    def prefix_search_aux(self, prefix: str, index: int, arr: list) -> tuple[int, int]|None:
        """
        Function Description: Auxilliary function for prefix_search for recursion.

        Input:
            prefix: prefix of word
            index: index of word to search
            arr: current depth of the trie accessed by the prefix

        Output:
            Returns [dictionary entry index, num_matches]
            Returns None if there is no result.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if arr is None:
            return None
        elif len(prefix) == index or len(prefix) == 0:
            return arr[26:]
        arr_index = ord(prefix[index]) - 97
        return self.prefix_search_aux(prefix, index+1, arr[arr_index])
    

# Question2
class AGraph():

    def __init__(self, preferences: list[list[int]], licences: list[int]) -> None:
        """
        Function Description:
            Initialise the graph needed for bipartite matching. 

        Approach Description:
            Used adjacency matrix for easy reverse flow. 
            The order of vertices are as follows: car_1 to car_n/5, person_1 to person_n, source, target
            Every cell has a list of integers that represents [flow, capacity, licence (1 for True)]. 
            If no edge is found between them, it is represented by None. Reverse flow is also set here.
            Target capacity is set to 2 first, then we run max_flow() once before changing it to 5.

        Input: 
            preferences: list of a person's list of preference of destinations
            licences: list of people who has driving licence

        Time Complexity: O(n^2) where n is len(preference), aka number of people
        Aux Space Complexity: O(n^2) where n is len(preference), aka number of people
        """
        self.cars = ceil(len(preferences)/5)                     # number of destinations (ceil(n/5))
        self.people = len(preferences)
        self.vertices = self.cars + self.people + 2              # all vertices in the graph
        self.licences = licences
        self.graph = []
        for _ in range(self.vertices):                           # rows of matrix
            self.graph.append([None]*self.vertices)              # None for no edges/paths
        for i, person in enumerate(preferences):                 # for every person,
            for destination in person:                           # for every destination they want to go
                self.graph[self.cars + i][destination] = [0, 1, 0]        # flow, capacity, licence
                self.graph[destination][self.cars + i] = [0, 0, 0]        # reverse flow
            self.graph[-2][self.cars + i] = [0, 1, 0]                     # source
            self.graph[self.cars + i][-2] = [0, 0, 0]                     # source reverse
        for i in range(self.cars):
            self.graph[i][-1] = [0, 2, 0]                # target (set as 2[min driver required] for now)
            self.graph[-1][i] = [0, 0, 0]                                 # target reverse
        for person in self.licences:                                      # setting those with licence
            for i, edge in enumerate(self.graph[person + self.cars]):
                if edge is not None and edge[1] != 0:    # latter is so source node doesn't get affected
                    edge[2] = 1      
                    self.graph[i][person + self.cars][2] = -1             # reduction of drivers

    def max_flow(self, flow: int, visited: list[bool]) -> int:
        """
        Function Description:
            Gets the max flow of the graph.

        Approach Description: 
            The same as Ford Fulkerson method, except since we are running twice with different
            settings, flow and visited. As the first time, we only run the drivers max_flow,
            flow = 0, while visited is True only for non-drivers (so DFS does not run them).
            The second time, as we already ran max_flow once, flow = previous flow result, 
            and visited is False for all. 
            Time Complexity for normal max_flow is O(EF), but if everyone wants to go to every
            possible destination, the graph gets dense, and E = n^2. The max_flow = number of people,
            which is n, therefore, resultant time complexity is O(n^3).
            Aux space complexity is O(n^2), as stack memory is cleared once recursion ends.

        Input: 
            flow: the flow of the graph
            visited: list of bool that DFS needs to visit

        Output:
            Returns the maximum flow of the graph

        Time Complexity: O(n^3), where n is number of people
        Aux Space Complexity: O(n^2), where n is number of people
        """
        augment = 1                             # to kickstart loop
        while augment > 0:
            augment = self.dfs(self.vertices-2, self.vertices-1, inf, \
                               visited[:], 0)  # source, target, bottleneck, visited bool list, no driver
            flow += augment
        return flow

    def dfs(self, fro: int, to: int, bottleneck: int, visited: list[bool], previous: int) -> int:
        """
        Function Description:
            Depth First Search algorithm to find all possible paths to augment the graph.

        Approach Description:
            A typical DFS for Ford-Fulkerson method that checks if there is a one-to-one 
            exchange of drivers. 

        Input: 
            fro, to: current vertex, target vertex
            bottleneck: minimum capacity of the path
            visited: list of bool that DFS needs to visit
            previous: 1 if previous edge is a driver, 0 if not, -1 if driver reverse flow
        
        Output:
            Returns the resultant flow of the path

        Time Complexity: O(E) where E is the number of edges
        Aux Space Complexity: O(E) where E is the number of edges
        """
        if fro == to:
            return bottleneck
        visited[fro] = True                                         # vertex is visited
        for i, edge in enumerate(self.graph[fro]):
            if edge is not None:
                residual = edge[1] - edge[0]
                driver = edge[2] + previous                         # one to one exchange of drivers
                if residual > 0 and not visited[i] and driver >= 0:
                    augment = self.dfs(i, to, min(bottleneck, residual), visited, edge[2])
                    if augment > 0:
                        edge[0] += augment                              
                        self.graph[i][fro][0] -= augment            # reverse flow
                        return augment
        return 0                                                    # no augmenting path
    
    def car_arrangement(self) -> list[list[int]]:
        """
        Function Description:
            Retrieves information from self.graph on allocation of the cars and people.

        Approach Description:
            By refering to edges in vertices of the cars, if there is a reverse flow from vertices
            that represent people, we would know that those are the people which is allocated
            to this car. 
            Time complexity is number of cars (n/5) * number of people (n), hence O(n^2).
            Aux space complexity is O(n), as only 0 to n is in the list.

        Output: 
            Result of allocation in list of list of people, where index x represents car number x.

        Time Complexity: O(n^2) where n is number of people
        Aux Space Complexity: O(n) where n is the number of people
        """
        arrangement = []
        for car in range(self.cars):
            car_list = []
            for i, edge in enumerate(self.graph[car]):
                if edge is not None and edge[0] == -1:      # by retrieving flow == -1, we know which 
                    car_list.append(i - self.cars)          # person it came from
            arrangement.append(car_list)
        return arrangement

    def allocate(self) -> list[list[int]]:
        """
        Function Description:
            Allocate people to cars using functions in class AGraph

        Approach Description:
            By allocating drivers first, it will ensure that there is enough drivers per car,
            and by algorithm in dfs, the ability to prevent a reverse flow of drivers if the 
            incoming flow is not one. This ensures there is always 2 drivers per car.
            Same complexity as max_flow.

        Output: 
            Result of allocation in list of list of people, where index x represents car number x.

        Time Complexity: O(n^3), where n is number of people
        Aux Space Complexity: O(n^2), where n is number of people
        """
        visited = [True]*(self.vertices-2)
        visited += [False, False]                                 # for source and target
        for person in self.licences:                              # we only allow travel for drivers
            visited[person + self.cars] = False             
        for i in range(self.cars):                                # and cars
            visited[i] = False
        if self.cars*2 != self.max_flow(0, visited):              # if not enough (2) drivers for any car
            return None
        for i in range(self.cars):
            self.graph[i][-1][1] = 5                              # reset car to target flow back to 5
        visited = [False]*self.vertices
        if self.people != self.max_flow(self.cars*2, visited):    # if allocations not possible
            return None
        return self.car_arrangement()                             # get result from graph
    
def allocate(preferences: list[list[int]], licences: list[int]) -> list[list[int]]:
    """Refer to class AGraph"""
    graph = AGraph(preferences, licences)
    return graph.allocate()

if __name__ == "__main__":
    Dictionary = load_dictionary("Dictionary.txt")
    myTrie = Trie(Dictionary)
    print(myTrie.prefix_search(""))
    preferences = [[0],[0],[1,0],[0,1],[1],[1],[0],[0],[0],[1]]
    licences = [2,3,1,5,0,4]
    print(allocate(preferences, licences))