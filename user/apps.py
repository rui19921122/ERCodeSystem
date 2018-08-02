from django.apps import AppConfig
from django.contrib.auth.models import Permission, Group
from django.db.models.signals import post_migrate


class UserConfig(AppConfig):
    name = 'user'

    def create_initial_data_for_database(**kwargs):
        """
        初始化数据库数据，保证数据库中初始用户组
        :return:
        """
        set_username = Permission.objects.get(codename='can_set_username')
        set_qrcode = Permission.objects.get(codename='can_set_user_qrcode_permission')
        normal_group = Group.objects.create(name='normal user')
        admin_group = Group.objects.create(name='admin user')
        admin_group.permissions.add(set_username)
        admin_group.permissions.add(set_qrcode)

    def ready(self):
        post_migrate.connect(self.create_initial_data_for_database)
