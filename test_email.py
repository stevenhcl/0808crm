
from datetime import datetime, timedelta
import uuid
from hashlib import md5,sha256

if __name__ == '__main__':
    td = timedelta(minutes=10)
    st = datetime.now() + td
    str_time = str(st.timestamp()).split('.')[0]
    # print(str_time)

    # uuid随机数的激活码
    # ud = str(uuid.uuid4())
    ud = ''.join(str(uuid.uuid4()).split('-'))
    # print(ud)
    pwd1 = 'Aa12345.'
    sha2561 = sha256(pwd1.encode('utf-8'))
    print(sha2561)
    md5_pwd1 = md5(pwd1.encode('utf-8'))
    print(md5_pwd1)

    pwd = 'Aa12345.'
    md5_pwd = md5(pwd.encode('utf-8')).hexdigest()
    print(md5_pwd)
    print(len(md5_pwd))
    sha256 = sha256(pwd.encode('utf-8')).hexdigest()
    print(sha256)
    print(len(sha256))







    username = 'test'
    code = ud
    time_stamp = str_time
    html = """
              <html>
                  <body>
                      <div>Python 邮件发送测试...</div>
                      <div>
                          欢迎您注册CRM管理系统，请点击此链接进行激活：
                          <a href="http://localhost:8000/active_accounts/?username=username&code=code&timestamp=121232311">
                              http://localhost:8000/active_accounts/?username={}&amp;code= {}&amp;timestamp= {}
                          </a>
                      </div>

                  <body>
              </html>
          """.format(username, code, time_stamp)
    # print(html)