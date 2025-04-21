from math import inf
######## Question 1

def restaurantFinder(d: int, site_list: list[int]) -> tuple[int, list]:
    """
    Function Description:
        Finds the maximum possible revenue along a stretch of road spaced 1km apart of each other,
        that are not within a certain distance apart, given by d.

    Approach Description:
        Initialize the first (d+1) sites. Since there are within d distance, there can only be one site
        that meet the requirement, which is the maximum within index 0 to n, for n <= d. 
        For sites in index > d, we compare it with the maximum site revenue between the previous site,
        or previous d-1 site + current_site. That will give us our maximum revenue for index 0 to n. 
        As we only loop through each site once, the time complexity is O(N).
        As for the selected sites, we check if the current site revenue is the same as the previous 
        site revenue. If it is, it means that the current site is not used as revenue. If it is different,
        it means the current site is being counted as revenue, and hence should be added into the 
        selected sites. We can then reduce the index by d+1, as we are sure that no sites in between was
        chosen. 

    Input:
        d: distance parameter, non-negative
        site_list: a list of int, denoting revenue of sites 1km apart

    Output:
        total_revenue: maximum possible revenue given d
        selected_sites: a list of those sites that make total_revenue possible

    Time complexity: O(N) where N is len(site_list)
    Aux space complexity: O(N) where N is len(site_list)
    """
    if d >= len(site_list):                 #if d is >= then number of sites, just choose the max
        total_revenue, selected_sites = 0, [] 
        for i, revenue in enumerate(site_list):
            if revenue > total_revenue:
                total_revenue = revenue
                selected_sites = [i+1]
        return total_revenue, selected_sites
    site_revenue = [0]*len(site_list)       #initialise max site revenue
    for i in range(d+1):                    #for index 0 to d
        site_revenue[i] = max(site_revenue[i-1], site_list[i])
    for i in range(d+1, len(site_list)):    #for index d+1 to n
        site_revenue[i] = max(site_revenue[i-d-1]+site_list[i], site_revenue[i-1])
    selected_sites = []
    x = len(site_list)
    while x > 0:
        if site_revenue[x-1] != site_revenue[x-2]:
            if site_revenue[x-1] > 0:          #if the site is not of negative revenue
                selected_sites.append(x)
            x -= d + 1
        else:
            x -= 1
    if site_revenue[-1] > 0 and len(selected_sites) == 0:   #edge case: if all sites have the same revenue
        selected_sites = [1]
    total_revenue = site_revenue[-1]
    selected_sites.reverse()
    return total_revenue, selected_sites


############### Question 2

class FloorGraph:
    def __init__(self, paths: list[tuple[int, int, int]], keys: list[tuple[int, int]]) -> None:
        """
        Function Description:
            A constructor that initialises the map of the floor of the tower into a graph. 
            It stores both locations, paths and keys of the floor.

        Approach Description:
            Find the number of vertices by checking the highest ID of the paths given, which
            is the first two numbers stored in the tuples of the path list.
            Storing the details of paths in an adjacency list with vertex as the index, 
            with direction and distance as a tuple (v,x). Keys are stored as a separate list, and 
            since keys <= vertices, it maintains both complexities.
            Vertices with no edges are stored as None, and vertices with no keys are stored as inf.

        Input:
            paths: a list of tuples, with tuples containing vertex u, vertex v, distance x, indicating
                   there is a paths from u to v, of distance in time, x mins.
            keys: a list of tuples, with tuples containing vertex u and time k, indicating there is
                  a key in vertex u, with k mins the time it takes to obtain the key.

        Output:
            None

        Time Complexity: O(V+E), where V is the vertices and E is the edges in the graph
        Space Complexity: O(V+E), where V is the vertices and E is the edges in the graph
        """
        max_id = max([max(u,v) for u,v,x in paths])
        self.vertices = [None]*(max_id+1)
        for u,v,x in paths:
            if self.vertices[u] is None:
                self.vertices[u] = [(v,x)]
            else:
                self.vertices[u].append((v,x))
        self.keys = [inf]*(max_id+1)
        for k,y in keys:
            self.keys[k] = y

    def climb(self, start: int, exits: list[int]) -> tuple[int, list[int]]|None:
        """
        Function Description:
            A function that finds the shortest possible path for a particular floor given the starting
            point and possible exits in the graph. 

        Approach Description:
            Using a modified Dijkstra algorithm, while prioritizing the shortest possible path first,
            we allow the algorithm to override any shorter paths if that particular vertex does not 
            have a key, we are able to get the shortest path that has a key. Since we do not add any
            other loops, the complexities are the same as Dijkstra algorithm.
            Therefore we need not only need to store the shortest distance, we also need to store if the
            current path from start has a key. Using an int to represent the time to obtain a key, with
            inf to represent that there is no key. 
            The priority queue used is a min heap, which also allows storage of distance information
            other than vertex. This allows prioritizing shortest distance.
            Then, checking against all other distances of different exits, we get the shortest distance
            and the exit for output.
            To find the route, as looping is possible unlike the conventional Dijkstra algorithm, there
            is a need to trace back the different predecessors that might be pointing to the same vertex
            multiple times. Hence, we need an array of list to store the predecessor, and a third value
            to store the number of nodes travelled, so to know when to stop the loop.

        Input:
            start: int that represents the starting vertex ID
            exits: a list of int that represent possible exit vertices ID
            
        Output:
            total_time: shortest time taken to clear a floor in mins
            route: route that is taken for shortest time in list of vertices

        Time Complexity: O(E*log(V)), where V is the vertices and E is the edges in the graph
        Space Complexity: O(V+E), where V is the vertices and E is the edges in the graph
        """
        distance = [(inf,inf,inf)]*len(self.vertices)  #total distance, min key through route, nodes travelled
        predecessor = []
        for _ in range(len(self.vertices)):
            predecessor.append([])
        distance[start] = (0, self.keys[start], 0)               #start initialised to 0
        queue = minheap((start, distance[start][0]))             #priority queue
        while not queue.is_empty():        
            vertex = queue.pop()        
            if self.vertices[vertex[0]]:                         #checks if vertex goes anywhere
                for v,x in self.vertices[vertex[0]]:             #iterates through all its edges
                    min_key = distance[vertex[0]][1]
                    if distance[vertex[0]][0] + x < distance[v][0]:   #if distance is shorter (regardless of key)
                        if min_key > self.keys[v]:                    #updates key if it takes a shorter time
                            min_key = self.keys[v]
                        distance[v] = distance[vertex[0]][0] + x, \
                            min_key, distance[vertex[0]][2] + 1       #updates the values
                        queue.push((v, distance[v][0]))
                        predecessor[v].append(vertex[0])
                    elif distance[vertex[0]][0] + distance[vertex[0]][1] + x \
                            < distance[v][0] + distance[v][1]:        #compares with key as well, no key represented by inf
                        distance[v] = distance[vertex[0]][0] + x, \
                            min_key, distance[vertex[0]][2] + 1    
                        queue.push((v, distance[v][0]))
                        predecessor[v].append(vertex[0])
        total_time, end = inf, None
        for exit in exits:                                      #find shortest exit
            if distance[exit][0] + distance[exit][1] < total_time:
                total_time, end = distance[exit][0] + distance[exit][1], exit
        if total_time is inf:                                   # if no possible paths
            return None
        route = [end]                                           #finding the route
        travelled = distance[end][2]                            
        while travelled > 0:                                    #loop till number of nodes traversed
            pred = predecessor[end][-1]
            route.append(pred)
            del predecessor[end][-1]
            end = pred
            travelled -= 1
        route.reverse()
        return total_time, route

