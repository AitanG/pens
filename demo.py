'''
Libraries
'''
import requests
import json


'''
Constants
'''
BASE_URL = "http://127.0.0.1:8000"
DIVIDER = "---------------------"


'''
Create parts
'''
# Pen parts
requests.post(f"{BASE_URL}/pens/part/metal%20barrel%20bottom")
requests.post(f"{BASE_URL}/pens/part/metal%20barrel%20top")
requests.post(f"{BASE_URL}/pens/part/plastic%20barrel%20bottom")
requests.post(f"{BASE_URL}/pens/part/plastic%20barrel%20top")
requests.post(f"{BASE_URL}/pens/part/metal%20pocket%20clip")
requests.post(f"{BASE_URL}/pens/part/plastic%20pocket%20clip")
requests.post(f"{BASE_URL}/pens/part/metal%20thruster")
requests.post(f"{BASE_URL}/pens/part/plastic%20thruster")
requests.post(f"{BASE_URL}/pens/part/cam")
requests.post(f"{BASE_URL}/pens/part/rubber%20grip")
requests.post(f"{BASE_URL}/pens/part/spring")
requests.post(f"{BASE_URL}/pens/part/ink%20cartridge")
requests.post(f"{BASE_URL}/pens/part/cartridge%20body")
requests.post(f"{BASE_URL}/pens/part/cartridge%20cap")
requests.post(f"{BASE_URL}/pens/part/writing%20tip")
requests.post(f"{BASE_URL}/pens/part/ink")

# Package parts
requests.post(f"{BASE_URL}/pens/part/box%20top")
requests.post(f"{BASE_URL}/pens/part/box%20bottom")
requests.post(f"{BASE_URL}/pens/part/box%20insert")

# Pens
requests.post(f"{BASE_URL}/pens/part/blue%20metal%20pen")
requests.post(f"{BASE_URL}/pens/part/blue%20plastic%20pen")
requests.post(f"{BASE_URL}/pens/part/red%20metal%20pen")
requests.post(f"{BASE_URL}/pens/part/red%20plastic%20pen")

# Packages
requests.post(f"{BASE_URL}/pens/part/blue%20metal%20pen%20package")
requests.post(f"{BASE_URL}/pens/part/blue%20plastic%20pen%20package")
requests.post(f"{BASE_URL}/pens/part/red%20metal%20pen%20package")
requests.post(f"{BASE_URL}/pens/part/red%20plastic%20pen%20package")


'''
Construct pen assemblies (top down)
'''
# Blue metal
requests.post(f"{BASE_URL}/pens/part/blue%20metal%20pen%20package/child/part/blue%20metal%20pen,box%20top,box%20bottom,box%20insert")
requests.post(f"{BASE_URL}/pens/part/blue%20metal%20pen/child/part/metal%20barrel%20bottom,metal%20barrel%20top,metal%20pocket%20clip,metal%20thruster,cam,rubber%20grip,spring,ink%20cartridge")

# Blue plastic
requests.post(f"{BASE_URL}/pens/part/blue%20plastic%20pen%20package/child/part/blue%20plastic%20pen,box%20top,box%20bottom,box%20insert")
requests.post(f"{BASE_URL}/pens/part/blue%20plastic%20pen/child/part/plastic%20barrel%20bottom,plastic%20barrel%20top,plastic%20pocket%20clip,plastic%20thruster,cam,rubber%20grip,spring,ink%20cartridge")

# Red metal
requests.post(f"{BASE_URL}/pens/part/red%20metal%20pen%20package/child/part/red%20metal%20pen,box%20top,box%20bottom,box%20insert")
requests.post(f"{BASE_URL}/pens/part/red%20metal%20pen/child/part/metal%20barrel%20bottom,metal%20barrel%20top,metal%20pocket%20clip,metal%20thruster,cam,rubber%20grip,spring,ink%20cartridge")

# Red plastic
requests.post(f"{BASE_URL}/pens/part/red%20plastic%20pen%20package/child/part/red%20plastic%20pen,box%20top,box%20bottom,box%20insert")
requests.post(f"{BASE_URL}/pens/part/red%20plastic%20pen/child/part/plastic%20barrel%20bottom,plastic%20barrel%20top,plastic%20pocket%20clip,plastic%20thruster,cam,rubber%20grip,spring,ink%20cartridge")

# Now construct ink cartridge
requests.post(f"{BASE_URL}/pens/part/ink%20cartridge/child/part/cartridge%20body,cartridge%20cap,writing%20tip,ink")


'''
Test queries
'''
print("List Parts")
print(DIVIDER)
r = requests.get(f"{BASE_URL}/pens/part/")
for item in r.json():
	print(item)
print("")

print("List Component Parts")
print(DIVIDER)
r = requests.get(f"{BASE_URL}/pens/part/component/")
for item in r.json():
	print(item)
print("")

print("List Orphan Parts")
print(DIVIDER)
r = requests.get(f"{BASE_URL}/pens/part/orphan/")
for item in r.json():
	print(item)
print("")

print("List Assemblies Containing Part - metal barrel bottom")
print(DIVIDER)
r = requests.get(f"{BASE_URL}/pens/part/metal%20barrel%20bottom/assembly/")
for item in r.json():
	print(item)
print("")

print("List Assemblies")
print(DIVIDER)
r = requests.get(f"{BASE_URL}/pens/assembly/")
for item in r.json():
	print(item)
print("")

print("List Top-Level Assemblies")
print(DIVIDER)
r = requests.get(f"{BASE_URL}/pens/assembly/top/")
for item in r.json():
	print(item)
print("")

print("List Subassemblies")
print(DIVIDER)
r = requests.get(f"{BASE_URL}/pens/assembly/subassembly/")
for item in r.json():
	print(item)
print("")

print("List Children - blue plastic pen")
print(DIVIDER)
r = requests.get(f"{BASE_URL}/pens/assembly/blue%20plastic%20pen/child/")
for item in r.json():
	print(item)
print("")

print("List First-Level Children - red metal pen")
print(DIVIDER)
r = requests.get(f"{BASE_URL}/pens/assembly/red%20metal%20pen/child/first/")
for item in r.json():
	print(item)
print("")

print("List Parts In Assembly - red plastic pen package")
print(DIVIDER)
r = requests.get(f"{BASE_URL}/pens/assembly/red%20plastic%20pen%20package/child/part/")
for item in r.json():
	print(item)
print("")

print("List Parts In Assembly - red plastic pen")
print(DIVIDER)
r = requests.get(f"{BASE_URL}/pens/assembly/red%20plastic%20pen/child/part/")
for item in r.json():
	print(item)
print("")

print("Remove Parts From Assembly - red plastic pen, (spring, plastic thruster); List Parts In Assembly - red plastic pen")
print(DIVIDER)
requests.delete(f"{BASE_URL}/pens/assembly/red%20plastic%20pen/child/part/spring,plastic%20thruster")

r = requests.get(f"{BASE_URL}/pens/assembly/red%20plastic%20pen/child/part/")
for item in r.json():
	print(item)
print("")

print("Delete Part - ink; List Parts; List Children - blue plastic pen")
print(DIVIDER)
requests.delete(f"{BASE_URL}/pens/part/ink")

r = requests.get(f"{BASE_URL}/pens/part/")
for item in r.json():
	print(item)
print(DIVIDER)

r = requests.get(f"{BASE_URL}/pens/assembly/blue%20plastic%20pen/child/")
for item in r.json():
	print(item)
print("")
