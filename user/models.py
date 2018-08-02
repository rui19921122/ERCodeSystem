from django.db import models
import uuid

# Create your models here.
from guardian.decorators import permission_required


class OuterUser(models.Model):
    """
    储存用户的基本信息，包括用户姓名，微信名称，微信识别代号，部门，用户权限。
    """
    username = models.CharField(max_length=20, verbose_name='姓名', null=True, blank=True)
    inner_user = models.ForeignKey('auth.User', verbose_name='系统内姓名', on_delete=models.CASCADE)
    wechat_name = models.CharField(max_length=100, verbose_name='微信名称', )
    wechat_id = models.CharField(max_length=100, verbose_name='微信open_id')

    class Meta:
        verbose_name = '用户管理'
        permissions = [
            ('can_set_username', '能够更改其他用户的姓名和权限'),
            ('can_set_user_qrcode_permission', '能够更改其他用户是否可以添加二维码')
        ]

    def __str__(self):
        if self.username:
            return self.username
        else:
            return self.wechat_name

    def group(self):
        """
        :return: 该用户所具备的权限
        """
        return [i.name for i in self.inner_user.groups.all()]

    @classmethod
    def create_user(cls, wechat_name, wechat_id):
        """
        创建一个新的系统用户,系统密码为随机生成的密码，因此用户仅可通过微信小程序api进行登陆。
        :param wechat_name: 微信用户名
        :param wechat_id: 微信用户识别码
        :return: OuterUser
        """
        from django.contrib.auth.models import User
        new_inner_user = User.objects.create_user(username=wechat_name,
                                                  password=uuid.uuid4())
        new_outer_user = cls.objects.create(
            wechat_id=wechat_id,
            wechat_name=wechat_name,
            inner_user=new_inner_user,
            username=''
        )
        return new_outer_user

    def set_username(self, username: str):
        """
        设定用户名称
        :return: bool
        """
        try:
            self.username = str(username)
            self.save()
        except TypeError as e:
            raise TypeError(e)
        except:
            raise BaseException()
        else:
            return self
