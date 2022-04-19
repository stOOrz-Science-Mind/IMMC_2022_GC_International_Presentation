from time import sleep

import numpy
import numpy as np
from numpy import linalg as la
import cv2

row = 14

seat_capacity = 3

total_pass = row * seat_capacity * 2

stay_rate = 0.1

"""
Markov chain matrix
first row: out side the plain
next number of rows: walkway cells
next number of rows * 2: seats 
"""

if __name__ == '__main__':
    x = numpy.zeros((row*3))
    A = numpy.zeros((row*3, row*3))

    is_closed_comparer = numpy.zeros((row*3))
    is_closed_comparer[0:row] = 0
    is_closed_comparer[row:] = seat_capacity

    remaining_pass = total_pass

    def check_closed():
        is_closed = is_closed_comparer <= x
        for i in range(row-1, -1, -1):
            if i == row-1:
                is_closed[i] = is_closed[i + row] & is_closed[i + row * 2]
            else:
                is_closed[i] = is_closed[i + row] & is_closed[i + row * 2] & is_closed[i + 1]

        remain_number = 0
        for i in range(row):
            if not is_closed[i+row]:
                remain_number += 1
            if not is_closed[i+row*2]:
                remain_number += 1

        return is_closed, x[:row].sum() == 0 and remaining_pass == 0, remain_number

    print(is_closed_comparer)
    print(check_closed())

    is_done = False

    t = 0

    while not is_done:
        # sleep(0.01)
        if remaining_pass > 0 and x[0] < 1:
            enter = min(1, remaining_pass)
            x[0] += enter
            remaining_pass -= enter
        is_closed, is_done, remain_number = check_closed()
        # print("is_done: {}, remain_number {} ".format(is_done, remain_number))
        for i in range(row):
            if is_closed[i]:
                A[i + 1][i] = 0
                A[i + row][i] = 0
                A[i + row * 2][i] = 0
                A[i][i] = 1
            else:
                r_is_closed = is_closed[row + i * 2:]
                sit_prob = 1 / (r_is_closed.size - r_is_closed.sum())

                walk_prob = (1 - sit_prob * 2) * (1-stay_rate)

                A[i+1][i] = walk_prob
                A[i][i] = (1 - sit_prob * 2) * stay_rate

                if is_closed[i+row]:
                    A[i+row][i] = 0
                else:
                    A[i + row][i] = sit_prob

                if is_closed[i+row*2]:
                    A[i + row * 2][i] = sit_prob = 0
                else:
                    A[i + row * 2][i] = sit_prob

            A[i+row][i+row] = 1
            A[i+row*2][i+row*2] = 1

        x = A @ x

        for i in range(x.size):
            if x[i] > seat_capacity:
                x[i % row] += x[i] - seat_capacity
                x[i] = seat_capacity

        # print(A)
        # print(x)

        t += 1

    print("Ready to take off at t =", t, sep=" ")