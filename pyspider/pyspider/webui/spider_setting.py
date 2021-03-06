#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mithril
# @Date:   2015-09-21 10:18:04
# @Last Modified by:   mithril
# @Last Modified time: 2015-10-15 14:41:49


from flask import request
from flask.ext.restful import reqparse, abort, Resource, fields, marshal_with
import time
import json
import colander


from spider_serializers import Settings, Keywords, Accounts, Proxies
from .database import connect_database
from .app import app, api

setting_parser = reqparse.RequestParser()
setting_parser.add_argument('settings', location='args', required=True)
setting_parser.add_argument('proxy_on', location='args', type=bool, default=False)
setting_parser.add_argument('js_on', location='args', type=bool, default=False)
setting_parser.add_argument('max_depth', location='args', type=int, default=3)

setting_fields = {
    'name': fields.String,
}

class SpiderSettingBase(Resource):
    @property
    def db(self):
        if hasattr(self, '_db'):
            return getattr(self, '_db')
        _db = connect_database(app.config['settingdb_url'])
        setattr(self, '_db', _db)
        return _db

# @api.resource('/spider/settings/common')
# class SpiderSettingsCommon(SpiderSettingBase):
#     def get(self):
#         result = self.db.get_common_settings()
#         return result, 200 if result else 404
#
#     def put(self):
#         deserialized = Settings().deserialize(json.loads(request.data))
#         self.db.set_common_settings(request.data)
#         return {}
#
# @api.resource('/spider/keywords/common')
# class SpiderKeywordsCommon(SpiderSettingBase):
#     def get(self):
#         result = self.db.get_common_keywords()
#         return result, 200 if result else 404
#
#     def put(self):
#         deserialized = Settings().deserialize(json.loads(request.data))
#         self.db.set_common_keywords(request.data)
#         return {}


def proper_error(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return
        except colander.Invalid, e:
            errors = e.asdict()
            return errors, 500
        except Exception as e:
            return
    return wrapper


@api.resource('/spider/settings/<tp>')
class SpiderSettings(SpiderSettingBase):
    def get(self, tp):
        result = self.db.get_settings(tp)
        return result, 200 if result else 404

    def put(self, tp):
        try:
            deserialized = Settings().deserialize(json.loads(request.data))
            self.db.set_settings(tp, deserialized)
            return {}
        except colander.Invalid, e:
            errors = e.asdict()

            return errors, 500

@api.resource('/spider/keywords/<tp>')
class SpiderKeywords(SpiderSettingBase):
    def get(self, tp):
        result = self.db.get_keywords(tp)
        return result, 200 if result else 404

    def put(self, tp):
        deserialized = Keywords().deserialize(json.loads(request.data))
        self.db.set_keywords(tp, deserialized)
        return {}

@api.resource('/spider/accounts/<tp>')
class SpiderAccounts(SpiderSettingBase):
    def get(self, tp):
        result = self.db.get_accounts(tp)
        return result, 200 if result else 404

    def put(self, tp):
        deserialized = Accounts().deserialize(json.loads(request.data))
        self.db.set_accounts(tp, deserialized)
        return {}

@api.resource('/spider/proxies')
class SpiderPorxies(SpiderSettingBase):
    def get(self):
        result = self.db.get_proxies()
        return result, 200 if result else 404

    def put(self):
        deserialized = Proxies().deserialize(json.loads(request.data))
        self.db.set_proxies(deserialized)
        return {}
