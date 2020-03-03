from django.shortcuts import render
from django.http import *
from . import models
import json


'''
Helper method that validates a request and gets the request params.
'''
def getRequestParams(request, requiredAttribute=None, requiredAttributes=[]):
	queryDict = request.POST

	if not queryDict:
		raise ValueError("No request params.")
	
	if requiredAttributes:
		for a in requiredAttributes:
			if not queryDict.__contains__(a):
				raise ValueError(f"Attribute {a} missing from request body.")
	else:
		if not queryDict.__contains__(requiredAttribute):
			raise ValueError(f"Attribute {requiredAttribute} missing from request body.")

	return queryDict


'''
Helper method that checks if the provided parent has any children,
and if so, converts it back into a part.
'''
def checkConvertBackToPart(parent):
	if not parent.children:
		parent.componentType = "part"
		del models.assemblies[parent.name]
		models.parts[parent.name] = parent


'''
Helper method that deletes the part passed into the request body.

Original text:
delete a part (thereby also deleting the part from its parent assemblies)
'''
def deletePart(request, name):
	if name not in models.parts:
		return HttpResponseBadRequest("The requested part does not exist.")

	part = models.parts[name]

	# Delete the part from its parent assemblies
	for parent in part.parents:
		parent.children.remove(part)
		checkConvertBackToPart(parent)

	# Delete the part from the list of parts
	del models.parts[part.name]

	return HttpResponse()


'''
Helper method that creates the part passed into the request body.

Original text:
create a new part
'''
def createPart(request, name):
	if name in models.parts:
		return HttpResponseBadRequest("The requested part already exists.")

	part = models.Component(name, componentType="part")
	models.parts[name] = part

	return HttpResponse()


'''
Helper method that recursively finds all components used to create a parent assembly.
'''
def getChildrenOfAssembly(parentAssembly, aggregatedChildren):
	aggregatedChildren.update(parentAssembly.children)

	childrenAssemblies = [child for child in parentAssembly.children if child.componentType == "assembly"]
	for child in childrenAssemblies:
		getChildrenOfAssembly(child, aggregatedChildren)


'''
Helper method that recursively finds all assemblies containing a component.
'''
def getAssembliesContaining(component, assembliesContaining):
	assembliesContaining.update(component.parents)

	for parent in component.parents:
		getAssembliesContaining(parent, assembliesContaining)


'''
POST/DELETE Method

URL Path: 'part/<str:name>'

create a new part
delete a part (thereby also deleting the part from its parent assemblies)
'''
def part(request, name):
	if request.method == "POST":
		# This is a post request--create new part
		return createPart(request, name)
	elif request.method == "DELETE":
		# This is a delete request--delete the part
		return deletePart(request, name)
	else:
		return HttpResponseBadRequest()


'''
GET Method

URL Path: 'part/'

list all parts
'''
def listParts(request):
	if request.method != "GET":
		return HttpResponseBadRequest()

	# List parts
	body = json.dumps(list(models.parts.keys()))
	response = HttpResponse(body, content_type="application/json")
	return response


'''
POST Method

URL Path: 'part/<str:parentName>/child/part/<str:childrenNames>'

add one or more parts as "children" to a "parent" part, which then becomes an assembly
'''
def addPartsToPart(request, parentName, childrenNames):
	if request.method != "POST":
		return HttpResponseBadRequest()

	# Validation on parent name
	if parentName not in models.parts:
		if parentName in models.assemblies:
			return HttpResponseBadRequest("The specified parent part is already an assembly.")
		else:
			return HttpResponseBadRequest("The parent part does not exist.")

	# Validation on child names
	childNames = childrenNames.split(",")
	for childName in childNames:
		if childName not in models.parts:
			if childName in models.assemblies:
				return HttpResponseBadRequest(f"The specified child part {childName} is an assembly.")
			else:
				return HttpResponseBadRequest(f"The child part {childName} does not exist.")
		if childName == parentName:
			return HttpResponseBadRequest(f"An assembly cannot use itself as a part.")

	# Convert parent part to an assembly
	parentPart = models.parts[parentName]
	parentPart.componentType = "assembly"
	parentPart.children = []
	del models.parts[parentName]
	models.assemblies[parentName] = parentPart

	# Link each pair of parts together hierarchically
	for childName in childNames:
		childPart = models.parts[childName]
		parentPart.children.append(childPart)
		childPart.parents.append(parentPart)

	return HttpResponse()


'''
GET Method

URL Path: 'part/component/'

list all component parts (parts that are not subassemblies, but are included in a parent assembly)
'''
def listComponentParts(request):
	if request.method != "GET":
		return HttpResponseBadRequest()

	# List component parts
	componentParts = [key for key, value in models.parts.items() if value.parents]
	body = json.dumps(componentParts)
	response = HttpResponse(body, content_type="application/json")
	return response


'''
GET Method

URL Path: 'part/orphan/'

list all orphan parts (parts with neither parents nor children)
'''
def listOrphanParts(request):
	if request.method != "GET":
		return HttpResponseBadRequest()

	# List orphan parts
	orphanParts = [key for key, value in models.parts.items() if not value.parents]
	body = json.dumps(orphanParts)
	response = HttpResponse(body, content_type="application/json")
	return response


