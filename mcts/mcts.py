# coding=utf-8
from math import sqrt, log
import copy
import random
import gym
from colorama import Back, Fore

TREE_HEAD = '--'
UCB_C = 12.0


class Node:
	"""
	The node of the MCT
	"""

	def __init__(self, parent: 'Node' = None, depth: 'int>=0' = 0):
		self.parent = parent
		if self.parent:
			self.depth = self.parent.depth + 1
		else:
			self.depth = depth
		self.index = 0
		self.state = None
		self.env_state = None
		self.reward = 0
		self.time = 0
		self._children = Layer(0, self)

	def __str__(self):
		return TREE_HEAD * self.depth + '[%i, %.3f, %d, %.3f]' % (self.index, self.reward, self.time, self.ucb)

	def add_child(self, child: 'Node' = None):
		if not child:
			child = Node(self)
		if not self._children:
			self._children = Layer(0, self)
		self._children.add_node(child)
		return child

	def child(self, index: 'int>=0' = 0):
		"""
		Get the child of self with the right index.
		:param index: the index of the child, default=0
		:return: the child node if exists, else None
		"""
		if index < len(self.children):
			return self.children[index]
		else:
			return None

	def sibling(self):
		"""
		Get the right neighbor of self.
		:return: the neighbor node if exists, else None
		"""
		if self.parent and self.index < len(self.parent.children) - 1:
			return self.parent.children[self.index + 1]
		else:
			return None

	def bp(self, reward):
		self.reward += reward
		self.time += 1
		node = self
		while node.parent:
			node = node.parent
			node.reward += reward
			node.time += 1

	@property
	def ucb(self):
		u = self.reward / self.time
		if self.parent:
			u += UCB_C * sqrt(log(self.parent.time) / self.time)
		return u

	@property
	def children(self):
		if self._children:
			return self._children.nodes
		else:
			return None

	@children.setter
	def children(self, layer: 'Layer'):
		self._children = layer


class Layer:
	"""
	A set of Node which have the same parent
	"""

	def __init__(self, length, parent: 'Node' = None):
		self._nodes = [None] * length
		for i in range(length):
			self._nodes[i] = Node(parent)
		self.parent = parent
		if self.parent:
			self.parent.children = self
			self.depth = self.parent.depth + 1
		else:
			self.depth = 0

	def __str__(self):
		string = ''
		prepend = '-' * self.depth
		for node in self._nodes:
			string += prepend
			string += str(node)
		return string

	def __len__(self):
		return len(self._nodes)

	def add_node(self, node: 'Node' = None):
		"""
		Add a node at the last index of the Layer.
		if the node is None, it will create a new Node.
		:param node: Node, None
		:return: node
		"""
		if not node:
			node = Node(self.parent)
		node.index = len(self._nodes)
		self._nodes.append(node)
		return node

	@property
	def nodes(self):
		return self._nodes


class Tree:
	"""
	The Monte Carlo Tree model
	"""

	def __init__(self, actions: 'iter', simulate_depth: 'int>0' = 10):
		self.root = Node()
		self._actions = actions
		self.simulate_depth = simulate_depth
		self.action_history = []

	def __str__(self):
		def self_str(node, string):
			string += (str(node) + '\n')
			return [string]

		return self._iter_dfs(self.root, self_str, [''])[0]

	@property
	def actions(self):
		return self._actions

	@actions.setter
	def actions(self, actions: 'iter'):
		for action in actions:
			self._actions.append(action)

	@property
	def depth(self):
		def max_depth(node, max_d=0):
			if node.depth > max_d:
				max_d = node.depth
			return [max_d]

		return self._iter_dfs(self.root, max_depth, [0])[0]

	def _iter_dfs(self, node: 'Node', func: 'function', arg: 'iter' = []):
		"""
		DFS algorithm of the Tree.
		Execute the function in all the Nodes under the given node.
		:param node: the root node of the DFS
		:param func: the function to be executed
		The first argument of the function must be a Node
		The return of the function must be the arg that will be used in the inner recursion of the iteration
		:param arg: the arg of the function
		:return: the arg that changed after the iteration
		"""
		arg = func(node, *arg)
		if node.children:
			arg = self._iter_dfs(node.child(), func, arg)
		if node.sibling():
			arg = self._iter_dfs(node.sibling(), func, arg)
		return arg

	def _iter_bfs(self, node: 'Node', func: 'function', arg: 'iter' = []):
		"""
		BFS algorithm of the Tree.
		Execute the function in all the Nodes under the given node.
		:param node: the root node of the BFS
		:param func: the function to be executed
		The first argument of the function must be a Node
		The return of the function must be the arg that will be used in the inner recursion of the iteration
		:param arg: the arg of the function
		:return: the arg that changed after the iteration
		"""
		arg = func(node, *arg)
		if node.sibling():
			arg = self._iter_bfs(node.sibling(), func, arg)
		if node.children:
			arg = self._iter_bfs(node.child(), func, arg)
		return arg

	def select(self):
		node = self.root
		while node.children and len(node.children) == len(self.actions):
			node = max(node.children, key=lambda child: child.ucb)
		return node

	def expand(self, node: 'Node'):
		new_node = node.add_child()
		env = copy.deepcopy(node.env_state)
		new_node.state, reward, done, info = env.step(self.actions[new_node.index])
		new_node.env_state = env
		return new_node

	def simulate(self, node: 'Node'):
		sim_node = Node()
		sim_node.env_state = copy.deepcopy(node.env_state)
		accumulate_reward = 0
		for i in range(self.simulate_depth):
			sim_node.state, reward, done, info = sim_node.env_state.step(random.choice(self.actions))
			accumulate_reward += reward
			if done:
				break
		node.bp(accumulate_reward)

	def print(self, max_depth=None):
		def print_node(node, _max_depth):
			if node.depth == 0:
				print(Back.GREEN + Fore.BLACK + str(node) + Fore.RESET + Back.RESET, 'Depth:', self.depth)
			elif node.depth < _max_depth:
				print(node)
			return [max_depth]

		self._iter_dfs(self.root, print_node, [max_depth])


def mcts(state, env_state, actions, tree_depth=10, simulate_depth=30):
	"""
	MCTS algorithm
	:param state: root state
	:param env_state: root environment state
	:param actions: a set of actions
	:param tree_depth: the max depth of the MCT
	:param simulate_depth: the depth of simulation
	:return: best action
	"""
	mct = Tree(actions, simulate_depth=simulate_depth)
	mct.root.state = state
	mct.root.env_state = copy.deepcopy(env_state)
	while mct.depth <= tree_depth:
		node = mct.expand(mct.select())
		mct.simulate(node)
	mct.print(max_depth=2)
	result = max(mct.root.children, key=lambda child: child.ucb)
	return mct.actions[result.index]


def test():
	"""
	test program
	:return: None
	"""
	env = gym.make('Taxi-v2')
	obs = env.reset()
	done = False
	reward = 0
	recording_obs = []
	recording_reward = []
	while not done:
		env.render()
		print('Reward:', reward)
		obs, reward, done, info = env.step(mcts(obs, env, range(env.action_space.n), tree_depth=5, simulate_depth=25))
		recording_obs.append(obs)
		recording_reward.append(reward)
	print(recording_obs)
	print(recording_reward)


if __name__ == '__main__':
	test()
