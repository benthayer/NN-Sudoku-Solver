from backtracker import Backtracker
import json
from datetime import datetime, timedelta

dims = (5, 5)


def get_limit(dims):
    limits = {
        (5, 5): timedelta(0, 30)
    }
    return limits.get(dims, None)


with open('data\{}x{}.txt'.format(dims[0], dims[1]), 'a+') as f:
    num_generated = 0
    num_cancelled = 0
    num_total = 0
    while True:
        start_time = datetime.now()
        size = dims[0] * dims[1]
        puzzle = [set(range(size)) for _ in range(size ** 2)]
        solver = Backtracker(dims)
        # False if it takes over a minute to generate

        num_total += 1
        try:
            solution = solver.generate(max_time=get_limit(dims), display_time=False)

            solution = [x.pop() for x in solution]
            sol_str = json.dumps(solution)

            f.write(sol_str + '\n')
            f.flush()

            num_generated += 1
            print("Puzzle {} generated ({})".format(num_total, num_generated))
        except TimeoutError:
            num_cancelled += 1
            print("Puzzle {} CANCELLED ({})".format(num_total, num_cancelled))
