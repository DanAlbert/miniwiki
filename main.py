import webapp2
from webapp2 import uri_for

import jinja2
import os

from models import Page


BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))


def create_default_page(page_title):
    default_text = ('This page is brand new. ' +
                    'You can edit it by clicking the link above.')

    page = Page(title=page_title, text=default_text)
    page.put()
    return page


class PageHandler(webapp2.RequestHandler):
    def get(self, page_title='Main Page'):
        page = Page.all().filter('title =', page_title).get()
        if not page:
            page = create_default_page(page_title)

        data = {
            'page': page,
            'uri_for': uri_for,
        }

        template = jinja.get_template('page.html')
        return self.response.out.write(template.render(data))

    def post(self, page_title):
        page = Page.all().filter('title =', page_title).get()
        text = self.request.get('text')
        page.text = text
        page.put()
        self.redirect(uri_for('page', page_title=page_title))


class PageEditHandler(webapp2.RequestHandler):
    def get(self, page_title):
        page = Page.all().filter('title =', page_title).get()

        data = {
            'page': page,
            'uri_for': uri_for,
        }

        template = jinja.get_template('page-edit.html')
        return self.response.out.write(template.render(data))


app = webapp2.WSGIApplication([
        webapp2.Route(r'/', handler=PageHandler, name='main-page'),
        webapp2.Route(r'/<page_title>', handler=PageHandler, name='page'),
        webapp2.Route(r'/<page_title>/edit', handler=PageEditHandler,
                      name='edit-page'),
    ], debug=True)
