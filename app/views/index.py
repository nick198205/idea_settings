# coding:utf8
# @author:nick
# @company:joyme
from django.shortcuts import render
from wechat_sdk.messages import WechatMessage
from wechat_manage.models.public_model import PublicAccount
from wechat_sdk import WechatBasic
from . import login_required, catch_error, auth_public, get_params
from . import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app.models.message import Message, MsgResponse
from wechat_manage.models.followers_model import PublicFollowers


@login_required
@catch_error
def index(request):
    """

    :param request:
    :return:
    """
    public_index = [('id', 'id'), ('public_name', u'名称'), ('public_type', u'公众号类别') \
        , ('create_time', u'创建时间'), ('public_manage', u'进入公众号')]
    page_title = u'微信管理:后台首页'
    table_title = u'选择公众号'
    # 获取公众号信息
    publics = PublicAccount.objects.all()

    table_heads = [x[1] for x in public_index]
    table_datas = []
    for public in publics:
        # todo 将默认管理起始页改为用户管理l
        public.public_manage = '<a href="/wechat/%s/followers/query">进入管理</a>' % public.id
        line = [getattr(public, key[0]) for key in public_index]
        table_datas += [line]
    return render(request, 'base/simple_table.html', locals())


@csrf_exempt
@auth_public
def reply(request, public, *args):
    """
    作为 接口的view
    实现获取request并做出响应
    :type public: WechatBasic
    :param request:
    :param public:
    :param args:
    :return:
    """
    # 判断是否为微信的验证url请求
    signature = get_params(request, name='signature')
    if signature:
        # 微信服务器验证url有效性逻辑
        nonce = get_params(request, name='nonce')
        timestamp = get_params(request, name='timestamp')
        echostr = get_params(request, name='echostr')
        if public.check_signature(signature, timestamp, nonce):
            return HttpResponse(echostr)
    # 获取微信公众号配置实例
    public_instance = args[0]
    # xml_string=request.body
    # from lxml import etree
    # xml=etree.fromstring(xml_string)

    # 使用sdk解析微信服务器发来的消息
    # sdk解析后将消息保存到实例中
    public.parse_data(request.body)
    # 从实例获取解析后的xml
    msg = public.get_message()  # type:WechatMessage
    user_instance = PublicFollowers.objects.get(public=public_instance, openid=msg.source)
    message_instance = Message(form_user=user_instance, public=public_instance, type=msg.type, create_time=msg.time,
                               msgid=msg.id)
    if msg.type == 'text':
        message_instance.content = msg.content
    try:
        message_instance.mediaid = msg.media_id
    except AttributeError:
        pass
    message_instance.save()

    pass
