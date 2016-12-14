# coding:utf8
# @author:nick
# @company:joyme
# 公众号相关model
from django.db import models
from django_wx_joyme.utils.string_util import create_random_str
from django.contrib.admin.options import ModelAdmin


class PublicAccount(models.Model):
    # 公众号配置表

    encrypt_mode_choices = (('normal', u'明文模式'), ('compatible', u'兼容模式'), ('safe', u'安全模式'))
    public_name = models.CharField(max_length=255, verbose_name=u'公众号名称')
    token = models.CharField(max_length=255, verbose_name=u'公众号token', editable=False)
    app_id = models.CharField(max_length=255, verbose_name=u'公众号id', unique=True)
    app_secret = models.CharField(max_length=255, verbose_name=u'公众号secret')
    encrypt_mode = models.CharField(max_length=255, choices=encrypt_mode_choices, verbose_name=u'消息加解密方式')
    encrypt_aes_key = models.CharField(max_length=255, verbose_name=u'公众平台开发者选项中的 EncodingAESKey', null=True,
                                       blank=True)
    # access_token = models.CharField(max_length=255, verbose_name=u'公众号access token', null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'公众号创建时间', editable=False)
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'公众号更新时间', editable=False)
    public_type = models.CharField(max_length=25,
                                   choices=[('test', u'测试号'), ('subscribe', u'订阅号'), ('service', u'服务号')])

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        自定义save 方法
        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return:
        """
        if self.encrypt_mode != 'normal' and self.encrypt_aes_key == '':
            raise Exception(u'没有输入正确的EncodingAESKey')
        self.token = create_random_str()
        super(PublicAccount, self).save(force_insert, force_update, using, update_fields)

    def __unicode__(self):
        return self.public_name

    class Meta:
        verbose_name=verbose_name_plural = u'公众号配置'
        ordering = ["-id"]


class PublicMenuConfig(models.Model):
    menu_cats = [
        ('click', u'点击事件'),
        ('view', u'绑定网址'),
        ('scancode_push', u'自动扫码'),
        ('scancode_waitmsg', u'扫码事件'),
        ('pic_sysphoto', u'自动拍照发图'),
        ('pic_photo_or_album', u'拍照或相册发图'),
        ('pic_weixin', u'微信相册发图'),
        ('location_select', u'弹出地理位置选择器'),
        ('media_id', u'下发消息'),
        ('view_limited', u'跳转图文消息url')
    ]
    public = models.ForeignKey(PublicAccount, verbose_name=u'公众号')
    menu_type = models.CharField(max_length=255, choices=menu_cats, verbose_name=u'菜单类型')
    menu_name = models.CharField(max_length=255, verbose_name=u'菜单名称')
    created_time = models.DateTimeField(auto_created=True, verbose_name=u'创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    info = models.TextField(verbose_name=u'信息内容')
    menu_level=models.IntegerField(choices=((1,u'一级菜单'),(2,u'二级菜单')))
