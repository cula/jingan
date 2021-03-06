# -*- coding: utf-8 -*-

import json
import settings
import functools
import logging
import datetime
from tornado.web import RequestHandler, HTTPError, URLSpec
from tornado.gen import coroutine
from bson.objectid import ObjectId
from models import User, Role
from libs.json_encoder import ComplexEncoder


def authorized(role_keys=['admin']):
    def __authorized(func):
        @functools.wraps(func)
        def __wrapper(self, *args, **kwargs):
            try:
                if self.current_user.role.key in role_keys:
                    return func(self, *args, **kwargs)
            except:
                pass
            self.redirect("/")
        return __wrapper
    return __authorized


class BaseHandler(RequestHandler):

    route_map = None
    route_kwargs = None
    route_name = None

    context = dict()
    query = ''
    page = settings.default_active_page
    count_per_page = settings.default_count_per_page

    logger = logging.getLogger("tornado.application")

    errors = list()

    SOURCE_LIST_DISPLAY = {
        '京东': '京东',
        '天猫': '天猫',
        '苏宁': '苏宁',
        '一号店': '一号店',
        '飞牛': '飞牛',
    }

    @classmethod
    def get_url_spec(cls):
        return URLSpec(cls.route_map, cls, cls.route_kwargs, cls.route_name)

    @classmethod
    def to_son(cls, obj):
        return json.dumps(obj, cls=ComplexEncoder)

    @classmethod
    def from_son(cls, string):
        return json.loads(string)

    @coroutine
    def prepare(self):
        auth_cookie = self.get_secure_cookie(settings.auth_cookie_name, None)
        if auth_cookie:
            try:
                user_id = str(auth_cookie, 'utf-8')
                if user_id:
                    user = yield User.objects.get(ObjectId(user_id))
                    if user:
                        user.last_login = datetime.datetime.now()
                        self.current_user = user
                        user.save()
            except Exception as e:
                self.logger.info(e)
        try:
            self.query = self.get_argument('q')
            self.context['q'] = self.query
        except:
            pass
        try:
            self.page = int(self.get_argument('p'))
            if self.page < 1:
                raise
            self.context['p'] = self.page
        except:
            pass

    def write_son(self, obj, status_code=200):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self._status_code = status_code
        return self.write(self.to_son(obj))
