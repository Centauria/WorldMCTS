# coding=utf-8
from model import Model, EXP_MODE
from rnn.rnn import rnn_next_state
from . import mcts
import numpy as np

SEED = 1

np.random.seed(SEED)


def random_linear_sample(min_value: 'float' = 0, max_value: 'float' = 1, n: 'int' = 16):
	diff = (max_value - min_value) / n
	r = np.random.random() * diff
	return r + np.arange(min_value, max_value, diff)


def dp(*args: 'iter'):
	"""
	Get the direct product of given sets.
	:param args: given sets
	:return: the direct product
	"""

	def _dp_inner(result, *args_inner: 'iter'):
		result_self = []
		if len(args_inner) > 0:
			if len(result) != 0:
				for r in result:
					for i in args_inner[0]:
						result_self.append(r + [i])
			else:
				for i in args_inner[0]:
					result_self.append([i])

			result = _dp_inner(result_self, *args_inner[1:])
		return result

	return _dp_inner([], *args)


class ModelMCTS(Model):
	def __init__(self):
		super(Model, self).__init__(load_model=True)
		self.mct = mcts.Tree()

	def get_action(self, z):
		a = random_linear_sample(-1, 1)
		b = random_linear_sample(0, 1)
		c = random_linear_sample(0, 1)
		actions = dp(a, b, c)
		self.mct.actions = actions
		action, self.mct = mcts.mcts(z, self.env, actions, old_tree=self.mct, tree_depth=6, simulate_depth=200)

		self.state = rnn_next_state(self.rnn, z, action, self.state)

		return action


def simulate(mct: 'mcts.Tree'):
	pass


if __name__ == '__main__':
	pass
