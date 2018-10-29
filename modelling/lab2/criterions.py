import collections
import random
from math import log


def quantile99(v):
    x = 2.33
    return v + (2 * v) ** 0.5 * x + 2 / 3 * x ** 2 - 2 / 3


def uniformity_criterion(a, b, lst):
    counts = collections.defaultdict(int)
    for x in lst:
        counts[x] += 1
    n = len(lst)
    k = b - a + 1
    V = sum(count ** 2 for count in counts.values()) * k / n - n
    quantile = quantile99(k - 1)
    return max(0, (quantile - V) / quantile)


def correlation_criterion(lst):
    s = lst[0]
    s2 = lst[0] ** 2
    last = lst[0]
    sm = 0
    n = len(lst)
    for i in range(1, n):
        temp = lst[i]
        s += temp
        s2 += temp ** 2
        sm += last * temp
        last = temp
    sm += lst[0] * lst[-1]
    try:
        C = (n * sm - s ** 2) / (n * s2 - s ** 2)
    except ZeroDivisionError:
        return 0
    return 1 - abs(C)


def entropy_criterion(lst):
    n = len(lst)
    counts = collections.defaultdict(int)
    for x in lst:
        counts[x] += 1
    entropy = 0
    for count in counts.values():
        p = count / n
        entropy -= p * log(p, 2)
    return entropy / log(n, 2)


def common_criterion(a, b, lst, uni=True, cor=True, ent=True):
    return (
        max(uniformity_criterion(a, b, lst), not uni) *
        max(correlation_criterion(lst), not cor) *
        max(entropy_criterion(lst), not ent)
    )


if __name__ == '__main__':
    lst = [i for i in range(1000)]
    random.shuffle(lst)
    coef = common_criterion(0, 999, lst)

    print('Пример более чем 90% случайной последовательности:')
    print(lst)
    print('коэффициент случайности: {}%'.format(round(coef * 100, 2)))
