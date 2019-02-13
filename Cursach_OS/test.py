#!/usr/bin/python3.6

import random
import time

a = 0
while True:
    for i in range(1000):
        a = (a * a + 17) % (a + 37) + random.randint(1, 100)
    print(a)
    time.sleep(0.01)

