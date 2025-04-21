from __future__ import annotations
from dataclasses import dataclass
from heap import MaxHeap

@dataclass
class Beehive:
    """A beehive has a position in 3d space, and some stats."""

    x: int
    y: int
    z: int

    capacity: int
    nutrient_factor: int
    volume: int = 0

    def __lt__(self, other: Beehive) -> bool:
        """
        Comparison magic method based on emeralds for "<" or ">"
        Complexity: O(1)
        """
        return min(self.capacity, self.volume) * self.nutrient_factor \
              < min(other.capacity, other.volume) * other.nutrient_factor
    
    def __le__(self, other: Beehive) -> bool:
        """
        Comparison magic method based on emeralds for "<=" or ">="
        Complexity: O(1)
        """
        return min(self.capacity, self.volume) * self.nutrient_factor \
            <= min(other.capacity, other.volume) * other.nutrient_factor
    
    def __eq__(self, other: Beehive) -> bool:
        """
        Comparison magic method based on emeralds for "=="
        Complexity: O(1)
        """
        return min(self.capacity, self.volume) * self.nutrient_factor \
            == min(other.capacity, other.volume) * other.nutrient_factor

class BeehiveSelector:
  
    """A selection of Beehives to pick from"""

    def __init__(self, max_beehives: int) -> None:
        """
        Initialises the selector

        Arguments: max_beehives - maximum number of beehives in selector

        Complexity: O(1)
        """
        self.beehive = MaxHeap(max_beehives)

    def set_all_beehives(self, hive_list: list[Beehive]) -> None:
        """
        Replaces all current beehives in selector with those in hive_list

        Arguments: hive_list - list of Beehive to be added in BeehiveSelector

        Complexity: O(len(hive_list))
        """
        self.beehive.heapify(hive_list)
    
    def add_beehive(self, hive: Beehive) -> None:
        """
        Adds Beehive to selector

        Arguments: hive - Beehive to be added

        Complexity: O(log(len(number of beehive in selector)))
        """
        self.beehive.add(hive)
    
    def harvest_best_beehive(self) -> float:
        """
        Harvests the honey from the best beehive. Reduces the volume of the beehive after harvest.

        Returns: number of emeralds in float

        Complexity: O(log(len(number of beehive in selector)))
        """
        res = self.beehive.get_max()
        emerald = min(res.volume, res.capacity) * res.nutrient_factor
        res.volume = max(0, res.volume-res.capacity)
        self.beehive.add(res)
        return emerald