class minheap():

    def __init__(self, point: tuple[int, int]) -> None:
        """
        Function Description:
            Modified minimum heap data stucture as priority queue for usage in FloorGraph init. 
            Stores information about the current vertex as well as distance travelled. 
            Minimum distance travelled is prioritized. 

        Approach Description:
            Simple min heap structure learned in FIT1008. First element is not used. 

        Input: 
            point: tuple of two int, first being vertex ID and second being distance travelled in mins
        
            Output: None

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.heap = [None, point]
    
    def is_empty(self) -> bool:
        """
        Function Description:
            Checks if heap is empty

        Input:
            None

        Output: 
            bool, True if heap is empty, False otherwise
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return len(self.heap) == 1

    def __len__(self) -> int:
        """
        Function Description:
            Checks for number of elements in heap

        Input: None
        Output: 
            int, number of element in heap
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return len(self.heap)-1
    
    def push(self, point: tuple[int, int]) -> None:
        """
        Function Description:
            Adds an element in the heap
        Input:
            point: as stated in __init__
        Output:
            None
        Time Complexity: O(log(n)) where n is the number of element in the heap, due to _rise
        Space Complexity: O(1)
        """
        self.heap.append(point)
        self._rise(len(self))
    
    def pop(self) -> tuple[int, int]:
        """
        Function Description:
            Returns the prioritized element in the heap (min distance) and deletes them from the queue

        Input: None
        Output: 
            min: point with the smallest distance 
        Time Complexity: O(log(n)) where n is the number of element in the heap, due to _sink
        Space Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError
        min = self.heap[1]
        self.heap[1] = self.heap[-1]
        del self.heap[-1]
        if not self.is_empty():    
            self._sink(1)
        return min
    
    def _rise(self, k: int) -> None:
        """
        Function Description:
            Rise element to its correct position

        Input: 
            k: index of the element in the wrong position
        Output:
            None
        Time Complexity: O(log(n)) where n is the number of element in the heap
        Space Complexity: O(1)
        """
        point = self.heap[k]
        while k > 1 and point[1] < self.heap[k//2][1]:
            self.heap[k] = self.heap[k//2]
            k = k//2
        self.heap[k] = point
    
    def _sink(self, k: int) -> None:
        """
        Function Description:
            Sink an element to its correct position

        Input:
            k: index of element in the wrong position
        Output:
            None
        Time Complexity: O(log(n)) where n is the number of element in the heap
        Space Complexity: O(1)
        """
        point = self.heap[k]
        while 2*k <= len(self):
            min_child = self.smallest_child(k)
            if self.heap[min_child][1] >= point[1]:
                break
            self.heap[k] = self.heap[min_child]
            k = min_child
        self.heap[k] = point
    
    def smallest_child(self, k: int) -> int:
        """
        Function Description:
            Return the index of its smaller child

        Input:
            k: index of parent node
        Output:
            index of the child
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if 2*k == len(self) or self.heap[2*k][1] < self.heap[2*k+1][1]:
            return 2*k
        else:
            return 2*k+1