class Component:
	def __init__(self, name, componentType):
		self.name = name
		self.componentType = componentType
		if self.componentType == "assembly":
			self.children = []
		self.parents = []

parts = {} # maps name to Component object
assemblies = {} # maps name to Component object
