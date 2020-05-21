import math
from typing import List, Tuple

import numpy as np

from core.geometry import Point, Line

PI = np.pi


def rotate(p, a):
    return Point(
        p.x * math.cos(a) - p.y * math.sin(a),
        p.x * math.sin(a) + p.y * math.cos(a),
    )


def normalized_direction(dir):
    dir = math.fmod(dir, 2 * PI)
    if dir > PI:
        dir -= 2 * PI
    if dir < -PI:
        dir += 2 * PI
    return dir


def points_on_opposite_sides(a: Point, b: Point, line: Line):
    x, y = line.p1, line.p2
    xy = y - x
    xa = a - x
    xb = b - x
    return xy.cross(xb) * xy.cross(xa) <= 0


def is_lines_intersect(ab: Line, cd: Line):
    a, b = ab.p1, ab.p2
    c, d = cd.p1, cd.p2
    return points_on_opposite_sides(a, b, cd) \
           and points_on_opposite_sides(c, d, ab)


def is_intersect(line1, l_f, l_b, r_f, r_b):
    rect_lines = [
        Line(l_f, r_f),
        Line(r_f, r_b),
        Line(r_b, l_b),
        Line(l_b, l_f),
    ]
    return any(
        is_lines_intersect(line1, line2) for line2 in rect_lines
    )


def calculate_length(p_list: List[Point]):
    total_len = 0
    for i in range(len(p_list) - 1):
        total_len += distance_between_points(p_list[i], p_list[i + 1])
    return total_len


def get_closest_point(p: Point, p_list: List[Point]) -> Tuple[int, float]:
    """
    Returns (k, offset) meaning the closest point in on segment
    (p_list[k], p_list[k + 1]) and its distance between p_list[k + 1] is `offset`.
    """

    # Initialize to distance between p_list[0]
    min_dist = distance_between_points(p, p_list[0])
    index, offset = 0, distance_between_points(p_list[0], p_list[1])
    for i in range(len(p_list) - 1):
        a, b = p_list[i], p_list[i + 1]
        # Check dist(P, B)
        dist = distance_between_points(p, b)
        if dist < min_dist:
            min_dist, index, offset = dist, i, 0.0
        # Check closest point in segment (if exists)
        ab = b - a
        pb = b - p
        ab_l = distance_between_points(a, b)
        t = pb.dot(ab) / ab_l
        if 0 <= t <= ab_l:
            dist = math.sqrt(pb.dot(pb) - t ** 2)
            if dist < min_dist:
                min_dist, index, offset = dist, i, t

    return index, offset


def distance_between_points(p1: Point, p2: Point):
    dist = math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
    return dist


def intersect_ray_line(p: Point, direction: float, segments: List[Point]) -> float:
    # ray(t) = P + t * n  (t >= 0)
    n = Point(math.cos(direction), math.sin(direction))

    min_t = float('inf')
    for i in range(len(segments) - 1):
        a, b = segments[i], segments[i + 1]
        # Does segment AB intersect line of the ray?
        if n.cross(a - p) * n.cross(b - p) > 0:
            continue
        # Now find t such that P + t * n on AB <=> (P + t * n - A) x AB = 0
        #   <=> AP x AB + t * n x AB = 0
        ap = p - a
        ab = b - a
        t = - ap.cross(ab) / n.cross(ab)
        if t < 0:
            # On the negative side, so does not really intersects
            continue
        min_t = min(min_t, t)

    return min_t
