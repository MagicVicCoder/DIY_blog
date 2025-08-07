# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6, max=128)])
    confirm  = PasswordField(
        '确认密码',
        validators=[DataRequired(), EqualTo('password', message='两次密码必须一致')]
    )
    submit   = SubmitField('注册')

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6, max=128)])
    submit   = SubmitField('登录')

class PostForm(FlaskForm):
    title   = StringField('标题', validators=[DataRequired(), Length(min=1, max=200)])
    content = TextAreaField('内容', validators=[DataRequired()])
    submit  = SubmitField('发布')

