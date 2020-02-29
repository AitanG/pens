'''
Main data format:

{
	<Model ID>:
	{
		"color": <color>,
		"children":
		[
			{
				"name": <unique component name>,
				"componentType": {assembly, part},
				"children": (if not part)
				[
					{
						"name": <unique component name>,
						"componentType": {assembly, part},
						"children": ...
					}
				]
			},

			...
		]
	}

	...
}

'''

class Component:
	def __init__(self, name, componentType):
		self.name = name
		self.componentType = componentType
		if self.componentType == "assembly":
			self.children = []
		self.parents = []

class Pen:
	def __init__(self, name, color=None):
		self.name = name
		self.color = color
		self.children = [] # TODO: should just be the top-level assembly?


models = {
	"pens": {}, # maps name to Pen object
	"parts": {}, # maps name to Component object
	"assemblies": {} # maps name to Component object
}
