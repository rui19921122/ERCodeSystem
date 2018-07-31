from rest_framework import serializers


class WxUserSerializer(serializers.BaseSerializer):
    """
    小程序发起的用户信息
    """
    avatarUrl = serializers.URLField(required=True)
    nickName = serializers.CharField(required=True)
    code = serializers.CharField(required=True)


