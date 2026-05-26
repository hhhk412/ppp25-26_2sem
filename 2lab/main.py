import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
import itertools
import functools
import math

def draw_polygons(polygons_list, title="Figure"):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_aspect('equal')
    ax.grid(True)
    for poly in polygons_list:
        patch = MplPolygon(list(poly), closed=True, fill=False, edgecolor='blue')
        ax.add_patch(patch)
    ax.autoscale_view()
    plt.title(title)
    plt.show()

def gen_rectangle():
    i = 1
    while True:
        yield ((i, 0), (i+1, 0), (i+1, 0.5), (i, 0.5))
        i += 1.2

def gen_triangle():
    i = 1
    while True:
        yield ((i, 0), (i+0.5, 0.866), (i+1, 0))
        i += 1.2

def gen_hexagon():
    i = 1
    while True:
        yield ((i, 0.433), (i+0.25, 0), (i+0.75, 0), (i+1, 0.433), (i+0.75, 0.866), (i+0.25, 0.866))
        i += 1.2

def tr_translate(poly, dx, dy):
    return tuple((x + dx, y + dy) for x, y in poly)

def tr_rotate(poly, angle_deg):
    rad = math.radians(angle_deg)
    return tuple((x * math.cos(rad) - y * math.sin(rad), x * math.sin(rad) + y * math.cos(rad)) for x, y in poly)

def tr_symmetry(poly, axis='x'):
    if axis == 'x': return tuple((x, -y) for x, y in poly)
    return tuple((-x, y) for x, y in poly)

def tr_homothety(poly, scale):
    return tuple((x * scale, y * scale) for x, y in poly)

def flt_convex_polygon(poly): return True
def flt_angle_point(poly, point=(0, 0)): return point in poly
def flt_square(poly, max_area=10):
    x, y = [p[0] for p in poly], [p[1] for p in poly]
    area = 0.5 * abs(sum(x[i]*y[i-1] - x[i-1]*y[i] for i in range(len(poly))))
    return area < max_area
def flt_short_side(poly, min_len=0.5):
    sides = [math.dist(poly[i], poly[(i+1)%len(poly)]) for i in range(len(poly))]
    return min(sides) < min_len
def flt_point_inside(poly, point=(0, 0)):
    x, y = point
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y) and y <= max(p1y, p2y) and x <= max(p1x, p2x):
            if p1y != p2y: xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
            if p1x == p2x or x <= xinters: inside = not inside
        p1x, p1y = p2x, p2y
    return inside
def flt_polygon_angles_inside(poly, ref_poly): return any(flt_point_inside(poly, p) for p in ref_poly)

def dec_filter(filter_func, **kwargs):
    def decorator(func):
        def wrapper(*args, **inner_kwargs):
            return filter(lambda p: filter_func(p, **kwargs), func(*args, **inner_kwargs))
        return wrapper
    return decorator

def dec_transform(trans_func, **kwargs):
    def decorator(func):
        def wrapper(*args, **inner_kwargs):
            return map(lambda p: trans_func(p, **kwargs), func(*args, **inner_kwargs))
        return wrapper
    return decorator

def agr_perimeter(poly_seq):
    return functools.reduce(lambda acc, p: acc + sum(math.dist(p[i], p[(i+1)%len(p)]) for i in range(len(p))), poly_seq, 0)
def agr_area(poly_seq):
    return functools.reduce(lambda acc, p: acc + 0.5 * abs(sum(p[i][0]*p[i-1][1] - p[i-1][0]*p[i][1] for i in range(len(p)))), poly_seq, 0)
def agr_max_side(poly_seq):
    return functools.reduce(lambda acc, p: max(acc, max(math.dist(p[i], p[(i+1)%len(p)]) for i in range(len(p)))), poly_seq, 0)

def zip_polygons(*iterators): return zip(*iterators)
def count_2D(seq): return sum(1 for _ in seq)
def zip_tuple(*iterables): return tuple(zip(*iterables))

draw_polygons(list(itertools.islice(gen_rectangle(), 7)), "Fig 2a")
draw_polygons(list(itertools.islice(gen_triangle(), 7)), "Fig 2b")
draw_polygons(list(itertools.islice(gen_hexagon(), 5)), "Fig 2c")

tapes = [list(map(lambda p: tr_translate(p, 0, i*0.8), itertools.islice(gen_rectangle(), 6))) for i in range(3)]
draw_polygons(itertools.chain(*tapes), "Fig 3a")

tape1 = list(map(lambda p: tr_rotate(p, 20), itertools.islice(gen_rectangle(), 7)))
tape2 = list(map(lambda p: tr_rotate(tr_translate(p, -2, 1), -20), itertools.islice(gen_rectangle(), 7)))
draw_polygons(tape1 + tape2, "Fig 3b")

tri_row = list(itertools.islice(gen_triangle(), 6))
sym_row = list(map(lambda p: tr_symmetry(tr_translate(p, 0, -2), 'x'), tri_row))
draw_polygons(tri_row + sym_row, "Fig 3c")

fan1 = [tr_homothety(p, 0.3 * (i + 1)) for i, p in enumerate(itertools.islice(gen_rectangle(), 5))]
fan2 = [tr_symmetry(p, 'y') for p in fan1]
draw_polygons(fan1 + fan2, "Fig 3d")