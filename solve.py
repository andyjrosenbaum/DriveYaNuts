#!/usr/bin/env python
"""Solve the puzzle game "Drive Ya Nuts"
    https://www.amazon.com/Vintage-Milton-Bradley-Drive-Puzzle/dp/B00I84HL70/
"""
# Assumes python 3.8.0+
# SOLUTION: [d, f, a, c, g, b, e]
import argparse


def main(partial=False, verbose=False):
    """Find the solution(s) and print to stdout.

    Args:
        partial: (bool) Only find partial solution (starting pairs).
        verbose: (bool) More prints.

    """
    # Sorted lexicographically
    a = Nut([1, 2, 3, 4, 5, 6], 'a')
    b = Nut([1, 2, 5, 6, 3, 4], 'b')
    c = Nut([1, 3, 5, 2, 4, 6], 'c')
    d = Nut([1, 3, 5, 4, 2, 6], 'd')
    e = Nut([1, 4, 2, 3, 5, 6], 'e')
    f = Nut([1, 5, 3, 2, 6, 4], 'f')
    g = Nut([1, 6, 5, 4, 3, 2], 'g')

    all_nuts_list = [a, b, c, d, e, f, g]

    if partial:
        print_partial_solutions(all_nuts_list, verbose)
    else:
        print_full_solutions(all_nuts_list, verbose)


class Nut:
    def __init__(self, numbers, name):
        """Wrapper for Nut object.

        Args:
            numbers: list(int) Numbers on the Nut in widdershins (counter-clockwise) direction,
                e.g.  [1, 2, 3, 4, 5, 6]

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
            # print(f'>> Warning: converting lookup index {old_item} to {item}')
        return self.numbers[item]

    def __gt__(self, other):
        return self.name > other.name

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return self.name


def get_open_edges(nut_1, index_1, nut_2, index_2):
    """Suppose that nut_1 and nut_2 match up at index_1 and index_2: return open edges on left and right.

    Args:
        nut_1: Nut
        index_1: int
        nut_2: Nut
        index_2: int

    Returns:
        tuple(tuple(int, int), tuple(int, int)) Left edge, Right edge.

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
    """Partial solution finder, to narrow down to possible center center and second nuts.

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
            print(f'{center_nut=}, Next {n.name}')
            print(f'{left_edge=}, {right_edge=}')
            print(f'{left_possible=}, {right_possible=}')
            print(f'Overall possible: {left_possible and right_possible}')
            print('')
        if overall_possible:
            possible_pairs.append((center_nut, n, left_options, right_options))

    return possible_pairs


def trace_path(center_nut, second_nut, center_index, available_nuts, stack=[], verbose=True):
    """Full solution finder.

    Args:
        center_nut: Nut
        second_nut: Nut
        center_index: int
        available_nuts: set(Nut)
        stack: list(Nut) previous nuts used in sequence thus far.
        verbose: (bool) More prints.

    Returns:
        bool: True if solution found, else False.
        list(Nut): Solution sequence if found, else empty list.

    """
    # Reached end of path; success!
    if not available_nuts:
        if verbose:
            print('')
            print('*** Reached end with success!!!! ***')
            print(stack)
            print('')
        return True, stack

    center_value = center_nut[center_index]
    second_index = second_nut.numbers.index(center_value)

    if verbose:
        print('')
        print(f'{stack=}')
        print(f'{center_nut=}, {second_nut=}.')
        print(f'{center_index=}, {center_value=}, {second_index=}')
        print(f'{available_nuts=}')

    left_edge, right_edge = get_open_edges(
        center_nut, center_index, second_nut, second_index)

    for right_nut in available_nuts:
        if right_edge in right_nut.edges_set:
            if verbose:
                print(f'{right_edge=} found for Nut {right_nut=}.')
                print(f'Recursion!')
            # Sorting adds running time, but ensures deterministic order of exploration.
            new_available_nuts = sorted(set(available_nuts) - {right_nut})
            stack = stack + [right_nut]
            # Recursion!
            return trace_path(center_nut, right_nut, center_index + 1, new_available_nuts, stack=stack, verbose=verbose)

    if verbose:
        print(f'No available nut for {right_edge=}; No solution found for stack!')
    return False, stack


def print_partial_solutions(nuts_list, verbose=False):
    """Print only possible starting pairs.

    Args:
        nuts_list: (list(Nut)) list of Nuts in the puzzle.
        verbose: (bool) More prints.

    """
    possible_starting_pairs = []

    for cn in nuts_list:
        possible_starting_pairs.extend(try_center(cn, nuts_list, verbose=verbose))

    print('')
    print(f'Found {len(possible_starting_pairs)} possible starting pairs.')
    print('Possible starting paris:')
    for pair in possible_starting_pairs:
        print(f'\tPair: ({pair[0].name}, {pair[1].name}), Left: {pair[2]}, Right: {pair[3]}')


def print_full_solutions(nuts_list, verbose=False):
    """Print full solutions.

    Args:
        nuts_list: (list(Nut)) list of Nuts in the puzzle.
        verbose: (bool) More prints.

    """
    solutions = []
    for cn in nuts_list:
        for sn in sorted(set(nuts_list) - {cn}):
            starting_stack = [cn, sn]
            if verbose:
                print('')
                print(f'Trying {starting_stack=}')
            available = sorted(set(nuts_list) - {cn, sn})
            found, sequence = trace_path(cn, sn, 0, available, stack=starting_stack, verbose=verbose)
            if found:
                solutions.append(sequence)

    print('')
    print('Final solutions found:')
    for s in solutions:
        print(f'\t{s}')


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser()
    parser = argument_parser
    parser.add_argument(
        "-p", "--partial", action="store_true", help="Only print partial solution (possible starting pairs)")
    parser.add_argument("-v", "--verbose", action='store_true', help="Print verbose debug messages")
    args = parser.parse_args()
    main(partial=args.partial, verbose=args.verbose)
