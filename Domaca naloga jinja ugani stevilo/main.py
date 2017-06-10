#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
        #if not params: --> napacno!
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("ugani-stevilo.html")

    def post(self):
        secret = 88
        vnos = int(self.request.get("stevilo"))
        rezultat = None
        if vnos == secret:
            rezultat = {"izpis": u"Uspelo ti je! Ves čas sem verjela vate!"}
        elif vnos > secret:
            rezultat = {"izpis": "Ha! Previsoko"}
        elif vnos < secret:
            rezultat = {"izpis": "Ha! Prenizko!"}

        return self.render_template("ugani-stevilo.html", params = rezultat)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
