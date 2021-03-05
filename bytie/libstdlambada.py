from typing import List

import numpy
import random
import matplotlib.pyplot as plt

sum = numpy.sum
mean = numpy.mean
median = numpy.median


def plot(nums: List) -> str:
    randstr = str(random.randrange(10000000))
    filename = f"plot_{randstr}.png"
    filepath = f"{PATH}/{filename}"
    url = f"{HOST}/{filename}"
    plt.plot(nums)
    plt.title(f"Grifik çizdircik bişki prigrim yik mi ki birdisin? (:")
    plt.savefig(filepath)
    plt.close()
    return url
