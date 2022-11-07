from django.test import TestCase
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import ProfileList

# Create your tests here.
class ViewTests(TestCase):

    def setUp(self):    #テスト用データの登録
        self.user = User.objects.create(
            username='test_user',
        )
        ProfileList.objects.create(
            author=self.user,
            image=""
        )
    
    def test_get_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_get_login(self):
        client = Client()
        client.logout()
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
    
    def test_get_create(self):
        client = Client()
        client.logout()
        response = self.client.get(reverse("user_create"))
        self.assertEqual(response.status_code, 200)
    
    def test_get_explanation(self):
        response = self.client.get('/explanation')
        self.assertEqual(response.status_code, 200)
    
    def test_get_board_explanation(self):
        response = self.client.get('/board_explanation')
        self.assertEqual(response.status_code, 200)
    
    def test_get_contact(self):
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 200)
    
    def test_get_profile(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_get_board_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('board_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_get_user_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_get_user_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
