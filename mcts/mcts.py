# coding=utf-8
TREE_HEAD = '--'


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
		self.reward = 0
		self.time = 0
		self.children = None

	def __str__(self):
		prepend = TREE_HEAD * self.depth
		return prepend + '[%i, %.3f, %d]\n' % (self.index, self.reward, self.time)

	def add_child(self, child: 'Node' = None):
		if not child:
			child = Node(self)
		if not self.children:
			self.children = Layer(0, self)
		self.children.add_node(child)


class Layer:
	"""
	A set of _nodes which have the same parent
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
		if not node:
			node = Node(self.parent)
		node.parent = self.parent
		node.index = len(self._nodes)
		self._nodes.append(node)
		return node

	@property
	def nodes(self):
		return self._nodes

	@property
	def length(self):
		return len(self._nodes)


class Tree:
	"""
	The Monte Carlo Tree model
	"""

	def __init__(self):
		self.root = Node()

	def __str__(self):
		node = self.root
		return self._str_iter_dfs(node)

	def _str_iter_dfs(self, node, string=''):
		result = string + str(node)
		if node.children:
			result += self._str_iter_dfs(self.child(node), string)
		if self.sibling(node):
			result += self._str_iter_dfs(self.sibling(node), string)
		return result

	def child(self, node: 'Node', index: 'int>=0' = 0):
		return node.children.nodes[index]

	def sibling(self, node: 'Node'):
		if node.parent and node.index < node.parent.children.length - 1:
			return node.parent.children.nodes[node.index + 1]
		else:
			return None

	def select(self):
		pass

	def expand(self):
		pass

	def simulate(self):
		pass

	def bp(self):
		pass


def mcts():
	"""
	MCTS algorithm
	:return: None
	"""


def test():
	"""
	test program
	:return: None
	"""
	t = Tree()
	t.root.add_child()
	t.root.add_child()
	t.root.add_child()
	t.root.children.nodes[0].add_child()
	t.root.children.nodes[0].add_child()
	t.root.children.nodes[0].add_child()
	t.root.children.nodes[0].add_child()
	print(t)


if __name__ == '__main__':
	test()
