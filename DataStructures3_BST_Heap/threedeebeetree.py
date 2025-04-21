from __future__ import annotations
from typing import Generic, TypeVar, Tuple
from dataclasses import dataclass, field

I = TypeVar('I')
Point = Tuple[int, int, int]

@dataclass
class BeeNode:

    key: Point
    item: I = None
    subtree_size: int = 1
    octants: list[BeeNode|None] = field(default_factory= lambda: [None]*8)
    # Ordered in terms of x,y,z: [---, --+, -+-, -++, +--, +-+, ++-, +++]

    def get_child_for_key(self, point: Point) -> BeeNode | None:
        """
        Retrieve the child node for a particular point.

        Arguments: point - reference Point of which octant the child is
        Returns: BeeNode of child

        Complexity: O(1)
        """
        return self.octants[self.get_octant_index(point)]

    def get_octant_index(self, point: Point) -> int:
        """
        Returns the index of the octants for a particular point.

        Arguments: reference point of which octant it lies in
        Returns: int of the octant

        Complexity: O(1)
        """
        index = 0
        if point[0] >= self.key[0]:
            index += 4
        if point[1] >= self.key[1]:
            index += 2
        if point[2] >= self.key[2]:
            index += 1
        return index

class ThreeDeeBeeTree(Generic[I]):
    """ 3️⃣🇩🐝🌳 tree. """

    def __init__(self) -> None:
        """
            Initialises an empty 3DBT
        """
        self.root = None
        self.length = 0

    def is_empty(self) -> bool:
        """
            Checks to see if the 3DBT is empty
        """
        return len(self) == 0

    def __len__(self) -> int:
        """ Returns the number of nodes in the tree. """

        return self.length

    def __contains__(self, key: Point) -> bool:
        """
            Checks to see if the key is in the 3DBT
        """
        try:
            self.get_tree_node_by_key(key)
            return True
        except KeyError:
            return False

    def __getitem__(self, key: Point) -> I:
        """
        Attempts to get an item in the tree, it uses the Key to attempt to find it
        
        Arguments: key in the form of a Point
        Returns: item of the corresponding key

        Best Complexity: O(CompK) item in the root of the tree
        Worst Complexity: O(CompK*D) where D is the depth of the tree
            where CompN is the comparision of key
        """
        node = self.get_tree_node_by_key(key)
        return node.item

    def get_tree_node_by_key(self, key: Point) -> BeeNode:
        return self.get_tree_node_by_key_aux(self.root, key)
    
    def get_tree_node_by_key_aux(self, current: BeeNode, key: Point) -> BeeNode:
        if current is None:
            raise KeyError(f"Key not found: {key}")
        elif key == current.key:
            return current
        else:
            return self.get_tree_node_by_key_aux(current.get_child_for_key(key), key)

    def __setitem__(self, key: Point, item: I) -> None:
        """
        Attempts to insert an item into the tree, it uses the Key to insert it
        Also updates the node's subtree size

        Arguments: key and item of the Node you want to insert

        Best Complexity: O(CompK) inserts the item at the root.
        Worst Complexity: O(CompK * D) inserts at the bottom of the tree where D is the depth of the tree
            where CompK is the complexity of comparing the keys
        """
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: BeeNode, key: Point, item: I) -> BeeNode:
        if current is None:
            current = BeeNode(key, item)
            self.length += 1
        elif key == current.key:
            raise ValueError("Inserting duplicate item")
        else:
            current.octants[current.get_octant_index(key)] = self.insert_aux(current.get_child_for_key(key), key, item)
            current.subtree_size += 1
        return current

    def is_leaf(self, current: BeeNode) -> bool:
        """ Simple check whether or not the node is a leaf. """
        return any(current.octants)

if __name__ == "__main__":
    tdbt = ThreeDeeBeeTree()
    tdbt[(3, 3, 3)] = "A"
    tdbt[(1, 5, 2)] = "B"
    tdbt[(4, 3, 1)] = "C"
    tdbt[(5, 4, 0)] = "D"
    print(tdbt.root.get_child_for_key((4, 3, 1)).subtree_size) # 2