from django.urls import path
from . import views


urlpatterns = [
    # list all parts
    path('part/', views.listParts),

    # create a new part
    # delete a part (thereby also deleting the part from its parent assemblies)
    path('part/<slug:name>', views.part),

    # add one or more parts as "children" to a "parent" part, which then becomes an assembly
    path('part/<slug:parentName>/child/part/<slug:childrenNames>', views.addPartsToPart),

    # list all orphan parts (parts with neither parents nor children)
    path('part/orphan/', views.listOrphanParts),

    # list all component parts (parts that are not subassemblies, but are included in a parent assembly)
    path('part/component/', views.listComponentParts),

	# list all assemblies that contain a specific child part, either directly or indirectly (via a subassembly)
    path('part/<slug:name>/assembly/', views.listAssembliesContainingPart),

	# list all assemblies
	path('assembly/', views.listAssemblies),

    # list all top level assemblies (assemblies that are not children of another assembly)
    path('assembly/pen/', views.listPens),

    # list all subassemblies (assemblies that are children of another assembly)
    path('assembly/subassembly/', views.listSubassemblies),

    # list all children of a specific assembly
    path('assembly/<slug:parentName>/child/', views.listChildrenOfAssembly),

    # list all the first-level children of a specific assembly
    path('assembly/<slug:parentName>/child/first/', views.listTopChildrenOfAssembly),

	# list all parts in a specific assembly (which are not subassemblies)
    path('assembly/<slug:parentName>/child/part/', views.listPartsInAssembly),

    # remove one or more parts from an assembly
    path('assembly/<slug:parentName>/child/part/<childrenNames>', views.removePartsFromAssembly),

]