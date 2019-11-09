
# SOLUTION: [d, f, a, c, g, b, e]
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
        if item >= len(self.numbers):
            old_item = item
            item = old_item % len(self.numbers)
            print(f'>> Warning: converting looking index {old_item} to {item}')
        return self.numbers[item]

    def __gt__(self, other):
        return self.name > other.name

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return self.name


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


def try_center(center_nut, all_nuts, verbose=True):
    """

    Args:
        center_nut: Nut
        all_nuts: list(Nut)
        verbose: Print each option tried.

    Returns:
        list(Nut, Nut, list(Nut), list(Nut): List of valid combinations of
            Center piece, Second piece, possible Left edges, possible Right edges.

    >>> a = Nut([1, 2, 3, 4, 5, 6], 'a')
    >>> b = Nut([1, 2, 5, 6, 3, 4], 'b')
    >>> c = Nut([1, 3, 5, 2, 4, 6], 'c')
    >>> d = Nut([1, 3, 5, 4, 2, 6], 'd')
    >>> e = Nut([1, 4, 2, 3, 5, 6], 'e')
    >>> f = Nut([1, 5, 3, 2, 6, 4], 'f')
    >>> g = Nut([1, 6, 5, 4, 3, 2], 'g')
    >>> all_nuts_list = [a, b, c, d, e, f, g]
    >>> try_center(a, all_nuts_list, verbose=False)
    [(a, b, [d, f], [c]), (a, e, [c], [d, f]), (a, f, [b, e], [c])]


    """
    possible_pairs = []

    # Check for second nut validity
    for n in all_nuts:
        if n == center_nut:
            continue

        # Match up on the '1's
        left_edge, right_edge = get_open_edges(
            center_nut, 0, n, 0)

        available_nuts = sorted(set(all_nuts) - {center_nut, n})

        # available_edges = set().union(*(nut.edges_set for nut in available_nuts))
        left_options = []
        right_options = []
        for m in available_nuts:
            if left_edge in m.edges_set:
                left_options.append(m)
            if right_edge in m.edges_set:
                right_options.append(m)

        left_possible = bool(left_options)
        right_possible = bool(right_options)
        overall_possible = left_possible and right_possible

        if verbose:
            print(f'Center {center_nut.name}, Next {n.name}')
            print(f'Left edge: {left_edge}, Right edge: {right_edge}')
            print(f'Left possible: {left_possible}, Right possible: {right_possible}')
            print(f'Overall possible: {left_possible and right_possible}')
            print('')
        if overall_possible:
            possible_pairs.append((center_nut, n, left_options, right_options))

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

VERBOSE = False
# VERBOSE = True

for cn in all_nuts_list:
    possible_starting_pairs.extend(try_center(cn, all_nuts_list, verbose=VERBOSE))

print('')
print(f'Found {len(possible_starting_pairs)} possible starting pairs.')
print('Possible starting paris:')
for pair in possible_starting_pairs:
    print(f'\tPair: ({pair[0].name}, {pair[1].name}), Left: {pair[2]}, Right: {pair[3]}')


# Flesh out starting pairs.
def trace_path(center_nut, second_nut, center_index, available_nuts):
    """

    Args:
        center_nut: Nut
        second_nut: Nut
        center_index: int
        available_nuts: set(Nut)

    Returns:
        bool: path match

    """
    print('')
    print(f'Center nut {center_nut}, Second nut {second_nut}.')
    center_value = center_nut[center_index]
    second_index = second_nut.numbers.index(center_value)
    print(f'Center index {center_index}, Center value {center_value}, Second index: {second_index}')
    print(f'Available nuts: {available_nuts}')

    left_edge, right_edge = get_open_edges(
        center_nut, center_index, second_nut, second_index)

    # Reached end of path
    if not available_nuts:
        print('')
        print('*** Reached end with success!!!! ***')
        print('')
        return True

    for right_nut in available_nuts:
        if right_edge in right_nut.edges_set:
            print(f'Right edge {right_edge} found for Nut {right_nut}.')
            print(f'Recursion!')
            new_available_nuts = sorted(set(available_nuts) - {right_nut})
            return trace_path(center_nut, right_nut, center_index + 1, new_available_nuts)

    print('No more matches!')
    return False


for cn in all_nuts_list:
    print('')
    print(f'# Trying Center nut {cn}')
    for sn in sorted(set(all_nuts_list) - {cn}):
        print('')
        print(f'## Trying second nut {sn}')
        available = sorted(set(all_nuts_list) - {cn, sn})
        trace_path(cn, sn, 0, available)
