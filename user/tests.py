from django.test import TestCase
from .models import OuterUser
from django.contrib.auth.models import Group, Permission
from rest_framework.test import APITestCase
from django.urls import reverse
from .serializers import UpdateUsernameAndPermissionSerializer
from rest_framework import status


# Create your tests here.

class TestCreateUser(APITestCase):
    def setUp(self):
        # 创建一个基本用户
        self.admin_user = OuterUser.create_user('test', '123456')
        # 创建一个管理员用户组
        self.admin_group = Group.objects.create(name='admin user')
        self.admin_group.permissions.add(Permission.objects.get(codename='can_set_username'))

        self.admin_user.inner_user.groups.add(self.admin_group)

    def test_create_user(self):
        # 测试create user 函数是否可以运行
        wechat_name = 'test_name'
        wechat_id = '123456'
        user = OuterUser.create_user(wechat_name, wechat_id)
        self.assertIsInstance(user, OuterUser, 'create user failed')

    def test_can_set_username(self):
        # 测试set username函数是否可以运行
        USERNAME = 'TEST_USERNAME'
        self.admin_user.set_username(USERNAME)
        self.admin_user = OuterUser.objects.get(pk=self.admin_user.pk)
        self.assertEqual(self.admin_user.username, USERNAME, 'username not equal')

    def test_admin_can_update_username(self):
        # 测试管理员用户是否可以修改任意一个用户的名称
        changed_user = OuterUser.create_user('changed_user', '123456')
        self.client.force_login(self.admin_user.inner_user)
        url = reverse('update username and permission', kwargs={'pk': changed_user.inner_user_id})
        res = self.client.put(url, {'username': 'changed_username'})
        changed_user.refresh_from_db()
        self.assertEqual(res.status_code, 200)
        self.assertEqual('changed_username', changed_user.username)
        self.client.logout()

    def test_a_normal_user_can_not_update_username(self):
        # 测试一个非管理用户是否不可以修改任意一个用户的名称
        changed_user = OuterUser.create_user('changed_user2', '123456')
        normal_user = OuterUser.create_user('normal_user', '123456')
        self.client.force_login(normal_user.inner_user)
        url = reverse('update username and permission', kwargs={'pk': changed_user.inner_user_id})
        res = self.client.put(url, {'username': 'changed_username', 'user_id': changed_user.id})
        changed_user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(changed_user.username, '')
