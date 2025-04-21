from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain

from typing import TYPE_CHECKING, Union

from data_structures.linked_stack import LinkedStack

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        return TrailSeries(self.path_follow.store.mountain, self.path_follow.store.following)

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """Removes the mountain at the beginning of this series."""
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""
        return TrailSeries(mountain, Trail(TrailSeries(self.mountain, self.following)))

    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        return TrailSplit(Trail(None), Trail(None), Trail(TrailSeries(self.mountain, self.following)))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""
        return TrailSeries(self.mountain, Trail(TrailSeries(mountain, self.following)))

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        return TrailSeries(self.mountain, Trail(TrailSplit(Trail(None), Trail(None), self.following)))

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
        return Trail(TrailSeries(mountain, Trail(self.store)))

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        return Trail(TrailSplit(Trail(None), Trail(None), Trail(self.store)))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """
        Follow a path and add mountains according to a personality.
        
        Arguments: personality (Type of WalkerPersonality you want)
        Complexity: O(number of Trails traversed)
        """
        stack = LinkedStack()
        stack.push(self.store)
        while not stack.is_empty():
            path = stack.pop()
            if isinstance(path, TrailSplit):
                stack.push(path.path_follow.store)
                if personality.select_branch(path.path_top, path.path_bottom):
                    stack.push(path.path_top.store)
                else:
                    stack.push(path.path_bottom.store)
            elif isinstance(path, TrailSeries):
                personality.add_mountain(path.mountain)
                stack.push(path.following.store)
        
    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        lst = []
        if isinstance(self.store, TrailSplit):
            lst += self.store.path_top.collect_all_mountains()
            lst += self.store.path_bottom.collect_all_mountains()
            lst += self.store.path_follow.collect_all_mountains()
        elif isinstance(self.store, TrailSeries):
            lst.append(self.store.mountain)
            lst += self.store.following.collect_all_mountains()
        return lst

    def length_k_paths(self, k: int|None) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        if isinstance(self.store, TrailSeries):
            following_path = self.store.following.length_k_paths(None)
            for lst in following_path:
                lst.insert(0, self.store.mountain)
            mountain_list = following_path
        elif isinstance(self.store, TrailSplit):
            top_path = self.store.path_top.length_k_paths(None)
            bottom_path = self.store.path_bottom.length_k_paths(None)
            follow_path = self.store.path_follow.length_k_paths(None)
            for _ in range(len(follow_path)-1):
                top_path += top_path
                bottom_path += bottom_path
            for i, lst in enumerate(top_path):
                top_path[i] = lst + follow_path[i%len(follow_path)]
            for i, lst in enumerate(bottom_path):
                bottom_path[i] = lst + follow_path[i%len(follow_path)]
            mountain_list = top_path + bottom_path
        else:
            return [[]]
        if k is None:
            return mountain_list
        return [lst for lst in mountain_list if len(lst) == k] 
            
