import os
import re
import itertools
import functools
import glob
from typing import List
import argparse
import time
import pathlib
from functools import wraps

import matplotlib.pyplot as plt

import csp

OPTIONS = {
    'mrv': csp.mrv,
    'mac': csp.mac,
    'fc': csp.forward_checking,
    'no_inference': csp.no_inference,
    'first_unassigned_variable': csp.first_unassigned_variable
}

FILE_PATH = pathlib.Path(__file__)
TESTS_PATH = os.path.join(os.path.basename(FILE_PATH.parents[0]), "inputs")


# Some utility functions for plotting & displaying results
def testing(func):

    @wraps(func)
    def inner(*args, **kwargs):
        s = args[0]  # The csp object
        print(f'Executing Backtracking search...\nInference={kwargs["inference"].__name__}')
        print(f'Select Unassigned Variable: {kwargs["select_unassigned_variable"].__name__}')

        tic = time.perf_counter()
        res = func(*args, **kwargs)
        tac = time.perf_counter()

        exec_time = tac - tic
        conflicts = s.conflicts
        nassigns = s.nassigns
        puzzle_size = s.size

        print(f"Execution time: {exec_time:.4f} seconds\nTotal conflicts: {conflicts}")
        print(f"Total assignments: {nassigns}")
        print("Output result:")
        s.display(res)

        return res, puzzle_size, exec_time, conflicts, nassigns

    return inner


def plot_results(fc_results, mac_results, compare_on, save=False):
    fc = sorted(list(fc_results.items()))
    mac = sorted(list(mac_results.items()))
    sizes = list(map(lambda x: x[0], fc))
    fc_vals = list(map(lambda x: x[1], fc))
    mac_vals = list(map(lambda x: x[1], mac))

    fig, ax = plt.subplots(figsize=(5, 5))
    plt.plot(sizes, fc_vals, label="MRV + FC")
    plt.plot(sizes, mac_vals, label="MRV + MAC")
    ax.set_title('Comparison of MRV+FC with MRV + MAC')
    ax.set_xlabel('Puzzle size')
    ax.set_ylabel(compare_on)
    plt.legend()
    if save:
        plt.savefig(compare_on + ".png")
    plt.show()


# Main part
class Clique():

    def __init__(self, val: int, op: str, points: List[str]):
        self.op = op
        self.points = points
        self.val = val

    def __repr__(self):
        return f"Clique({self.points})"


def get_clique_domain(clique: Clique, kenken_size: int):
    M = len(clique.points)
    return [*itertools.product(range(1, kenken_size + 1), repeat=M)]


def clique_constraint(clique: Clique, val):
    if clique.op == '+':
        return sum(val) == clique.val

    elif clique.op == '*':
        return functools.reduce(lambda x, y: x * y, val) == clique.val

    elif clique.op == '=':
        return val[0] == clique.val

    elif clique.op == '-':
        return abs(val[0] - val[1]) == clique.val

    elif clique.op == '/':
        return max(val[0], val[1]) / min(val[0], val[1]) == clique.val


def get_point_neighs(point: str, kenken_size: int, cliques: List[Clique]):
    neighs = set()

    r, c = divmod(int(point), kenken_size)
    # find point neighbors
    neighs = {str(j*kenken_size+c) for j in range(kenken_size) if j*kenken_size+c != int(point)}\
        .union({str(r*kenken_size + j) for j in range(kenken_size) if r*kenken_size+j != int(point)})

    # find clique neighbors
    for c in cliques:
        if point in c.points:
            neighs.add(c)

    return neighs