'''
GET Method

URL Path: 'part/<str:name>/assembly/'

list all assemblies that contain a specific child part, either directly or indirectly (via a subassembly)
'''
def listAssembliesContainingPart(request, name):
	if request.method != "GET":
		return HttpResponseBadRequest()

	# Validation on part name
	if name not in models.parts:
		return HttpResponseBadRequest("The part does not exist.")

	part = models.parts[name]

	# Populate set of assemblies using recursive function call and return
	assembliesContaining = set([])
	getAssembliesContaining(part, assembliesContaining)
	body = json.dumps([assembly.name for assembly in assembliesContaining])
	response = HttpResponse(body, content_type="application/json")
	return response



'''
GET Method

URL Path: 'assembly/'

list all assemblies
'''
def listAssemblies(request):
	if request.method != "GET":
		return HttpResponseBadRequest()

	# List assemblies
	body = json.dumps(list(models.assemblies.keys()))
	response = HttpResponse(body, content_type="application/json")
	return response


'''
GET Method

URL Path: 'assembly/pen/'

list all top level assemblies (assemblies that are not children of another assembly)
'''
def listPens(request):
	if request.method != "GET":
		return HttpResponseBadRequest()

	# List top level assemblies
	assemblyNames = [value.name for key, value in models.assemblies.items() if not value.parents]
	body = json.dumps(assemblyNames)
	response = HttpResponse(body, content_type="application/json")
	return response


'''
GET Method

URL Path: 'assembly/subassembly/'

list all subassemblies (assemblies that are children of another assembly)
'''
def listSubassemblies(request):
	if request.method != "GET":
		return HttpResponseBadRequest()

	# List subassemblies
	assemblyNames = [value.name for key, value in models.assemblies.items() if value.parents]
	body = json.dumps(assemblyNames)
	response = HttpResponse(body, content_type="application/json")
	return response


'''
GET Method

URL Path: 'assembly/<str:parentName>/child/'

list all children of a specific assembly
'''
def listChildrenOfAssembly(request, parentName):
	if request.method != "GET":
		return HttpResponseBadRequest()

	# Validation on parent name
	if parentName not in models.assemblies:
		return HttpResponseBadRequest("The parent assembly does not exist.")

	parentAssembly = models.assemblies[parentName]

	# Populate set of children using recursive function call and return
	children = set([])
	getChildrenOfAssembly(parentAssembly, children)
	body = json.dumps([child.name for child in children])
	response = HttpResponse(body, content_type="application/json")
	return response


'''
GET Method

URL Path: 'assembly/<str:parentName>/child/first/'

list all the first-level children of a specific assembly
'''
def listTopChildrenOfAssembly(request, parentName):
	if request.method != "GET":
		return HttpResponseBadRequest()

	# Validation on parent name
	if parentName not in models.assemblies:
		return HttpResponseBadRequest("The parent assembly does not exist.")

	# List children
	parentAssembly = models.assemblies[parentName]
	childNames = [child.name for child in parentAssembly.children]
	body = json.dumps(childNames)
	response = HttpResponse(body, content_type="application/json")
	return response


'''
GET Method

URL Path: 'assembly/<str:parentName>/child/part/'

list all parts in a specific assembly (which are not subassemblies)
'''
def listPartsInAssembly(request, parentName):
	if request.method != "GET":
		return HttpResponseBadRequest()

	# Validation on parent name
	if parentName not in models.assemblies:
		return HttpResponseBadRequest("The parent assembly does not exist.")

	# List parts
	parentAssembly = models.assemblies[parentName]
	childNames = [child.name for child in parentAssembly.children if child.componentType == "part"]
	body = json.dumps(childNames)
	response = HttpResponse(body, content_type="application/json")
	return response


'''
DELETE Method

URL Path: 'assembly/<str:parentName>/child/part/<str:childrenNames>'

remove one or more parts from an assembly
'''
def removePartsFromAssembly(request, parentName, childrenNames):
	if request.method != "DELETE":
		return HttpResponseBadRequest()

	# Validation on parent name
	if parentName not in models.assemblies:
		if parentName in models.parts:
			return HttpResponseBadRequest("The parent assembly is a part.")
		else:
			return HttpResponseBadRequest("The parent assembly does not exist.")

	# Validation on child names
	childNames = childrenNames.split(",")
	for childName in childNames:
		if childName not in models.parts:
			if childName in models.assemblies:
				return HttpResponseBadRequest(f"The specified part {childName} is an assembly.")
			else:
				return HttpResponseBadRequest(f"The part {childName} does not exist.")

	# Make sure all parts exist in the assembly
	parentAssembly = models.assemblies[parentName]
	childParts = set([models.parts[childName] for childName in childNames]) # use set to remove dupes
	for childPart in childParts:
		if childPart not in parentAssembly.children:
			return HttpResponseBadRequest( \
				f"The part {childName} was not found in the first level of the assembly.")

	# Perform removal
	for childPart in childParts:
		childPart = models.parts[childName]
		parentAssembly.children.remove(childPart)
		childPart.parents.remove(parentAssembly)
		checkConvertBackToPart(parentAssembly)

	return HttpResponse()
