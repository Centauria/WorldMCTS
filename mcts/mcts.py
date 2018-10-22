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
		self.explored = False
		self.reward = 0
		self.time = 0
		self._children = None

	def __str__(self):
		prepend = TREE_HEAD * self.depth
		return prepend + '[%i, %.3f, %d]' % (self.index, self.reward, self.time)

	def add_child(self, child: 'Node' = None):
		if not child:
			child = Node(self)
		if not self._children:
			self._children = Layer(0, self)
		self._children.add_node(child)

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
		node.parent = self.parent
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

	def __init__(self):
		self.root = Node()

	def print(self):
		def self_print(node):
			print(node)
			return []

		self._iter_dfs(self.root, self_print)

	def _iter_dfs(self, node: 'Node', func: 'function', arg: 'iter' = []):
		"""
		DFS algorithm of the Tree.
		Execute the function in all the Nodes under the given node.
		:param node: the root node of the DFS
		:param func: the function to be executed
		The first argument of the function must be a Node
		The return of the function must be the arg that will be used in the inner recursion of the iteration
		:param arg: the arg of the function
		:return: None
		"""
		arg = func(node, *arg)
		if node.children:
			self._iter_dfs(self.child(node), func, arg)
		if self.sibling(node):
			self._iter_dfs(self.sibling(node), func, arg)

	def _iter_bfs(self, node: 'Node', func: 'function', arg: 'iter' = []):
		"""
		BFS algorithm of the Tree.
		Execute the function in all the Nodes under the given node.
		:param node: the root node of the BFS
		:param func: the function to be executed
		The first argument of the function must be a Node
		The return of the function must be the arg that will be used in the inner recursion of the iteration
		:param arg: the arg of the function
		:return: None
		"""
		arg = func(node, *arg)
		if self.sibling(node):
			self._iter_bfs(self.sibling(node), func, arg)
		if node.children:
			self._iter_bfs(self.child(node), func, arg)

	def child(self, node: 'Node', index: 'int>=0' = 0):
		return node.children[index]

	def sibling(self, node: 'Node'):
		if node.parent and node.index < len(node.parent.children) - 1:
			return node.parent.children[node.index + 1]
		else:
			return None

	def reset(self):
		"""
		Set the variable 'explored' of all Node in the Tree to False.
		:return: None
		"""

		def set_to_false(node):
			node.explored = False

		self._iter_dfs(self.root, set_to_false, (self.root,))

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
	t.root.children[1].add_child()
	t.root.children[1].add_child()
	t.root.children[1].add_child()
	t.root.children[1].children[0].add_child()
	t.root.children[1].children[0].add_child()
	t.root.children[1].children[0].add_child()
	t.root.children[1].children[0].add_child()
	t.root.add_child()
	t.root.children[2].add_child()
	t.print()
	pass


if __name__ == '__main__':
	test()
