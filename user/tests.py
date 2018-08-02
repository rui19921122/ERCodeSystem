from django.test import TestCase
from .models import OuterUser
from django.contrib.auth.models import Group, Permission
from rest_framework.test import APITestCase
from django.urls import reverse
from .serializers import UpdateUsernameAndPermissionSerializer
from rest_framework.utils.encoders import JSONEncoder
from rest_framework import status


# Create your tests here.

class TestCreateUser(APITestCase):
    def setUp(self):
        # 创建一个基本用户
        self.admin_user = OuterUser.create_user('test', '123456')
        # 创建一个管理员用户组
        self.admin_group = Group.objects.get(name='admin group')
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

    def test_admin_can_update_user_permission(self):
        # 测试管理员用户是否可以修改任意一个用户的权限
        changed_user = OuterUser.create_user('changed_user2', '123456')
        self.client.force_login(self.admin_user.inner_user)
        url = reverse('update username and permission', kwargs={'pk': changed_user.inner_user_id})
        res = self.client.put(url, {'permission': 'admin'})
        changed_user.refresh_from_db()
        self.assertEqual(changed_user.inner_user.has_perm('user.can_set_username'), True)
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

    def test_list_users(self):
        # 测试管理员是否可以查询到所有用户
        url = reverse('query_users')
        self.client.force_login(self.admin_user.inner_user)
        users = OuterUser.objects.all()
        expert_value = []
        for user in users:
            expert_value.append({
                'username': user.username,
                'wechat_name': user.wechat_name,
                'pk': user.pk,
                'group': user.group()
            })
        res = self.client.get(url)
        self.assertListEqual(
            expert_value,
            res.json()
        )
