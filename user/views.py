from django.shortcuts import render
from django.views import View

# Create your views here.

from rest_framework.views import APIView


class UserView(APIView):
    """
    获取用户的信息，用户通过扫描二维码进入系统后，小程序会调用login命令，生成一个code，在用户已经授权过用户信息后，小程序会通过wx.request接口将用户数据与code发送到此View。
    如果用户未在系统内存在，则此接口会创建用户。
    """
    def post(self,request):
        pass
