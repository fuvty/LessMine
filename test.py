
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import time
from lib.SampleEdge import SampleEdge
from lib.ConditionalSampleEdge import ConditionalSampleEdge
from lib.ConditionalClose import ConditionalClose
import numpy as np
from lib.Dictionary import Dictionary
import random

test_dict = dict()
test_dict[1] = [3]
test_dict[1].append(3)
test_dict[5] = [5]
print(test_dict[1])

for i in range(3):
    print(i)
    if i == 1:
        i=i-1

