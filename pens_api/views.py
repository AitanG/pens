from django.shortcuts import render
from django.http import *
from . import models
import json

# TODO: add method to each comment header

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
Helper method that recursively finds all parts used to create a parent assembly.

'''
def getChildrenOfAssembly(parentAssembly, aggregatedChildren):
	childrenParts = [child for child in parentAssembly.children if child.componentType == "part"]
	aggregatedChildren.update(childrenParts)

	if childrenParts != len(parentAssembly.children):
		# Recursive case: not all children are parts
		childrenAssemblies = [child for child in parentAssembly.children if child.componentType == "assembly"]
		for child in childrenAssemblies:
			getChildrenOfAssembly(childrenAssemblies, aggregatedChildren)


'''
Helper method that recursively finds all assemblies containing a component.

'''
def getAssembliesContaining(component, assembliesContaining):
	if not component.parents:
		# Base case: current component has no parents
		return

	assembliesContaining.update(component.parents)

	for parent in component.parents:
		getAssembliesContaining(parent, assembliesContaining)


'''
API Method

URL Path: 'part/<slug:name>'

create a new part
delete a part (thereby also deleting the part from its parent assemblies)

'''
def part(request, name):
	if request.method == "POST":
		return createPart(request, name)
	elif request.method == "DELETE":
		return deletePart(request, name)
	else:
		return HttpResponseBadRequest()


'''
API Method

URL Path: 'part/'

list all parts

'''
def listParts(request):
	if request.method != "GET":
		return HttpResponseBadRequest()

	body = json.dumps(list(models.parts.keys()))
	response = HttpResponse(body, content_type="application/json")
	return response


'''
API Method

URL Path: 'part/<slug:parentName>/child/part/<slug:childrenNames>'

add one or more parts as "children" to a "parent" part, which then becomes an assembly

'''
def addPartsToPart(request, parentName, childrenNames):
	if request.method != "POST":
		return HttpResponseBadRequest()

	if parentName not in models.parts:
		return HttpResponseBadRequest("The parent part does not exist.")

	childNames = names.split(",")
	for childName in childNames:
		if childName not in models.parts:
			return HttpResponseBadRequest(f"The child part {childName} does not exist.")

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
API Method

URL Path: 'part/orphan/'

list all orphan parts (parts with neither parents nor children)

'''
def listOrphanParts(request):
	if request.method != "GET":
		return HttpResponseBadRequest()

	orphanParts = [key for key, value in models.parts.items() if not value.parents]
	body = json.dumps(orphanParts)
	response = HttpResponse(body, content_type="application/json")
	return response


'''
API Method

URL Path: 'part/component/'

list all component parts (parts that are not subassemblies, but are included in a parent assembly)

'''
def listComponentParts(request):
	if request.method != "GET":
		return HttpResponseBadRequest()

	orphanParts = [key for key, value in models.parts.items() if value.parents]
	body = json.dumps(orphanParts)
	response = HttpResponse(body, content_type="application/json")
	return response


'''
API Method

URL Path: 'part/<slug:name>/assembly/'

list all assemblies that contain a specific child part, either directly or indirectly (via a subassembly)

'''
def listAssembliesContainingPart(request, name):
	if request.method != "GET":
		return HttpResponseBadRequest()

	if name not in models.parts:
		return HttpResponseBadRequest("The part does not exist.")

	part = models.parts[name]
	assembliesContaining = set([])
	getAssembliesContaining(part, assembliesContaining)
	body = json.dumps(list(assembliesContaining))
	response = HttpResponse(body, content_type="application/json")
	return response



'''
API Method

URL Path: 'assembly/'

list all assemblies

'''
def listAssemblies(request):
	if request.method != "GET":
		return HttpResponseBadRequest()

	assemblies = [key for key, value in models.assemblies.items()]
	body = json.dumps(assemblies)
	response = HttpResponse(body, content_type="application/json")
	return response


'''
API Method

URL Path: 'assembly/pen/'

list all top level assemblies (assemblies that are not children of another assembly)

'''
def listPens(request):
	if request.method != "GET":
		return HttpResponseBadRequest()

	assemblies = [value for key, value in models.assemblies.items() if not value.parents]
	body = json.dumps(assemblies)
	response = HttpResponse(body, content_type="application/json")
	return response


'''
API Method

URL Path: 'assembly/subassembly/'

list all subassemblies (assemblies that are children of another assembly)

'''
def listSubassemblies(request):
	if request.method != "GET":
		return HttpResponseBadRequest()

	assemblies = [value for key, value in models.assemblies.items() if value.parents]
	body = json.dumps(assemblies)
	response = HttpResponse(body, content_type="application/json")
	return response


'''
API Method

URL Path: 'assembly/<slug:parentName>/child/'

list all children of a specific assembly

'''
def listChildrenOfAssembly(request, parentName):
	if request.method != "GET":
		return HttpResponseBadRequest()

	if parentName not in models.parts:
		return HttpResponseBadRequest("The parent part does not exist.")

	parentAssembly = models.assemblies[parentName]
	children = set([])
	getChildrenOfAssembly(parentAssembly, children)
	body = json.dumps(list(children))
	response = HttpResponse(body, content_type="application/json")
	return response


'''
API Method

URL Path: 'assembly/<slug:parentName>/child/first/'

list all the first-level children of a specific assembly

'''
def listTopChildrenOfAssembly(request, parentName):
	if request.method != "GET":
		return HttpResponseBadRequest()

	if parentName not in models.parts:
		return HttpResponseBadRequest("The parent part does not exist.")

	parentAssembly = models.assemblies[parentName]
	children = [child.name for child in parentAssembly.children]
	body = json.dumps(children)
	response = HttpResponse(body, content_type="application/json")
	return response


'''
API Method

URL Path: 'assembly/<slug:parentName>/child/part/'

list all parts in a specific assembly (which are not subassemblies)

'''
def listPartsInAssembly(request, parentName):
	if request.method != "GET":
		return HttpResponseBadRequest()

	if parentName not in models.assemblies:
		return HttpResponseBadRequest("The parent assembly does not exist.")

	parentAssembly = models.assemblies[parentName]
	childParts = [child for child in parentPart.children if child.componentType == "part"]
	body = json.dumps(children)
	response = HttpResponse(body, content_type="application/json")
	return response


'''
API Method

URL Path: 'assembly/<slug:parentName>/child/part/<slug:childrenNames>'

remove one or more parts from an assembly

'''
def removePartsFromAssembly(request, parentName, childrenNames):
	if request.method != "DELETE":
		return HttpResponseBadRequest()

	if parentName not in models.assemblies:
		return HttpResponseBadRequest("The parent assembly does not exist.")

	childNames = names.split(",")
	for childName in childNames:
		if childName not in models.parts:
			return HttpResponseBadRequest(f"The part {childName} does not exist.")

	parentAssembly = models.assemblies[parentName]
	childParts = [models.parts[childName] for childName in childNames]
	for childPart in childParts:
		if childPart not in parentAssembly.children:
			return HttpResponseBadRequest( \
				f"The part {childName} was not found in the first level of the assembly.")

	for childPart in childParts:
		childPart = models.parts[childName]
		parentAssembly.children.remove(childPart)

	return HttpResponse()
