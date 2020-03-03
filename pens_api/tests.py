from django.test import Client, TestCase
from . import models
import json


def reset():
	models.parts = {}
	models.assemblies = {}


class SimpleTest(TestCase):
	def setUp(self):
		self.c = Client()

	def testCreateDeletePart(self):
		reset()

		response = self.c.post('/pens/part/barrel-bottom')
		self.assertEqual(response.status_code, 200)

		response = self.c.post('/pens/part/barrel-bottom')
		self.assertEqual(response.status_code, 400)

		self.c.post('/pens/part/engine')
		response = self.c.delete('/pens/part/engine')
		self.assertEqual(response.status_code, 200)

		response = self.c.delete('/pens/part/engine')
		self.assertEqual(response.status_code, 400)

	def testAddRemoveParts(self):
		reset()

		self.c.post('/pens/part/ink-cartridge')
		self.c.post('/pens/part/ink')

		# Add part to assembly
		response = self.c.post('/pens/part/ink-cartridge/child/part/ink')
		self.assertEqual(response.status_code, 200)

		response = self.c.get('/pens/assembly/')
		self.assertEqual(response.content, b'["ink-cartridge"]')

		response = self.c.get('/pens/assembly/ink-cartridge/child/')
		self.assertEqual(response.content, b'["ink"]')

		# Remove part from assembly
		response = self.c.delete('/pens/assembly/ink-cartridge/child/part/ink')
		self.assertEqual(response.status_code, 200)

		# Add the part back to the assembly
		response = self.c.post('/pens/part/ink-cartridge/child/part/ink')
		self.assertEqual(response.status_code, 200)

		# Now delete the part
		response = self.c.delete('/pens/part/ink')
		self.assertEqual(response.status_code, 200)

		# Make sure the delete was successful
		response = self.c.get('/pens/part/')
		self.assertEqual('"ink"' not in str(response.content), True)

		# Make sure the ink-cartridge is no longer considered an assembly
		response = self.c.get('/pens/assembly/ink-cartridge/child/')
		self.assertEqual(response.content, b'The parent assembly does not exist.')

		response = self.c.get('/pens/part/')
		self.assertEqual('"ink-cartridge"' in str(response.content), True)

