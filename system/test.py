import uuid
from datetime import datetime, timedelta
from .models import User

# print(datetime.now())


# 发邮件
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib # 发送邮件模块
from datetime import datetime

# 发送邮件
def format_addr(str):
    name, addr = parseaddr(str)
    return formataddr((Header(name, 'utf-8').encode(), addr))


# def send_email(request):
def send_email(email, username, password):
    # return render(request, 'send_email.html')
    # 用户名
    # username = request.POST.get('username')
    username = username
    # 邮箱
    # email = request.POST.get('email')
    email = email
    # 密码
    # password = request.POST.get('password')
    password = password
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
    user = User(username=username, email=email, password=password, code=code, timestamp=time_stamp)
    user.save()



    # 邮件内容

    html = """
        <html>
            <body>
                <div>Python 邮件发送测试...</div>
                <div>
                    欢迎您注册CRM管理系统，请点击此链接进行激活：
                    <a href="http://localhost:8000/active_accounts/?username=username&code=code&timestamp=121232311">
                        http://localhost:8000/active_accounts/?username={ }&amp;code= { }&amp;timestamp= { }
                    </a>
                </div>

            <body>
        </html>
    """.format(username, code, time_stamp)

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
    print('ok')
if __name__ == '__main__':
    # # 时间戳是当前时间加10分钟
    # td = timedelta(minutes=10)
    # st = str((datetime.now() + td).timestamp()).split('.')[0]
    pass
send_email('55752275@qq.com', 'stevenhcl', '123456')