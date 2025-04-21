from __future__ import annotations
from typing import Generic, TypeVar
from math import ceil
from bst import BinarySearchTree
from node import TreeNode

T = TypeVar("T")
I = TypeVar("I")

class Percentiles(Generic[T]):

    def __init__(self) -> None:
        """
        __init___
        
        Initialises the Percentile class.
        
        Parameter/s: None
        Return case: None
        
        Worst-case complexity: O(1)
        Best-case complexity: O(1)
        """
        
        self.tree = BinarySearchTree()
    
    def add_point(self, item: T) -> None:
        """
        add_point
        
        Adds a point to the object.
        
        Parameter/s: item - the point to add to the object
        Return case: None
        
        Worst-case complexity: O(log(n))
        Best-case complexity: O(log(n))
        """

        self.tree[item] = item
    
    def remove_point(self, item: T) -> None:
        """
        remove_point
        
        Removes from a point from the object.
        
        Parameter/s: item - the point to remove from the object
        Return case: None
        
        Worst-case complexity: O(log(n))
        Best-case complexity: O(log(n))
        """
        
        del self.tree[item]

    def ratio(self, x: float, y: float) -> list[T]:
        """
        ratio
        
        Computes a list of all items fitting the larger/smaller than criteria. 
        This list doesn't need to be sorted.
        
        Parameter/s: x - the returned list must contain elements larger than x% of elements in the list
                     y - the returned list must contain elements smaller than y% of elements in the list
        Return case: list[T] - a list of all items fitting the larger/smaller than criteria
        
        Worst-case complexity: O(log(n) + m), where n is the number of points already in the object 
                               and m is the number of points returned by the function
        Best-case complexity:  O(log(n)), where only one item meets the criteria.
        """

        result = []
        xIndex = ceil(x * len(self) / 100) + 1
        yIndex = (100 - y) * len(self) // 100
        root = self.tree.root

        if root is not None:
            smallestNode = self.tree.kth_smallest(xIndex, root)
            largestNode = self.tree.kth_smallest(yIndex, root)
            result = self.ratio_aux(root, smallestNode, largestNode, result)

        return result
    
    def ratio_aux(self, current: TreeNode, smallestNode: TreeNode, largestNode: TreeNode, result: list[T]) -> list[T]:
        """
        ratio_aux
        
        Recursively adds to the result list until the desired length has been achieved.
        
        Parameter/s: current - the node being assessed
                     smallestNode - the node of smallest value which will be added to the result list
                     largestNode - the node of largest value which be added to the result list
                     result - the list to be returned by the ratio function
        Return case: list[T] - the updated result list

        Complexity: O(1)
        """
        if current is not None:
            if current.key < smallestNode.key:
                self.ratio_aux(current.right, smallestNode, largestNode, result)
            elif current.key > largestNode.key:
                self.ratio_aux(current.left, smallestNode, largestNode, result)
            else:
                result.append(current.item)
                self.ratio_aux(current.left, smallestNode, largestNode, result)
                self.ratio_aux(current.right, smallestNode, largestNode, result)
            return result
    
    def __len__(self) -> int:
        """
        __len__
        
        Returns the number of objects in the Percentiles class instance.
        
        Parameter/s: None
        Return case: int - the number of objects in the Percentiles class instance
        
        Worst-case complexity: O(1)
        Best-case complexity: O(1)
        """

        return len(self.tree)