# -*- coding: utf-8 -*-

import datetime
from tornado.gen import coroutine
from tornado.web import authenticated

import settings
from models import User, Role
from libs.base_handler import BaseHandler
from libs.form_error import FormError


class LoginHandler(BaseHandler):

    route_map = settings.auth_login_url

    def get(self):
        if self.current_user:
            return self.redirect(self.get_argument('next', '/'))
        else:
            return self.render('auth/login.html')

    @coroutine
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        user = yield User.objects.get(name=username)
        if not user or user.status != 'ACTIVE':
            return self.write_son({
                'errors': [FormError("用户不存在.")],
            })
        if user.check_raw_password(password):
            expire_days = None
            if self.get_argument('remember_me', None):
                expire_days = 7
            user.last_login = datetime.datetime.now()
            yield user.save()
            self.set_secure_cookie(
                settings.auth_cookie_name,
                str(user._id),
                expire_days
            )
            self.logger.info('%s %s login.' % (user._id, user.name))
            return self.write_son({'redirect': self.get_argument('next', '/')})
        else:
            return self.write_son({
                'errors': [FormError(u"密码错误.")],
            })


class LogoutHandler(BaseHandler):

    route_map = settings.auth_logout_url

    @authenticated
    def get(self):
        self.clear_cookie(settings.auth_cookie_name)
        return self.redirect(self.get_argument('next', '/'))


class ChangePasswordHandler(BaseHandler):

    route_map = r'/auth/password/change'

    @authenticated
    def get(self):
        return self.render('auth/change_password.html')

    @authenticated
    @coroutine
    def post(self):
        old_password = self.get_argument('old_password')
        user = yield User.objects.get(name=self.current_user.name)
        if not user.check_raw_password:
            return self.write_son({
                'errors': [FormError(u"旧密码输入不一致.")]
            })
        if not user or user.status != 'ACTIVE':
            return self.write_son({
                'errors': [FormError("用户不存在.")],
            })
        if user.check_raw_password(self.get_argument('old_password')):
            new_password = self.get_argument('new_password')
            new_password_again = self.get_argument('new_password_again')
            if (new_password != new_password_again):
                return self.write_son({
                    'errors': [FormError(u"两次密码输入不一致.")]
                })
            user.set_password(new_password_again)
            yield user.save()
            return self.write_son({
                'redirect': '/auth/logout'
            })
        else:
            return self.write_son({
                'errors': [FormError(u"旧密码错误.")]
            })
