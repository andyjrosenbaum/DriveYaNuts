# Pieces sorted by lexicographic order of numbers in the widdershins
# (counter-clockwise) direction.
import itertools


class Nut:
    def __init__(self, numbers, name):
        """Wrapper for Nut object.

        Args:
            numbers: list(int) Numbers e.g.  [1, 2, 3, 4, 5, 6]

        Returns:
            Nut: Class with edges inferred from list of numbers.

        >>> nut_a = Nut([1, 2, 3, 4, 5, 6], 'a')
        >>> nut_a.edges_list
        [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1)]
        >>> (1, 2) in nut_a.edges_set
        True
        >>> (1, 3) in nut_a.edges_set
        False

        """
        self.numbers = tuple(numbers)
        self.name = name
        edges = []
        for i in range(len(numbers) - 1):
            edges.append((numbers[i], numbers[i + 1]))
        edges.append((numbers[-1], numbers[0]))
        self.edges_list = edges
        self.edges_set = frozenset(edges)

    def __getitem__(self, item):
        return self.numbers[item]


def get_open_edges(nut_1, index_1, nut_2, index_2):
    """Suppose that nut_1 and nut_2 match up at index_1 and index_2. Return open edges.


    Args:
        nut_1: Nut
        index_1: int
        nut_2: Nut
        index_2: int

    Returns:
        tuple(tuple(int), tuple(int)) Left edge, Right edge.

    >>> a = Nut([1, 2, 3, 4, 5, 6], 'a')
    >>> b = Nut([1, 2, 5, 6, 3, 4], 'b')
    >>> c = Nut([1, 3, 5, 2, 4, 6], 'c')

    >>> get_open_edges(a, 0, b, 0)
    ((2, 6), (2, 4))

    >>> get_open_edges(a, 0, c, 0)
    ((3, 6), (2, 6))

    >>> get_open_edges(a, 1, c, 3)
    ((4, 1), (3, 5))

    """
    val_1 = nut_1[index_1]
    val_2 = nut_2[index_2]
    if val_1 != val_2:
        raise ValueError(
            f"Pieces do not match {nut_1}[{index_1}], {nut_2}[{index_2}]")

    left_edge = (nut_2[index_2 + 1], nut_1[index_1 - 1])
    right_edge = (nut_1[index_1 + 1], nut_2[index_2 - 1])

    return left_edge, right_edge


def try_center(center_nut, all_nuts):
    """

    Args:
        nut:
        all_nuts:

    Returns:
    """
    set_nuts = set(all_nuts)
    set_nuts.remove(center_nut)

    possible_pairs = []

    # Check for second nut validity
    for n in all_nuts:
        if n not in set_nuts:
            continue
        left_edge, right_edge = get_open_edges(
            center_nut, 0, n, 0)

        available_nuts = set_nuts - {n}
        available_edges = set().union(*(nut.edges_set for nut in available_nuts))
        left_possible = left_edge in available_edges
        right_possible = right_edge in available_edges
        overall_possible = left_possible and right_possible

        print(f'Center {center_nut.name}, Next {n.name}')
        print(f'Left edge: {left_edge}, Right edge: {right_edge}')
        print(f'Left possible: {left_possible}, Right possible: {right_possible}')
        print(f'Overall possible: {left_possible and right_possible}')
        print('')
        if overall_possible:
            possible_pairs.append((center_nut, n))

    return possible_pairs


# Sorted lexicographically
a = Nut([1, 2, 3, 4, 5, 6], 'a')
b = Nut([1, 2, 5, 6, 3, 4], 'b')
c = Nut([1, 3, 5, 2, 4, 6], 'c')
d = Nut([1, 3, 5, 4, 2, 6], 'd')
e = Nut([1, 4, 2, 3, 5, 6], 'e')
f = Nut([1, 5, 3, 2, 6, 4], 'f')
g = Nut([1, 6, 5, 4, 3, 2], 'g')

all_nuts_list = [a, b, c, d, e, f, g]

possible_starting_pairs = []

for n in all_nuts_list:
    possible_starting_pairs.extend(try_center(n, all_nuts_list))

print('')
print('Possible starting paris:')
for pair in possible_starting_pairs:
    print(f'\tPair: ({pair[0].name}, {pair[1].name})')
