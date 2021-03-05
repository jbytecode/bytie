from typing import List

import numpy
import random
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv


load_dotenv()

HOST = os.getenv("BYTIE_HOST") or 'http://localhost/'
PATH = os.getenv("BYTIE_PATH") or './.tmp'

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
