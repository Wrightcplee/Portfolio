from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.
    """

    TABLE_SIZE = 27

    def __init__(self) -> None:
        """
        __init__
        
        Initialises the Infinte Hash Table.
        
        Parameter/s: None
        Return case: None
        
        Worst-case complexity: O(1)
        Best-case complexity: O(1)
        """
        
        self.array = ArrayR(self.TABLE_SIZE)

        for i in range(self.TABLE_SIZE):
            self.array[i] = []

        self.level = 0
        self.count = 0

    def hash(self, key: K) -> int:
        """
        hash
        
        Hashes a key for insert into the Infinite Hash Table.
        
        Parameter/s: key - the key to hash
        Return case: int - the position at which to insert
        
        Worst-case complexity: O(1)
        Best-case complexity: O(1)
        """
        
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        __getitem__

        Get the value at a certain key.

        Parameter/s: key - the key which corresponds to the desired value
        Return case: V - the desired value
                     KeyError - if the key isn't represented in the Infinite Hash Table

        Worst-case complexity: O(n), where n is the depth of the Hash Table which the (key, value) pair is in.
        Best-case complexity: O(n), where n is the depth of the Hash Table which the (key, value) pair is in.
        """

        location = self.get_location(key)

        position = self.array[location[0]]

        for i in range(1, len(location) - 1):
            position = position[1][location[i]]

        return position[1]

    def __setitem__(self, key: K, value: V) -> None:
        """
        __setitem__

        Set an (key, value) pair in our hash table.

        Parameter/s: key - the key which corresponds to the value, value - the data which to set
        Return case: None

        Worst-case complexity: O(n + N + z * N), where n is the depth of the Hash Table 
                               which there is first a (key, value) pair and not a (key, Hash Table) 
                               which corresponds to the key's position and 
                               N is the table size of the Hash Table and 
                               z is the number of new Hash Tables to be generated corresponding to the key's position.
        Best-case complexity: O(1)
        """

        self.level = 0
        position = [self.hash(key)]
        keyAndValue = self.array[position[self.level]]

        if keyAndValue == []:
            self.array[position[self.level]] = [key, value]
            self.count += 1
            return

        while isinstance(keyAndValue[1], ArrayR):
            self.level += 1
            position.append(self.hash(key))
            keyAndValue = keyAndValue[1][position[self.level]]

            if keyAndValue == []:
                keyAndValue.append(key)
                keyAndValue.append(value)
                self.count += 1
                return


        if keyAndValue == key:
            keyAndValue = [key, value]
        else:
            oldKeyAndValue = []
            oldKeyAndValue.append(keyAndValue[0])
            oldKeyAndValue.append(keyAndValue[1])

            keyAndValue[0] = key[0:self.level + 1]
            keyAndValue[1] = ArrayR(self.TABLE_SIZE)

            for i in range(self.TABLE_SIZE):
                keyAndValue[1][i] = []

            self.level += 1

            oldPosition = self.hash(oldKeyAndValue[0])
            newPosition = self.hash(key)

            while oldPosition == newPosition:
                keyAndValue[1][oldPosition].append(key[0:self.level + 1])
                keyAndValue[1][oldPosition].append(ArrayR(self.TABLE_SIZE))

                for i in range(self.TABLE_SIZE):
                    keyAndValue[1][oldPosition][1][i] = []

                keyAndValue = keyAndValue[1][oldPosition]

                self.level += 1

                oldPosition = self.hash(oldKeyAndValue[0])
                newPosition = self.hash(key)


            keyAndValue[1][oldPosition] = oldKeyAndValue
            keyAndValue[1][newPosition] = [key, value]

            self.count += 1

    def __delitem__(self, key: K) -> None:
        """
        __delitem__

        Deletes a (key, value) pair in our hash table.

        Parameter/s: key - the key that corresponds to the value which to delete
        Return case: KeyError - if the key isn't represented in the Infinite Hash Table

        Worst-case complexity: O(n + N + z * (n + N)), where n is the depth of the Hash Table 
                               which the (key, value) pair is in and 
                               N is the table size and 
                               z is the number of Hash Tables which must be collapsed.
        Best-case complexity: O(n), where n is the depth of the Hash Table which the (key, value) pair is in.
        """

        location = self.get_location(key)
        keyAndValue = self.array[location[0]]

        for i in range(1, len(location)):
            keyAndValue = keyAndValue[1][location[i]]
        
        keyAndValue.pop()
        keyAndValue.pop()

        self.count -= 1

        location.pop()
        if len(location) == 0:
            return
        
        keyAndValue = self.array[location[0]]
        
        for i in range(1, len(location)):
            keyAndValue = keyAndValue[1][location[i]]
        
        count = 0
        for i in range(self.TABLE_SIZE):
            if keyAndValue[1][i] != []:
                if isinstance(keyAndValue[1][i][1], ArrayR):
                    count = 27
                    break
                count += 1
                oldKeyAndValue = keyAndValue[1][i]

        if count > 1:
            return

        while count < 2:
            keyAndValue.pop()
            keyAndValue.pop()

            location.pop()
            if len(location) == 0:
                break

            keyAndValue = self.array[location[0]]

            for i in range(1, len(location)):
                keyAndValue = keyAndValue[1][location[i]]

            count = 0
            for i in range(self.TABLE_SIZE):
                if keyAndValue[1][i] != []:
                    if isinstance(keyAndValue[1][i][1], ArrayR):
                        count = 27
                        break
                    count += 1

        keyAndValue.append(oldKeyAndValue[0])
        keyAndValue.append(oldKeyAndValue[1])           
                

    def __len__(self) -> int:
        """
        __len__
        
        Returns the number of elements in the Infinite Hash Table.
        
        Parameter/s: None
        Return case: int - the number of elements in the Infinite Hash Table
        
        Worst-case complexity: O(1)
        Best-case complexity: O(1)
        """
        
        return self.count

    def __str__(self) -> BaseException:
        """
        __str__

        Returns NotImplementedError.

        Parameter/s: None
        Return case: BaseException - NotImplementedError

        Worst-case complexity: O(1)
        Best-case complexity: O(1)
        """

        raise NotImplementedError()

    def get_location(self, key) -> list:
        """
        get_location

        Get the sequence of positions required to access this key.

        Parameter/s: the key which to get the position sequence for
        Return case: list - an ordered list representing the position sequence
                     KeyError - if the key isn't represented in the Infinte Hash Table

        Worst-case complexity: O(n), where n is the depth of the Hash Table which the (key, value) pair is in.
        Best-case complexity: O(1)
        """

        self.level = 0
        location = [self.hash(key)]
        keyAndValue = self.array[location[0]]

        if keyAndValue == []:
            raise KeyError(key)

        while isinstance(keyAndValue[1], ArrayR):
            self.level += 1
            position = self.hash(key)
            keyAndValue = keyAndValue[1][position]
            location.append(position)

            if keyAndValue == []:
                return location
        
        if keyAndValue[0] == key:
            return location
        else:
            raise KeyError(key)

    def __contains__(self, key: K) -> bool:
        """
        __contains__

        Checks to see if the given key is in the Hash Table

        Parameter/s: key - the key being checked
        Return case: bool - True if the key is represented in the Infinite Hash Table 
                            and False if it is not

        Worst-case complexity: See __getitem__
        Best-case complexity: See __getitem__
        """

        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True
