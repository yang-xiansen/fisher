from threading import Thread

from flask import current_app, render_template, app
from app import mail
from flask_mail import Message


#定义异步
def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_mail(to, subject, template, **kwargs):   # to, subject, template发给谁， 主题， 模板名称，传入模板的一组参数
    # msg = Message('测试邮箱', sender='271819776@qq.com', body='Test',
    #               recipients=['271819776@qq.com']) #主题， 发送者， 内容， 接收者

    msg = Message('[鱼书]' + ' ' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    #将html文件加入邮件中
    msg.html = render_template(template, **kwargs)
    app = current_app._get_current_object() #获取真实的核心对象app，而不要代理app
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()