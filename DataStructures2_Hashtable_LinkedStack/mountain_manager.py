from mountain import Mountain
from double_key_table import DoubleKeyTable
from algorithms.mergesort import mergesort

class MountainManager:

    def __init__(self) -> None:
        """
        Initialises table for all mountains.

        Complexity: O(1)
        """
        self.mountains = DoubleKeyTable()

    def add_mountain(self, mountain: Mountain) -> None:
        """
        Add a mountain to the manager.

        Arguments: mountain (Mountain you want to add)
        Complexity: O(1)
        """
        self.mountains[str(mountain.difficulty_level), mountain.name] = mountain

    def remove_mountain(self, mountain: Mountain) -> None:
        """
        Remove a mountain from the manager.

        Arguments: mountain (Mountain you want to remove)
        Complexity: O(1)
        """
        del self.mountains[str(mountain.difficulty_level), mountain.name]

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        """
        Remove old mountain and add new ones.

        Arguments: old (Mountain you want to remove)
                   new (Mountain you want to add)
        Complexity: O(1)
        """
        self.remove_mountain(old)
        self.add_mountain(new)

    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        """
        A list of all mountains of a particular difficulty

        Arguments: diff (difficulty level of the mountain)
        Returns: list of Mountains of "diff" diffculty
        Complexity: O(1)
        """
        return self.mountains.values(str(diff))

    def group_by_difficulty(self) -> list[list[Mountain]]:
        """
        A list of list of all mountains, grouped and sorted by difficulty in ascending order

        Returns: As stated above
        Best/Worst Case Complexity: O(klog(k)+k), k = number of keys
        """
        result = []
        difficulty_levels = mergesort(self.mountains.keys())
        for i in difficulty_levels:
            result.append(self.mountains.values(i))
        return result