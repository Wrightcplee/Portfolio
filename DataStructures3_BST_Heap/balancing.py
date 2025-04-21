from __future__ import annotations
from threedeebeetree import Point
from ratio import Percentiles

def make_ordering(my_coordinate_list: list[Point]) -> list[Point]:
    """
    Make ordering main. If coordinate list length is <= 17, returns it as it is. (Base Case)

    Complexity: O(n*log(n)*log(n)). Also O(midpoint*recursion depth) where recursion depth is log(n)
    """
    if len(my_coordinate_list) <= 17:
        return my_coordinate_list
    mid = midpoint(my_coordinate_list)
    octants = split(my_coordinate_list, mid)
    res = [mid]
    for i in octants:
        res += make_ordering(i)
    return res
    
def midpoint(my_coordinate_list: list[Point]) -> Point:
    """
    Finds a midpoint that satisfy the ratio 1:7

    Complexity: O(n*log(n)) for n is len(my_coordinate_list)
    """
    x = Percentiles()
    y = Percentiles()
    z = Percentiles()
    for i in my_coordinate_list:
        x.add_point(i[0])
        y.add_point(i[1])
        z.add_point(i[2])
    xratio = x.ratio(12.5,12.5)
    xlst = [point for point in my_coordinate_list if point[0] in xratio]
    yratio = y.ratio(12.5,12.5)
    ylst = [point for point in xlst if point[1] in yratio]
    zratio = z.ratio(12.5,12.5)
    for point in ylst:
        if point[2] in zratio:
            return point
    
def split(my_coordinate_list: list[Point], mid: Point) -> list[list[Point]]:
    """
    Splits the lists into 8 octants for a particular midpoint.

    Complexity: O(n), n is len(my_coordinate_list) 
    """
    octants = [[] for _ in range(8)]
    for i in my_coordinate_list:
        if i != mid:
            index = 0
            if i[0] > mid[0]:
                index += 4
            if i[1] > mid[1]:
                index += 2
            if i[2] > mid[2]:
                index += 1
            octants[index] += [i]
    return octants