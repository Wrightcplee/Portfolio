from __future__ import annotations

from mountain import Mountain
from double_key_table import DoubleKeyTable
from algorithms.mergesort import mergesort, merge

class MountainOrganiser:

    def __init__(self) -> None:
        """
        Initialisation.
        self.mountains for mountains in table format, dict in format: (K1: length, K2: name, V: rank)
        self.sorted_mountaints: list[Mountains] in sorted form

        Complexity: O(1)
        """
        self.mountains = DoubleKeyTable()
        self.sorted_mountains: list[Mountain] = []

    def cur_position(self, mountain: Mountain) -> int:
        """
        Returns current rank of mountains amongst all mountains

        Arguments: mountain (Mountain which you want its rank)
        Returns: int (Rank of the Mountain)

        Complexity: O(1)
        """
        return self.mountains[str(mountain.length), mountain.name]

    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        Add a list of mountains. Stores the rank as the value.

        Arguments: mountains (list of Mountains you want to add)
        Best/Worse Case Complexity: O(Mlog(M) + N) where M is the length of input list, 
                                    and N is the total number of mountains included so far.
        """
        self.sorted_mountains = merge(self.sorted_mountains, mergesort(mountains))
        for i, mountain in enumerate(self.sorted_mountains):
            self.mountains[str(mountain.length), mountain.name] = i