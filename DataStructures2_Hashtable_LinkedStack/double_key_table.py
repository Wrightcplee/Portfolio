from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import *
from data_structures.referential_array import ArrayR
from iterator import ListIterator

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes: list | None = None, internal_sizes: list | None = None) -> None:
        """
        __init__

        initialises the Double Key Hash Table.

        Parameter/s: sizes - possible sizes of the top Hash Table
                     internal_sizes - possible sizes of the bottom Hash Tables
        Return case: None

        Worst-case complexity: O(1)
        Best-case complexity: O(1)
        """
        
        if sizes is not None:
            self.TABLE_SIZES = sizes

        self.internal_sizes = internal_sizes
        self.size_index = 0
        self.count = 0

        self.array:ArrayR[tuple[K1,V]] = ArrayR(self.TABLE_SIZES[self.size_index])

        self.keyIterators = []
        self.valueIterators = []

    def hash1(self, key: K1) -> int:
        """
        hash1

        Hash the 1st key for insert/retrieve/update into the hashtable.

        Parameter/s: key - the key which to hash
        Return case: int - the hash

        Time complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        hash2

        Hash the 2nd key for insert/retrieve/update into the hashtable.

        Parameter/s: key - the key which to hash
                     sub_table - the Hash Table which to invoke the hash on
        Return case: int - the hash

        Time complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        _linear_probe

        Search and return the position within the Double Key Hash Table which the two keys correspond to, using linear probing.

        Parameter/s: key1 - the top Hash Table key
                     key2 -  the bottom Hash Table key
                     is_insert - a boolean describing the user's intent to insert an item corresponding to the two keys.
        Return case: tuple[int, int] - a tuple describing the position that the two keys correspond to
                     KeyError - if the key pair is not represented within the Double Key Hash Table and is_insert is False
                     FullError - if the Double Key Hash Table is full.

        Worst-case complexity: O(hash1(key) + n * COMP(K) + hash2(key) + N * COMP(K)), 
                               where n is the table size of the top Hash Table and 
                               N is the table size of the bottom Hash Table.
        Best-case complexity: O(hash1(key) + hash2(key))
        """

        position1 = self.hash1(key1) # Initial position in the top Hash Table.
        fullTopTable = True

        for i in range(self.table_size):
            if self.array[position1] is None:
                if is_insert:
                    table = LinearProbeTable(self.internal_sizes)
                    table.hash = lambda k: self.hash2(k, table)
                    self.array[position1] = (key1, table)
                    self.count += 1
                    fullTopTable = False
                    break
                else:
                    raise KeyError(key1)
            elif self.array[position1][0] == key1:
                fullTopTable = False
                break
            else:
                position1 = (position1 + 1) % self.table_size

        if fullTopTable:
            if is_insert:
                raise FullError("Top Hash Table is full!")
            else:
                raise KeyError(key1)
        
        position2 = self.array[position1][1]._linear_probe(key2, is_insert)

        return (position1, position2)

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        iter_keys

        Returns all keys in an Iterator within the desired Hash Table.

        Parameter/s: key - the key which corresponds to the desired bottom Hash Table 
                     (if key is None, the top Hash Table has its keys returned in an Iterator)
        Return case: Iterator - an Iterator of the keys within the desired Hash Table
        
        Worst-case time complexity: O(n + N), where n is the size of the top Hash Table
                                    and N is the size of the bottom Hash Table.
        Best-case time complexity: O(n), where n is the table size of the top Hash Table.
        """

        iterator = ListIterator(self.keys(key), 0, key)

        self.keyIterators.append(iterator)

        return iterator

    def keys(self, key: K1 | None = None) -> list[K1]:
        """
        keys

        Returns all keys within the desired Hash Table.

        Parameter/s: key - the key which corresponds to the desired bottom Hash Table 
                     (if key is None, the top Hash Table has its keys returned)
        Return case: list - a list of the keys within the desired Hash Table
        
        Worst-case time complexity: O(n + N), where n is the size of the top Hash Table 
                                    and N is the size of the bottom Hash Table.
        Best-case time complexity: O(n), where n is the table size of the top Hash Table.
        """

        result = []
        
        if key is None:
            for i in range(self.table_size):
                if self.array[i] is not None:
                    result.append(self.array[i][0])  
            return result
        
        position = self.hash1(key)

        for i in range(self.table_size):
            if self.array[position] is None:
                return result
            elif self.array[position][0] == key:
                return self.array[position][1].keys()
            else:
                position = (position + 1) % self.table_size

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        iter_values

        Returns all values in an Iterator within the desired Hash Table.

        Parameter/s: key - the key which corresponds to the desired bottom Hash Table 
                     (if key is None, then all values in all Bottom Hash Tables are returned in an Iterator)
        Return case: Iterator - a Iterator of the values within the desired Hash Table

        Worst-case time complexity: O(n + N), where n is the size of the top Hash Table 
                                    and N is the size of the bottom Hash Table.
        Best-case time complexity: O(n), where n is the table size of the top Hash Table.
        """

        iterator = ListIterator(self.values(key), 0, key)

        self.valueIterators.append(iterator)

        return iterator

    def values(self, key: K1 | None = None) -> list[V]:
        """
        values

        Returns all values within the desired Hash Table.

        Parameter/s: key - the key which corresponds to the desired bottom Hash Table 
                     (if key is None, then all values in all Bottom Hash Tables are returned)
        Return case: list - a list of the values within the desired Hash Table

        Worst-case time complexity: O(n + N), where n is the size of the top Hash Table 
                                    and N is the size of the bottom Hash Table.
        Best-case time complexity: O(n), where n is the table size of the top Hash Table.
        """

        result = []
        
        if key is None:
            for i in range(self.table_size):
                if self.array[i] is not None:
                    values = self.array[i][1].values()
                    for i in range(len(values)):
                        result.append(values[i])
            return result
        
        position = self.hash1(key)

        for i in range(self.table_size):
            if self.array[position] is None:
                return result
            elif self.array[position][0] == key:
                return self.array[position][1].values()
            else:
                position = (position + 1) % self.table_size

    def __contains__(self, key: tuple[K1, K2]) -> bool:
        """
        contains

        Checks to see if the given key pair is represented in the Hash Table.

        Parameter/s: key - the key pair being checked
        Return case: bool - True if the key pair is represented, False elsewise

        Time complexity: See linear probe.
        """
        
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        __getitem__

        Get the value at a certain key

        Parameter/s: key - the keys which correspond to the item's location within the Double Key Hash Table
        Return case: V - the item, KeyError - when the key does not exist

        Worst-case complexity: See _linear_probe
        Best-case complexity: See _linear_probe
        """

        position = self._linear_probe(key[0], key[1], False)

        return self.array[position[0]][1].array[position[1]][1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        __setitem__

        Sets an item within the Double Key Hash Table as a value corresponding to two keys.

        Parameter/s: key - the keys which correspond to the item's location within the Double Key Hash Table
                     data - the value which the item will hold.
        Return case: None

        Worst-case complexity: See _linear_probe
        Best-case complexity: See _linear_probe
        """

        position = self._linear_probe(key[0], key[1], True)

        self.array[position[0]][1][key[1]] = data

        if self.count > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        __delitem__

        Removes a (key, value) pair from the Double Key Hash Table.

        Parameter/s: key - the keys which correspond to the item's location within the Double Key Hash Table.
        Return case: KeyError - when the key doesn't exist

        Worst-case complexity: O(hash1(key) + n * COMP(K) + hash2(key) + N * COMP(K) + n + z + Z), 
                               where n is the table size of the top Hash Table and 
                               N is the table size of the bottom Hash Table and 
                               z is len(keyIterators) and Z is len(valueIterators).
        Best-case complexity: O(hash1(key) + hash2(key))
        """
        
        position = self._linear_probe(key[0], key[1], False)

        del self.array[position[0]][1][key[1]]

        if self.array[position[0]][1].is_empty():
            self.array[position[0]] = None

            oldArray = self.array
            self.array = ArrayR(self.TABLE_SIZES[self.size_index])
            self.count = 0

            for item in oldArray:
                if item is not None:
                    position = self.hash1(item[0])
                    for i in range(len(oldArray)):
                        if self.array[position] is None:
                            self.array[position] = item
                            self.count += 1
                            break
                        else:
                            position = (position + 1) % len(oldArray)
                
        for i in range(len(self.keyIterators) - 1):
            iterator = self.keyIterators[i]

            iterator = ListIterator(self.keys(iterator.key), iterator.index, iterator.key)

        for i in range(len(self.valueIterators) - 1):
            iterator = self.valueIterators[i]

            iterator = ListIterator(self.values(iterator.key), iterator.index, iterator.key)

    def _rehash(self) -> None:
        """
        _rehash

        Resizes the Double Key Hash Table and reinserts all appropriate values.

        Parameter/s: None
        Return case: None

        Worst-case complexity: O(n * (n + hash1(key))), where n is the table size of the top Hash Table.
        Best-case complexity: O(1)
        """
        
        self.size_index += 1

        if self.size_index == len(self.TABLE_SIZES): # If there are no more greater sizes to resize to in TABLE_SIZES.
            return
    
        oldArray = self.array
        self.array = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0

        for item in oldArray:
            if item is not None:
                position = self.hash1(item[0])
                for i in range(len(oldArray)):
                    if self.array[position] is None:
                        self.array[position] = item
                        self.count += 1
                        break
                    else:
                        position = (position + 1) % len(oldArray)

    @property
    def table_size(self) -> int:
        """
        table_size

        Returns the size of the top Hash Table.

        Parameter/s: None
        Return case: int - the size of the top Hash Table.

        Worst-case complexity: O(1)
        Best-case complexity: O(1)
        """
        
        return len(self.array)

    def __len__(self) -> int:
        """
        __len__

        Returns the total number of elements in the bottom Hash Tables.

        Parameter/s: None
        Return case: int - the total number of elements in the bottom Hash Tables

        Worst-case complexity: O(n), where n is the number of elements in the bottom Hash Tables.
        Best-case complexity: O(1)
        """
        length = 0

        for i in range(self.table_size):
            if self.array[i] is not None:
                length += len(self.array[i][1])

        return length

    def __str__(self) -> BaseException:
        """
        __str__

        Returns NotImplementedtError.

        Parameter/s: None
        Return case: BaseException - NotImplementedError

        Worst-case complexity: O(1)
        Best-case complexity: O(1)
        """
        
        raise NotImplementedError()