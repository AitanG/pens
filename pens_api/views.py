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
def deletePart(request):
	params = {}
	try:
		params = getRequestParams(request, "name")
	except ValueError as err:
		return HttpResponseBadRequest(err)

	if params.get("name") not in models.models["parts"]:
		return HttpResponseBadRequest("The requested part does not exist.")

	part = models.models["parts"][params.get("name")]

	# Delete the part from its parent assemblies
	for parent in part.parents:
		parent.children.remove(part)

	# Delete the part from the list of parts
	del models.models["parts"][part.name]

	return HttpResponse()


'''
Helper method that creates the part passed into the request body.

Original text:
create a new part
'''
def createPart(request):
	params = {}
	try:
		params = getRequestParams(request, "name")
	except ValueError as err:
		return HttpResponseBadRequest(err)

	name = params.get("name")
	if name in models.models["parts"]:
		return HttpResponseBadRequest("The requested part already exists.")

	part = models.Component(name, componentType="part")
	models.models["parts"][name] = part

	return HttpResponse()


'''
API Method

URL Path: 'part'

create a new part
delete a part (thereby also deleting the part from its parent assemblies)

'''
def part(request):
	if request.method == "POST":
		return createPart(request)

	elif request.method == "DELETE":
		return deletePart(request)

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

	body = json.dumps(list(models.models["parts"].keys()))
	response = HttpResponse(body, content_type="application/json")
	return response


'''
API Method

URL Path: 'part/<slug:parentName>/child/part'

add one or more parts as "children" to a "parent" part, which then becomes an assembly

'''
def addPartsToPart(request, parentName):
	if request.method != "POST":
		return HttpResponseBadRequest()

	params = {}
	try:
		params = getRequestParams(request, "names")
	except ValueError as err:
		return HttpResponseBadRequest(err)

	if parentName not in models.models["parts"]:
		return HttpResponseBadRequest("The parent part does not exist.")

	childNames = params.get("names").split(",")
	for childName in childNames:
		if childName not in models.models["parts"]:
			return HttpResponseBadRequest("The child part does not exist.")

	# Convert parent part to an assembly
	parentPart = models.models["parts"][parentName]
	parentPart.componentType = "assembly"
	parentPart.children = []
	del models.models["parts"][parentName]
	models.models["assemblies"][parentName] = parentPart

	# Link each pair of parts together hierarchically
	for childName in childNames:
		childPart = models.models["parts"][childName]
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

	orphanParts = {key: value for key, value in models.models["parts"].items() if not value.parents}
	body = json.dumps(list(orphanParts.keys()))
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

	orphanParts = {key: value for key, value in models.models["parts"].items() if value.parents}
	body = json.dumps(list(orphanParts.keys()))
	response = HttpResponse(body, content_type="application/json")
	return response


'''
API Method

URL Path: 'part/<slug:name>/assembly/'

list all assemblies that contain a specific child part, either directly or indirectly (via a subassembly)

'''
def listAssembliesContainingPart(request):
	return HttpResponse()

'''
API Method

URL Path: 'assembly/'

list all assemblies

'''
def listAssemblies(request):
	return HttpResponse()

'''
API Method

URL Path: 'assembly/pen/'

list all top level assemblies (assemblies that are not children of another assembly)

'''
def listPens(request):
	return HttpResponse()

'''
API Method

URL Path: 'assembly/subassembly/'

list all subassemblies (assemblies that are children of another assembly)

'''
def listSubassemblies(request):
	return HttpResponse()

'''
API Method

URL Path: 'assembly/<slug:name>/child/'

list all children of a specific assembly

'''
def listChildrenOfAssembly(request):
	return HttpResponse()

'''
API Method

URL Path: 'assembly/<slug:name>/child/first/'

list all the first-level children of a specific assembly

'''
def listTopChildrenOfAssembly(request):
	return HttpResponse()

'''
API Method

URL Path: 'assembly/<slug:name>/child/part'

remove one or more parts from an assembly

'''
def removePartsFromAssembly(request):
	return HttpResponse()

'''
API Method

URL Path: 'assembly/<slug:name>/child/part/'

list all parts in a specific assembly (which are not subassemblies)

'''
def listPartsInAssembly(request):
	return HttpResponse()
