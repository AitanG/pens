from django.urls import path
from . import views


urlpatterns = [
    # create a new part
    # delete a part (thereby also deleting the part from its parent assemblies)
    path('part', views.part),

    # list all parts
    path('part/', views.listParts),

    # add one or more parts as "children" to a "parent" part, which then becomes an assembly
    path('part/<slug:parentName>/child/part', views.addPartsToPart),

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
    path('assembly/<slug:name>/child/', views.listChildrenOfAssembly),

    # list all the first-level children of a specific assembly
    path('assembly/<slug:name>/child/first/', views.listTopChildrenOfAssembly),

    # remove one or more parts from an assembly
    path('assembly/<slug:name>/child/part', views.removePartsFromAssembly),

	# list all parts in a specific assembly (which are not subassemblies)
    path('assembly/<slug:name>/child/part/', views.listPartsInAssembly),

]