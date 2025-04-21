from __future__ import annotations
from typing import TypeVar

V = TypeVar("V")

class ListIterator:
    """
    ListIterator

    A class to represent an Iterator for in-built Python lists.
    """
    
    def __init__(self, data : list, index : int | None, key : str) -> None:
        """
        __init__
        
        Initialises the Iterator.
        
        Parameter/s: data - the list, index - the index at which to begin iteration
                     key - the key associated with the Hash Table
        Return case: BaseException - if the list is empty.
        
        Worst-case complexity: O(1)
        Best-case complexity: O(1)
        """

        self.data = data
        
        if index is None:
            index = 0
        self.index = index

        self.key = key

        self.previous = None
        
        try:
            self.current = self.data[self.index]
        except:
            raise BaseException("List entered into ListIterator is empty!")

    def __iter__(self):
        """
        __iter__
        
        Returns the object of the Iterator.
        
        Parameter/s: None
        Return case: ListIterator - the object of the Iterator
        
        Worst-case complexity: O(1)
        Best-case complexity: O(1)
        """

        return self

    def __next__(self) -> V:
        """
        __next__
        
        Iterates the list.
        
        Parameter/s: None
        Return case: V - the element in the list which was iterated over
        
        Worst-case complexity: O(1)
        Best-case complexity: O(1)
        
        """
        if self.has_next():
            self.index += 1

            self.previous = self.current
            self.current = self.data[self.index]
            return self.previous
        else:
            raise StopIteration
        
    def has_next(self) -> bool:
        """
        has_next
        
        Returns a boolean value describing whether the list can be iterated further or not.
        
        Parameter/s: None
        Return case: bool - True if the list can be iterated further
                            False if the list cannot be iterated further

        Worst-case complexity: O(1)
        Best-case complexity: O(1)
        """

        return self.current is not None