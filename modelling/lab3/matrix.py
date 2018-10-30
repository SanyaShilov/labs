from pprint import pprint
import numpy


def calc_limit_probabilities(matrix):
    n = len(matrix)
    return numpy.linalg.solve(
        [
            [
                -sum(matrix[i]) + matrix[i][i] if i == j else matrix[j][i]
                for j in range(n)
            ]
            if i != n - 1 else [1 for j in range(n)]
            for i in range(n)
        ],
        [0 if i != n - 1 else 1 for i in range(n)]
    ).tolist()


def calc_stabilization_times(matrix, limit_probabilities):
    n = len(matrix)
    return [
        limit_probabilities[i] /
        sum((matrix[j][i] if i != j else 0 for j in range(n)))
        for i in range(n)
    ]


if __name__ == '__main__':
    matrix = [
        [0, 0.455, 0.068, 0.300],
        [0.882, 0, 0.358, 0.936],
        [0.758, 0.779, 0, 0.924],
        [0.973, 0.159, 0.691, 0],
    ]
    probabilities = calc_limit_probabilities(matrix)
    stabilization_times = calc_stabilization_times(matrix, probabilities)
    pprint(probabilities)
    pprint(stabilization_times)
