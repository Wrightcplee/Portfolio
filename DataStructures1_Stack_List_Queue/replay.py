from __future__ import annotations
from action import PaintAction
from grid import Grid

from data_structures.queue_adt import CircularQueue

class ReplayTracker:

    """
    Tracks every action that can be replayed.
    """

    def __init__(self) -> None:
        """
        Initialises the tracker. Action taken is stored in self.replay_tracker.
        Complexity: O(1) 
        """
        self.replay_tracker = CircularQueue(10000)

    def start_replay(self) -> None:
        """
        Called whenever we should stop taking actions, and start playing them back.

        Useful if you have any setup to do before `play_next_action` should be called.
        """
        pass

    def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
        """
        Adds an action to the replay.

        `is_undo` specifies whether the action was an undo action or not.
        Special, Redo, and Draw all have this is False.

        Args:
        - action: a series of PaintStep or bool if the action is special
        - is_undo: bool if the action is an undo

        Complexity: O(1)
        """
        if not self.replay_tracker.is_full():
            self.replay_tracker.append((action, is_undo))

    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.
        Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.

        Args:
        - grid: class Grid to be applied on

        Returns:
        - True if the replay is finished
            
        Complexity: O(PaintAction.undo_apply() or PaintAction.redo_apply())
        """
        if not self.replay_tracker.is_empty():
            replay = self.replay_tracker.serve()
            if replay[1]:
                replay[0].undo_apply(grid)
            else:
                if replay[0]:
                    replay[0].redo_apply(grid)
            return False
        return True

if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g) # action 1, special
    f2 = r.play_next_action(g) # action 2, draw
    f3 = r.play_next_action(g) # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)

