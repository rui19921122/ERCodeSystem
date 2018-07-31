from django.test import TestCase
from .models import OuterUser


# Create your tests here.

class TestCreateUser(TestCase):
    def setUp(self):
        self.user = OuterUser.create_user('test','123456')

    def test_create_user(self):
        wx_name = 'test_name'
        wx_id = '123456'
        user = OuterUser.create_user(wx_name, wx_id)
        self.assertIsInstance(user, OuterUser, 'create user failed')

    def test_can_set_username(self):
        USERNAME = 'TEST_USERNAME'
        self.user.set_username(USERNAME)
        self.user = OuterUser.objects.get(self.user.pk)
        self.assertEqual(self.user.username, USERNAME,'username not equal')
