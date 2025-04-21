from __future__ import annotations
from action import PaintAction
from grid import Grid

from data_structures.stack_adt import ArrayStack

class UndoTracker:

    """
    Tracks every action made by user that can be undo-ed and redo-ed.
    """

    def __init__(self) -> None:
        """
        Initialises the tracker. Action taken is stored in self.action_list.
        Any action undo-ed is stored in self.undo_list. Will only be used when user undoes something, 
        and cleared when new action is taken. Used for redo.

        Complexity: O(1) 
        """
        self.action_list = ArrayStack(10000)
        self.undo_list = None

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.

        Args:
        - action: a series of PaintStep or bool if the action is special

        Complexity: O(1)
        """
        if not self.action_list.is_full():
            self.action_list.push(action)
        self.undo_list = None

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        Args:
        grid: class Grid to be applied on

        Return: 
        - The action that was undone, or None.

        Complexity: O(PaintAction.undo_apply())
        """
        if self.action_list.is_empty():
            return None
        if not self.undo_list:
            self.undo_list = ArrayStack(10000)
        undo_action = self.action_list.pop()
        self.undo_list.push(undo_action)
        undo_action.undo_apply(grid)
        return undo_action

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.
        
        Args:
        - grid: class Grid to be applied on

        Return: 
        - The action that was redone, or None.
        
        Complexity: O(PaintActoion.redo_apply())
        """
        if not self.undo_list:
            return None
        redo_action = self.undo_list.pop()
        self.action_list.push(redo_action)
        redo_action.redo_apply(grid)
        return redo_action
