from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpRequest
from LegacySite.models import *
from LegacySite.views import *

import json


# Create your tests here.

class Testing(TestCase):
	def clientSetUp(self):
		self.client = Client()


	def XSS_gift_test(self):
		product_obj = Product.objects.create(product_name = 'test', product_image_path='test', recommended_price = 1, description = 'test')
		response = self.client.get('/gift', {'director': '<a>test</a>'})
		self.assertContains(response,"&lt;a&gt;test&lt;/a&gt;", status_code=200)

	def XSS_buy_test(self):
		product_obj = Product.objects.create(product_name = 'test', product_image_path='test', recommended_price = 1, description = 'test')
		response = self.client.get('/buy', {'director': '<a>test</a>'})
		self.assertContains(response,"&lt;a&gt;test&lt;/a&gt;", status_code=200)

	def CSRF_test(self):
		product_obj = Product.objects.create(product_name = 'test', product_image_path='test', recommended_price = 1, description = 'test')
		response = self.client.get(reverse('Gift a Card'))
		self.assertContains(response,'csrfmiddlewaretoken')

	def SQLinjection_test(self):
		password = '1234567'
		user_test = User.objects.create(username='Hacker', password='1234567')
		data = io.StringIO('{"merchant_id": "NYU Apparel Card", "customer_id": "jerry84716@gmail.com", "total_value": "100", "records": [{"record_type": "amount_change", "amount_added": 2000, "signature": \'union select password from LegacySite_user where username = 'admin'--"}]}')
		filename="newcard(2).gftcard"
		response = self.client.post(reverse('Use a card'), {'card_data': data, 'filename' :filename, 'card_supplied': True, 'card_fname': 'test'},)
		self.assertContains(response,password)

