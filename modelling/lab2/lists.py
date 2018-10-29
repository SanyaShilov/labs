def random(lcg, a, b):
    n = lcg.next()
    return a + n % (b - a + 1)


def get_file_list(filename):
    file = open(filename)
    lst = [int(line.split()[0]) for line in file.readlines()]
    file.close()
    return lst


def get_random_list(lcg, a, b, length):
    return [random(lcg, a, b) for _ in range(length)]


def get_input_list(a, b):
    return [i for i in range(a, b + 1, (b + 1 - a) // 10)]
