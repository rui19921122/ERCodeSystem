from django.urls import reverse
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import Group, Permission

from user.models import OuterUser


class WxUserSerializer(serializers.Serializer):
    """
    小程序发起的用户信息,method post.
    """
    avatarUrl = serializers.URLField(required=True, help_text='用户头像网址')
    nickName = serializers.CharField(required=True, help_text='用户微信名称')
    code = serializers.CharField(required=True, help_text='通过小程序login方法得到的code')


class UpdateUsernameAndPermissionSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, help_text='设定的用户名')
    permission = serializers.ChoiceField(choices=(('none', '无权限用户'),
                                                  ('normal', '普通权限用户'),
                                                  ('admin', '管理员权限用户')
                                                  ),
                                         help_text='管理员用户可调用此API设置其他用户的权限及姓名，无权限用户即指仅可注册系统，无法通过扫描二维码查看信息，无法添加自己的二维码设备',
                                         required=False
                                         )

    def validate(self, attrs):
        """
        permission和username必须指定一个
        :param attrs:
        :return:
        """
        if attrs['username'] or attrs['permission']:
            return attrs
        else:
            raise ValidationError("用户姓名或者权限必需指定一个")

    def create(self, validated_data):
        raise NotImplementedError("无法通过此api创建用户，请使用小程序首次登陆创建")

    def update(self, instance, validated_data):
        assert isinstance(instance, OuterUser)
        username = validated_data.get('username')
        permission = validated_data.get('permission')
        if username:
            instance.username = username or instance.username
            instance.save()
        if permission:
            # 如果设置了permission字段，则开始设置用户权限组
            # 首先清空用户相关权限
            instance.inner_user.groups.filter().delete()
        if permission == 'none':
            # 如果用户权限被设置为none，则不添加任何权限
            pass
        elif permission == 'normal':
            return instance
