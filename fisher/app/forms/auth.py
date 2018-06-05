from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮箱不规范')])  #在这犯了个错，验证函数DataRequired函数忘了加()
    password = PasswordField(validators=[
        DataRequired(message='密码不可以为空，请输入你的密码'), Length(6,32)])
    nickname = StringField(validators=[
        DataRequired(), Length(2, 10, message='昵称至少需要两个字符，最多十个字符')])


    #编写自定义的验证器
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('用户名已存在')


class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮箱不规范')])
    password = PasswordField(validators=[
        DataRequired(message='密码不可以为空，请输入你的密码'), Length(6,32)])


class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(8,64), Email(message='电子邮箱不规范')])


class ResetPasswordForm(Form):
    password1 = PasswordField(validators=[DataRequired(),
                                          Length(6,32, message='密码长度至少需要6到32个字符'),
                                          EqualTo('password2', message='两次输入的密码不一致')])
    password2 = PasswordField(validators=[DataRequired(), Length(6,32)])


class ChangePasswordForm(Form):
    old_password = PasswordField('原有密码', validators=[DataRequired()])
    new_password1 = PasswordField('新密码', validators=[
        DataRequired(), Length(6,20, message='密码长度至少需要在6到20个字符之间'), EqualTo('new_password2', message='两次输入的密码不一致')
    ])
    new_password2 = PasswordField('确认新密码', validators=[DataRequired()])