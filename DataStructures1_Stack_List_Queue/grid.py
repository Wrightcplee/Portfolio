from __future__ import annotations

from data_structures.referential_array import ArrayR
from layer_store import SetLayerStore, AdditiveLayerStore, SequenceLayerStore

class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style: str, x: int, y: int) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.

        Args:
        - draw_style: str of either "SET", "ADD" or "SEQUENCE"
        - x: int for dimensions in the x-axis
        - y: int for dimensions in the y-axis

        Complexity: O(x*y) where x and y as dimensions of the grid
        """
        self.grid = ArrayR(x)
        for i in range(len(self.grid)):
            self.grid[i] = ArrayR(y)
            for j in range(len(self.grid[i])):
                if draw_style == self.DRAW_STYLE_SET:
                    self.grid[i][j] = SetLayerStore()
                elif draw_style == self.DRAW_STYLE_ADD:
                    self.grid[i][j] = AdditiveLayerStore()
                else:
                    self.grid[i][j] = SequenceLayerStore()
        self.x = x
        self.y = y
        self.brush_size = self.DEFAULT_BRUSH_SIZE

    def __getitem__(self, index: int) -> ArrayR:
        """
        Allows access to individual grid by using grid[x][y]. 

        Args:
        - index: int for the x-value of the grid

        Returns:
        - row in ArrayR of the input index

        Complexity: O(1)
        """
        return self.grid[index]

    def increase_brush_size(self) -> None:
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        Complexity: O(1)
        """
        if self.brush_size < self.MAX_BRUSH:
            self.brush_size += 1

    def decrease_brush_size(self) -> None:
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        Complexity: O(1)
        """
        if self.brush_size > self.MIN_BRUSH:
            self.brush_size -= 1

    def special(self) -> None:
        """
        Activate the special affect on all grid squares.
        Complexity: O(x*y) where x and y are dimensions of the grid
        """
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                self.grid[i][j].special()