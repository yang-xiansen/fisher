from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm, ChangePasswordForm
from app.models.base import db
from app.models.user import User
from . import web
from flask_login import login_user, logout_user, current_user
from app.libs.email import send_mail


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data) #user中的字段赋值，如email,password, nickname
            db.session.add(user)
        # db.session.commit() #这两步是写入数据库
        #     login_user(user, False)
        return redirect(url_for('web.login'))
        # user.password = generate_password_hash(form.password.data) #加密

    return render_template('auth/register.html', form=form)#将form传入前端，可以拿到错误信息，并还原用户输入的注册信息


@web.route('/login', methods=['GET', 'POST'])
def login():
    form= LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True) #(存到cookie)根据id验证用户， 在user模型中写get_id方法，获取id, remember是长久写入cookie
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)

        else:
            flash('账号不存在或密码错误')

    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            user = User.query.filter_by(email=account_email).first_or_404()
            # if not user:
            #     raise  Exception()   #first_or_404代替这两句代码

            send_mail(account_email, '重置你的密码',
                      'email/reset_password.html', user=user, token=user.generate_token())
            flash('邮箱已发送到'+ account_email+ ',请及时查收' )
            # return redirect(url_for('web.login'))
    return render_template('auth/forget_password_request.html', form=form)

#学会单元测试（不用去测试其他的代码）

@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        sucess = User.reset_password(token, form.password1.data)
        if sucess:
            flash('你的密码修改成功，请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html')


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        current_user.password = form.new_password1.data
        db.session.commit()
        flash('密码修改成功')
        return redirect(url_for('web.personal'))
    return render_template('auth/change_password.html', form=form)


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))