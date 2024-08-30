from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST,require_GET
from .models import User

from hashlib import md5,sha256

# 发邮件
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib # 发送邮件模块
from datetime import datetime, timedelta
import uuid


# Create your views here.

# 登陆
def login_register(request):

    return render(request, 'login_register.html')

def register(request):

    return render(request, 'register.html')

# 验证用户名是否唯一
@require_POST
def unique_username(request):
    try:
        # 接收参数
        username = request.POST.get('username')
        # 查询数据库
        user = User.objects.filter(username=username)
        # user = User.objects.get(username=username)
        if user:
            return JsonResponse({'code': 1, 'msg': '用户名已存在'})
        else:
            return JsonResponse({'code': 0, 'msg': '用户名可用'})
        # 返回结果
    except User.DoesNotExist as e:
        # 异常信息说明用户不存在

        return JsonResponse({'code': -1, 'msg': e})


@require_POST
def unique_email(request):
    try:
        # 接收参数
        email = request.POST.get('email')
        # 查询数据库
        user = User.objects.filter(email=email)
        # user = User.objects.get(email=email)
        if user:
            return JsonResponse({'code': 1, 'msg': '邮箱已存在1'})
        else:
            return JsonResponse({'code': 0, 'msg': '邮箱未注册，可以使用'})
        # 返回结果
    except User.DoesNotExist as e:
        # 异常信息说明用户不存在

        return JsonResponse({'code': -1, 'msg': '邮箱未注册'})

# 发送邮件
def format_addr(str):
    name, addr = parseaddr(str)
    return formataddr((Header(name, 'utf-8').encode(), addr))

@require_POST
def send_email(request):
    try:
        # return render(request, 'send_email.html')
        # 用户名
        username = request.POST.get('username')
        # 邮箱
        email = request.POST.get('email')
        # 密码
        # md5_pwd = md5(request.POST.get('password').encode('utf-8')).hexdigest()
        pwd = md5(request.POST.get('password').encode('utf-8')).hexdigest()
        # 查询数据库
        restult_username = User.objects.filter(username=username)
        result_email = User.objects.filter(email=email)
        if restult_username:
            return JsonResponse({'code': -1, 'msg': '用户名已存在1'})
        if result_email:
            return JsonResponse({'code': -1, 'msg': '邮箱已存在2'})

        # 生成激活码
        code = ''.join(str(uuid.uuid4()).split('-'))
        # 生成时间戳 10分钟后
        td = timedelta(minutes=10)
        ts = datetime.now() + td
        time_stamp = str(ts.timestamp()).split('.')[0]
        from_addr = 'stevenhcl@163.com'
        password = 'OSYRJXZIMGICLPQE'
        # to_addr = '55752275@qq.com'
        to_addr = email
        smtp_server = 'smtp.163.com'
        # 插入数据库数据
        user = User(username=username, password=pwd, email=email, code=code, timestamp=time_stamp)
        user.save()

        # 邮件内容
        html = """
            <html>
                <body>
                    <div>Python 邮件发送测试...</div>
                    <div>
                        欢迎您注册CRM管理系统，请点击此链接进行激活：
                        <a href="http://localhost:8000/active_accounts/?username={}&code={}&timestamp={}">
                            http://localhost:8000/active_accounts/?username={}&code={}&timestamp={}
                        </a>
                    </div>
    
                <body>
            </html>
        """.format(username, code, time_stamp, username, code, time_stamp)

        msg = MIMEText(html, 'plain', 'utf-8')  # 邮件内容
        msg['From'] = format_addr('Python爱好者 <%s>' % from_addr)  # 邮件发件人
        msg['To'] = format_addr('管理员 <%s>' % to_addr)  # 邮件发件人
        msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()  # 邮件主题
        # msg['Subject'] = '来自SMTP的问候……'
        server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
        server.set_debuglevel(1)  # 打印出和SMTP服务器交互的所有信息 0不打印 1打印
        server.login(from_addr, password)  # 登录SMTP服务器
        server.sendmail(from_addr, [to_addr], msg.as_string())  # 发送邮件
        server.quit()  # 关闭连接
        # print('ok')
        # 如果邮件发送失败回滚事务


        return JsonResponse({'code': 1, 'msg': f'注册成功，请登录邮箱&nbsp;{email}激活账号'})

    except smtplib.SMTPException as e:
        # return JsonResponse({'code': -1, 'msg': '注册失败，请重新注册'})
        return e

@require_GET
def active_accounts(request):
    username = request.GET.get('username')
    code = request.GET.get('code')
    timestamp = request.GET.get('timestamp')
    try:
        user = User.objects.get(username=username, code=code, timestamp=timestamp) # 查询数据库
        now_st = int(str(datetime.now().timestamp()).split('.')[0]) # 获取当前时间戳
        if now_st > int(timestamp): # 时间戳过期
            user.delete()  # 删除用户  正常开发一般不删除用户，只做逻辑删除
            return HttpResponse('该激活链接已失效，请重新注册')
        # 激活成功，更新数据库 清除激活码 code 和时间戳 timestamp（可保留时间戳）
        # user.is_valid = True # 激活成功
        user.code = ''  # 清除激活码
        user.status = 1  # 激活成功 有效账号
        user.save()

        return HttpResponse('<h3>激活成功，请登录&nbsp;&nbsp; <a herf="http://localhost:8000/login_register">CRM管理系统 </a></h3>')

    except Exception as e : # 没有查询到
        if isinstance(e, User.DoesNotExist):
            return HttpResponse('该链接已激活成功，请转换到登录页面')
        return HttpResponse('该链接已失效激活失败，请重新偿试激活')