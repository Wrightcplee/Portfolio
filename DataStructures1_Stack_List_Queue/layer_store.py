from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer

from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.bset import BSet
from data_structures.sorted_list_adt import ListItem
from data_structures.array_sorted_list import ArraySortedList
from layers import invert
from layer_util import LAYERS, cur_layer_index

class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    def __init__(self) -> None:
        """
        Instant variables layer store and invert.
        self.layer_store: the current layer it has
        self.invert: bool based on special function
        Complexity: O(1)
        """
        self.layer_store = None
        self.invert = False
    
    def add(self, layer: Layer) -> bool:
        """
        Changes the LayerStore if it is different from the current one.

        Args:
        - layer: effects in class Layer

        Returns:
        - True if LayerStore is changed

        Complexity: O(1)
        """
        if self.layer_store != layer:
            self.layer_store = layer
            return True
        return False

    def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns the color after going through the LayerStore.

        Args:
        - start: color being inputted into the LayerStore
        - timestamp, x, y: int value for Layer effects

        Returns:
        Output color after going through the LayerStore

        Complexity: O(1)
        """
        color = start
        if self.layer_store:
            color = self.layer_store.apply(color, timestamp, x, y)
        if self.invert:
            color = invert.apply(color, timestamp, x, y)
        return color

    def erase(self, layer: Layer) -> bool:
        """
        Removes the LayerStore if it has a Layer.

        Args:
        - layer: effects in class Layer

        Returns:
        - True if LayerStore has a Layer

        Complexity: O(1)
        """
        if self.layer_store:
            self.layer_store = None
            return True
        return False

    def special(self) -> None:
        """
        Sets/reverses the LayerStore to invert the grid.
        Complexity: O(1)
        """
        if self.invert:
            self.invert = False
        else:
            self.invert = True

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    
    def __init__(self) -> None:
        """
        Instantiate LayerStore to be a CircularQueue
        Complexity: O(1)
        """
        self.layer_store = CircularQueue(100*cur_layer_index)

    def add(self, layer: Layer) -> bool:
        """ 
        Adds a Layer to the current LayerStore.

        Args:
        - layer: effects in class Layer

        Returns:
        - True if LayerStore is changed

        Complexity: O(1)
        """
        if not self.layer_store.is_full():
            self.layer_store.append(layer)
            return True
        return False

    def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns a color after going through all Layers in the LayerStore.

        Args:
        - start: color being inputted into the LayerStore
        - timestamp, x, y: int value for Layer effects

        Returns:
        Output color after going through the LayerStore

        Complexity: O(len(self.layer_store))
        """
        color = start
        for i in range(len(self.layer_store)):
            layer = self.layer_store.serve()
            color = layer.apply(color, timestamp, x, y)
            self.layer_store.append(layer)
        return color

    def erase(self, layer: Layer) -> bool:
        """
        Removes the oldest Layer in the Queue.

        Args:
        - layer: effects in class Layer

        Returns:
        - True if LayerStore has a Layer

        Complexity: O(1)
        """
        if not self.layer_store.is_empty():
            self.layer_store.serve()
            return True
        return False

    def special(self) -> None:
        """
        Reverses the LayerStore.
        Complexity: O(2*len(self.layer_store))
        """
        reverse = ArrayStack(100)
        while len(self.layer_store) > 0:
            reverse.push(self.layer_store.serve())
        while len(reverse) > 0:
            self.layer_store.append(reverse.pop())

class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """
    def __init__(self) -> None:
        """
        Instantiate self.layer_store with a BitVector set based on number of layers available in LAYERS.
        Complexity: O(1)
        """
        self.layer_store = BSet(cur_layer_index)

    def add(self, layer: Layer) -> bool:
        """
        Activate the Layer in the LayerStore if not activated.

        Args:
        - layer: effects in class Layer

        Returns:
        - True if LayerStore is changed

        Complexity: O(1)
        """
        if layer.index+1 not in self.layer_store:
            self.layer_store.add(layer.index+1)
            return True
        return False
            
    def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns a color after going through the LayerStore.
        Applies changes in increasing order.

        Args:
        - start: color being inputted into the LayerStore
        - timestamp, x, y: int value for Layer effects

        Returns:
        Output color after going through the LayerStore
        
        Complexity: O(cur_layer_index)
        """
        color = start
        for i in range(cur_layer_index):
            if LAYERS[i].index+1 in self.layer_store:
                color = LAYERS[i].apply(color, timestamp, x, y)
        return color

    def erase(self, layer: Layer) -> bool:
        """
        Deactivate the Layer if activated.

        Args:
        - layer: effects in class Layer

        Returns:
        - True if a Layer has been removed 

        Complexity: O(1)
        """
        if layer.index+1 in self.layer_store:
            self.layer_store.remove(layer.index+1)
            return True
        return False
    
    def special(self) -> None:
        """
        Removes the median lexicographically ordered Layer based on the name of the Layer, 
        lexicographically smaller one if there is an even number of Layer activated.
        
        Best Case Complexity: O(cur_layer_index*log(len(self.layer_store))) 
            when adding gives O(log(len(self.layer_store))), if item added in layer_list is last
        Worst Case Complexity: O(cur_layer_index*len(self.layer_store))
            when adding gives O(len(self.layer_store)), if item added in layer_list is first
        """
        layer_list = ArraySortedList(cur_layer_index)
        for i in range(cur_layer_index):
            if LAYERS[i].index+1 in self.layer_store:
                layer_list.add(ListItem(i, LAYERS[i].name))
        if len(layer_list) != 0:
            if len(self.layer_store) % 2 != 0:
                self.layer_store.remove(layer_list[len(self.layer_store)//2].value+1)
            else:
                if layer_list[len(self.layer_store)//2-1].key < layer_list[len(self.layer_store)//2].key:
                    smaller = layer_list[len(self.layer_store)//2-1]
                else:
                    smaller = layer_list[len(self.layer_store)//2]
                self.layer_store.remove(smaller.value+1)