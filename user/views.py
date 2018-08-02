from django.contrib.auth.models import AnonymousUser, User, Permission
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from django.core.exceptions import ObjectDoesNotExist
from .models import OuterUser
from rest_framework import permissions, generics

from .serializers import WxUserSerializer, UpdateUsernameAndPermissionSerializer


# Create your views here.


class UserView(generics.GenericAPIView):
    """
    获取用户的信息
    """
    serializer_class = WxUserSerializer

    def post(self, request: Request):
        """
        获取用户的信息，用户通过扫描二维码进入系统后，小程序会调用login命令，生成一个code，
        在用户已经授权过用户信息后，小程序会通过wechat.request接口将用户数据与code发送到此View。
        如果用户未在系统内存在，则此接口会创建用户。
        """
        assert isinstance(request.user, AnonymousUser or User)
        user_data = WxUserSerializer(data=request.data)
        if user_data.is_valid():
            # 如果数据无误便向微信服务器后台发送请求，根据code获得用户认证号
            from .wechat_functions import get_user_open_id
            from custom_exceptions import WechatUserCodeError
            try:
                open_id, session_key = get_user_open_id(user_data.validated_data.get('code'))
            except WechatUserCodeError as error:
                return Response(status=status.HTTP_403_FORBIDDEN,
                                data={'error': error.args})
            try:
                outer_user = OuterUser.objects.get(wechat_id=open_id)
            except ObjectDoesNotExist:
                outer_user = OuterUser.create_user(
                    wechat_name=user_data.validated_data.get('nickName'),
                    wechat_id=open_id
                )
            token = Token.objects.get_or_create(user=outer_user.inner_user)
            return Response(
                data={'token': token[0].key,
                      'username': outer_user.username,
                      'nickname': outer_user.wechat_name})


from custom_permissions import UserCanSetUserInfo


class UpdateUsernameAndPermissionView(generics.UpdateAPIView):
    """
    管理员用户可以使用此API更改相关用户的真实姓名以及权限，以方便在系统内区分
    """
    permission_classes = (UserCanSetUserInfo, permissions.IsAuthenticated)
    serializer_class = UpdateUsernameAndPermissionSerializer

    def get_object(self):
        obj = generics.get_object_or_404(
            OuterUser, inner_user_id=self.kwargs.get(self.lookup_field)
        )
        self.check_object_permissions(self.request, obj)
        return obj


class QueryAllUserInfoView(generics.ListAPIView):
    """
    管理员可以使用此api获取所有用户
    """
    from .serializers import UserInfoSerializer
    queryset = OuterUser.objects.all()
    permission_classes = (UserCanSetUserInfo, permissions.IsAuthenticated)
    serializer_class = UserInfoSerializer