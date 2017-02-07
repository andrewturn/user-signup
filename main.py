#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, templates, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)





# class ErrorHandler(webapp2.RequestHandler):


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def user_valid(username):
    return username and USER_RE.match(username)


PASS_RE = re.compile(r"^.{3,20}$")
def password_valid(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def email_valid(email):
    return not email or EMAIL_RE.match(email)

class Signup(BaseHandler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username,
                      email = email)

        if not user_valid(username):
            params['error_username'] = "Not a valid username."
            have_error = True

        if not password_valid(password):
            params['error_password'] = "Not a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Passwords did not match."
            have_error = True

        if not email_valid(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.redirect('/welcome?username= ' + username)

class Welcome(BaseHandler):
    def get(self):
        username = self.request.get('username')
        self.response.write('Welcome,' + username)
        # if user_valid(username):
        #     self.render('welcome.html', username=username)
        # else:
        #     self.redirect('/signup')


app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/welcome', Welcome),
    ], debug=True)
