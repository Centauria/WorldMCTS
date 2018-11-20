# coding=utf-8
from model import *

from vae.vae import ConvVAE
from rnn.rnn import hps_sample, MDNRNN, rnn_init_state, rnn_next_state, rnn_output, rnn_output_size
import mcts
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
	def __init__(self, load_model=True):
		self.env_name = "carracing"
		self.env = make_env(self.env_name, seed=SEED, render_mode=render_mode, full_episode=False)
		self.vae = ConvVAE(batch_size=1, gpu_mode=False, is_training=False, reuse=True)

		self.rnn = MDNRNN(hps_sample, gpu_mode=False, reuse=True)

		if load_model:
			self.vae.load_json('../vae/vae.json')
			self.rnn.load_json('../rnn/rnn.json')

		self.state = rnn_init_state(self.rnn)
		self.rnn_mode = True

		self.input_size = rnn_output_size(EXP_MODE)
		self.z_size = 32

		if EXP_MODE == MODE_Z_HIDDEN:  # one hidden layer
			self.hidden_size = 40
			self.weight_hidden = np.random.randn(self.input_size, self.hidden_size)
			self.bias_hidden = np.random.randn(self.hidden_size)
			self.weight_output = np.random.randn(self.hidden_size, 3)
			self.bias_output = np.random.randn(3)
			self.param_count = ((self.input_size + 1) * self.hidden_size) + (self.hidden_size * 3 + 3)
		else:
			self.weight = np.random.randn(self.input_size, 3)
			self.bias = np.random.randn(3)
			self.param_count = (self.input_size) * 3 + 3

		self.render_mode = False
		self.mct = None

	def get_action(self, z):
		a = random_linear_sample(-1, 1)
		b = random_linear_sample(0, 1)
		c = random_linear_sample(0, 1)
		actions = dp(a, b, c)
		action, self.mct = mcts.mcts(z, self.env, actions, old_tree=self.mct, tree_depth=6, simulate_depth=200)

		self.state = rnn_next_state(self.rnn, z, action, self.state)

		return action


if __name__ == '__main__':
	N_episode = 1
	reward_list = []
	model = ModelMCTS()
	for i in range(N_episode):
		reward, steps_taken = simulate(model, train_mode=False, render_mode=True, num_episode=1)
		print("terminal reward", reward, "average steps taken", np.mean(steps_taken) + 1)
		reward_list.append(reward[0])