class Kenken(csp.CSP):
    """An object for modelling the Kenken problem
    
    Input expects to be in the form:
    4
    3#0#=
    24#1-2-6#*
    2#3-7#/
    1#11-15#-
    2#12-13#-
    7#9-10-14#+
    7#4-5-8#+
    """

    def __init__(self, input_file: str):

        self.variables = []
        self.cliques = []
        self.domains = dict()
        self.neighbors = dict()

        self.read_file(input_file)

        self.get_domains_and_neighbors()
        self.conflicts = 0

        super().__init__(None, self.domains, self.neighbors, self.kenken_constrains)

    def read_file(self, input_file: str):
        with open(input_file) as f:
            for i, line in enumerate(f.readlines()):
                if i == 0:  # The first line corresponds to the size of the grid
                    self.size = int(line.rstrip())
                else:
                    line = line.rstrip().split("#")
                    variables = re.compile(r"(\d+)").findall(line[1])
                    clique = Clique(int(line[0]), line[2], list(variables))
                    self.cliques.append(clique)
                    self.variables += [*variables, clique]

    def get_domains_and_neighbors(self):
        for var in self.variables:
            if isinstance(var, str):
                self.domains[var] = list(range(1, self.size + 1))
                self.neighbors[var] = get_point_neighs(var, self.size, self.cliques)
            else:
                self.domains[var] = get_clique_domain(var, self.size)
                self.neighbors[var] = var.points

    def kenken_constrains(self, A, a, B, b):
        # Both points
        if isinstance(A, str) and isinstance(B, str):
            return a != b
        # A is point, B a clique
        elif isinstance(A, str) and not isinstance(B, str):
            pt_index = B.points.index(A)
            if clique_constraint(B, b) and b[pt_index] == a:
                return True
            else:
                self.conflicts += 1
                return False
        # A is a clique, B is point
        elif isinstance(B, str) and not isinstance(A, str):
            pt_index = A.points.index(B)
            if clique_constraint(A, a) and a[pt_index] == b:
                return True
            else:
                self.conflicts += 1
                return False
        else:
            print("error!")

    def display(self, assignment):
        for i in range(self.size * self.size):
            c = i % self.size
            print(assignment[str(i)], end=" ")
            if c == self.size - 1:
                print()
        pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='Kenken',
        description='Solving Kenken puzzles using CSP Algorithms.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        usage='Use flag -i to enter your puzzle.'
    )

    parser.add_argument(
        '-i', '--input_puzzle', dest='input', help='The txt file containing the puzzle with the specified format.'
    )

    parser.add_argument(
        '-a',
        '--algorithm',
        dest='algorithm',
        choices=['backtracking', 'min_conflicts'],
        default='backtracking',
        help='Whether to use backtracking or min_conflicts.'
    )

    parser.add_argument(
        '-m',
        '--max_steps',
        dest='max_steps',
        default=100_000,
        type=int,
        help='The number of max steps for min conflicts'
    )

    parser.add_argument(
        '--inference',
        choices=['fc', 'mac', 'no_inference'],
        default='no_inference',
        help='fc: Forward Checking | mac: Maintaining Arc Consistency'
    )

    parser.add_argument(
        '--unassigned_variable',
        choices=['mrv', 'first_unassigned_variable'],
        default='first_unassigned_variable',
        help='Whether to use MRV or not.'
    )

    parser.add_argument(
        '-s', '--save_fig', action='store_true', default=False, help='Whether to save the plots or not.'
    )

    args = parser.parse_args()

    if args.input and args.algorithm == 'backtracking':
        file = args.input
        inference = OPTIONS[args.inference]
        select_unassinged_var = OPTIONS[args.unassigned_variable]

        kenken = Kenken(file)
        print(f"Your input file: {file}\nYour puzzle's size: {kenken.size}")
        print(
            f"Using backtracking with selected unassigned variable={select_unassinged_var.__name__} and inference={inference.__name__}"
        )
        tic = time.perf_counter()
        res = csp.backtracking_search(kenken, select_unassigned_variable=select_unassinged_var, inference=inference)
        tac = time.perf_counter()
        print(f"Puzzle solved in {(tac - tic):.3f} seconds.\nTotal conflicts: {kenken.conflicts}")
        print(f"Total assignments: {kenken.nassigns}")
        print(f"Output Solution:")
        kenken.display(res)

    elif args.input and args.algorithm == 'min_conflicts':

        file = args.input
        kenken = Kenken(file)
        print(f"Your input file: {file}\nYour puzzle's size: {kenken.size}")
        print("Solving with min conflicts...")
        tic = time.perf_counter()
        res = csp.min_conflicts(kenken, args.max_steps)
        tac = time.perf_counter()
        if res:
            print(f"Puzzle solved in {(tac - tic):.3f} seconds.\nTotal conflicts: {kenken.conflicts}")
            print(f"Total assignments: {kenken.nassigns}")
            print(f"Output Solution:")
            kenken.display(res)
        else:
            print(f"Max number of steps: {args.max_steps} exceeded without reaching to a solution.")
            print(f"Total assignmens: {kenken.nassigns}")

    else:
        files = sorted(list(glob.glob(os.path.join(TESTS_PATH, "*.txt"))))
        fc_confs = {}
        fc_times = {}
        fc_assigns = {}
        mac_confs = {}
        mac_times = {}
        mac_assigns = {}

        for file in files:
            # MRV + FC
            print(f"\nMRV + FC on {file}")
            s = Kenken(file)

            res, size, exec_time, conflicts, nassigns = testing(
                csp.backtracking_search
            )(s, inference=csp.forward_checking, select_unassigned_variable=csp.mrv)

            fc_confs[size] = conflicts
            fc_times[size] = exec_time
            fc_assigns[size] = nassigns

            # MRV + MAC
            print(f"\nMRV + MAC on {file}")
            s = Kenken(file)
            res, size, exec_time, conflicts, nassigns = testing(
                csp.backtracking_search
            )(s, inference=csp.mac, select_unassigned_variable=csp.mrv)

            mac_times[size] = exec_time
            mac_confs[size] = conflicts
            mac_assigns[size] = nassigns

        save = args.save_fig

        plot_results(fc_confs, mac_confs, 'Number of Conflicts', save)
        plot_results(fc_assigns, mac_assigns, 'Number of assignments', save)
        plot_results(fc_times, mac_times, 'Execution Time [s]', save)