# coding=utf-8
from env import make_env
import numpy as np

SEED = 1

np.random.seed(SEED)


def random_linear_sample(min_value: 'float' = 0, max_value: 'float' = 1, n: 'int' = 16):
	diff = (max_value - min_value) / n
	r = np.random.random() * diff
	return r + np.arange(min_value, max_value, diff)


if __name__ == '__main__':
	print(random_linear_sample(4, 5, 10))
