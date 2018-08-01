from rest_framework import serializers

from user.models import OuterUser


class WxUserSerializer(serializers.Serializer):
    """
    小程序发起的用户信息,method post.
    """
    avatarUrl = serializers.URLField(required=True, help_text='用户头像网址')
    nickName = serializers.CharField(required=True, help_text='用户微信名称')
    code = serializers.CharField(required=True, help_text='通过小程序login方法得到的code')


class UpdateUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, help_text='设定的用户名')

    def update(self, instance, validated_data):
        assert isinstance(instance, OuterUser)
        instance.username = validated_data.get('username')
        instance.save()
        return instance
