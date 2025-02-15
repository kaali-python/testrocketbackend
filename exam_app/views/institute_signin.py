# -*- coding: utf-8 -*-

import json
from hashlib import md5
from base64 import b64encode

from flask.views import MethodView
from flask import render_template, redirect, request
from flask.ext.restful import reqparse

from exam_app import app
from exam_app.auth import authenticate_user
from exam_app.exceptions import AuthenticationFailure


class InstituteSignin(MethodView):
    def get(self):
        return render_template('institute_signin.html')

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('host', type=str, required=True)
        args = parser.parse_args()
        try:
            institute = authenticate_user('institute', args['username'], md5(args['password']).hexdigest(), by='username')
        except AuthenticationFailure:
            return render_template('institute_signin.html', error='auth', **args)
        token = b64encode(institute.email) + '|' + institute.password + '|' + str(institute.id) + '|' + b64encode(institute.name)
        return redirect(args['host'] + app.config['INSTITUTE_URL']+'#token='+token)
