from django.test import TestCase
from django.http.request import (
    HttpRequest, QueryDict, RawPostDataException, UnreadablePostError,
)

from master_data.views import *
from django.contrib.auth.models import User
from master_data.models.company import Company
from master_data.models.user_profile import UserProfile

class RegisterTestCase(TestCase):
	def test_creates_user(self):
		postParams = {
		'first_name' : "Micheal",
		'middle_name' : "James",
		"last_name" : "Jackson",
		"email" : "michealjackson@example.com",
		"password" : "m_jackson",
		"confirm_password" : "m_jackson",
		"company_name" : "Jackson Enterprises",
		"company_url" : "www.jacksonenterprises.com",
		}

		request = HttpRequest()
		request.POST = postParams
		request.session = self.client.session
		request.session["key"] = 'test'
		request.session.save()
		register.RegisterView.post(self,request)

		user = User.objects.last()
		company = Company.objects.last()
		profile = UserProfile.objects.last()

		self.assertEqual(user.username, postParams["email"])
		self.assertEqual(user.email, postParams["email"])
		self.assertEqual(user.first_name, postParams["first_name"])
		self.assertEqual(user.last_name, postParams["last_name"])
		self.assertEqual(company.name, postParams["company_name"])
		self.assertEqual(company.company_url, postParams["company_url"])
		self.assertEqual(company.status, "Trial")
		self.assertEqual(company.created_by_id, user.id)
		self.assertEqual(company.updated_by_id, user.id)
		self.assertEqual(profile.middle_name, postParams["middle_name"])
		self.assertEqual(profile.company.id, company.id)
		self.assertEqual(profile.user.id, user.id)

	def test_confirm_wrong_password(self):
		postParams = {
		'first_name' : "Micheal",
		'middle_name' : "James",
		"last_name" : "Jackson",
		"email" : "michealjackson@example.com",
		"password" : "m_jackson",
		"confirm_password" : "m_jack",
		"company_name" : "Jackson Enterprises",
		"company_url" : "www.jacksonenterprises.com",
		}

		request = HttpRequest()
		request.POST = postParams
		request.session = self.client.session
		request.session["key"] = 'test'
		request.session.save()
		response = register.RegisterView.post(self,request)

		self.assertEqual(response.status_code,400)

	def test_incomplete_data(self):
		postParams = {
		'first_name' : "Micheal",
		"email" : "michealjackson@example.com",
		"password" : "m_jackson",
		"confirm_password" : "m_jack",
		"company_name" : "Jackson Enterprises",
		"company_url" : "www.jacksonenterprises.com",
		}

		request = HttpRequest()
		request.POST = postParams
		request.session = self.client.session
		request.session["key"] = 'test'
		request.session.save()
		response = register.RegisterView.post(self,request)

		self.assertEqual(response.status_code,400)

	def test_existing_email(self):
		postParams = {
		'first_name' : "Micheal",
		'middle_name' : "James",
		"last_name" : "Jackson",
		"email" : "michealjackson@example.com",
		"password" : "m_jackson",
		"confirm_password" : "m_jackson",
		"company_name" : "Jackson Enterprises",
		"company_url" : "www.jacksonenterprises.com",
		}

		request = HttpRequest()
		request.POST = postParams
		request.session = self.client.session
		request.session["key"] = 'test'
		request.session.save()
		register.RegisterView.post(self,request)
		response = register.RegisterView.post(self,request)

		self.assertEqual(response.status_code,400)
