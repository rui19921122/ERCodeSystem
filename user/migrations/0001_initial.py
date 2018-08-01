# Generated by Django 2.0.7 on 2018-08-01 02:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OuterUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=20, null=True, verbose_name='姓名')),
                ('wechat_name', models.CharField(max_length=100, verbose_name='微信名称')),
                ('wechat_id', models.CharField(max_length=100, verbose_name='微信id')),
                ('inner_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='系统内姓名')),
            ],
            options={
                'verbose_name': '用户管理',
                'permissions': [('can_set_username', '能够更改其他用户的姓名'), ('can_set_user_qrcode_permission', '能够更改其他用户是否可以添加二维码')],
            },
        ),
    ]
