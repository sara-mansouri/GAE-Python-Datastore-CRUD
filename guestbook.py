import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb


import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


# We set a parent key on the 'Greetings' to ensure that they are all in the
# same
# entity group.  Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.
def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Guestbook', guestbook_name)


class Greeting(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    author = ndb.UserProperty()
    
    name = ndb.StringProperty(indexed=True)
    fname = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


    #def post(self):
    #    delWhat = self.request.get("deletewhat")
        
    #    report = Greeting.query(Greeting.name == delWhat).get()
    #    # Delete the entity
    #    report.key.delete()
    #    #ndb.Key(Greeting, int(delWhat)).delete()
        
    #    self.response.write(delWhat)

    def post(self):
        
        edWhat = self.request.get("editwhat")
        
       # report = Greeting.query(Greeting.name==edWhat).get()
        #report.key.delete()

        #guestbook_name = self.request.get('guestbook_name',
        #                                  DEFAULT_GUESTBOOK_NAME)
        #report = Greeting(parent=guestbook_key(edWhat))
        report = Greeting.query(Greeting.name == edWhat).get()
        
        template_values = {
            'aaa_name': report.name,
            'aaa_fname': report.fname,
            'aaa_email': report.email,
            'aaa_note': report.content,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


      
        #report.name = self.request.get('name')
        #report.fname = self.request.get('fname')
        #report.email = self.request.get('email')
        #report.content = self.request.get('content')
        #report.put()
        

       # self.response.append('name':report.name)

         #response.append({'user_id':
       # self.response.write(delWhat)

        
class editing(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group.  Queries across the single entity group
        # will be consistent.  However, the write rate to a single entity group
        # should be limited to ~1/second.

        edWhat = self.request.get("editwhat")

        report = Greeting.query(Greeting.name == edWhat).get()

        
        #greeting.name = self.request.get('name')
        #greeting.fname = self.request.get('fname')
        #greeting.email = self.request.get('email')
        #greeting.content = self.request.get('content')
        #greeting.put()

        report.name = self.request.get('name')
        report.fname = self.request.get('fname')
        report.email = self.request.get('email')
        report.content = self.request.get('content')
        report.put()
        

        
class Guestbook(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group.  Queries across the single entity group
        # will be consistent.  However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        
        greeting.name = self.request.get('name')
        greeting.fname = self.request.get('fname')
        greeting.email = self.request.get('email')
        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))

    def Edit(self):
        #https://developers.google.com/appengine/docs/python/ndb/entities#creating_entities
        #sandy = key.get()
        #sandy.email = 'sandy@gmail.co.uk'
        #sandy.put()
        Greetings = Greeting.key.get()
        greeting.name = self.request.get('name')
        greeting.fname = self.request.get('fname')
        greeting.email = self.request.get('email')
        greeting.content = self.request.get('content')
        Greeting.put()

    def Delete(self):
        #https://developers.google.com/appengine/docs/python/ndb/entities#creating_entities
        #sandy.key.delete()
        Greeting.key.delete()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'greetings': "",
            'guestbook_name': "",
            'url': "",
            'url_linktext': "",
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
    def post(self):
        firstName = self.request.get("firstName")
        familyName = self.request.get("familyName")
        self.response.out.write("First Name: " + firstName + " Family Name: " + familyName)
 

application = webapp2.WSGIApplication([('/', MainPage),
    ('/sign', Guestbook),
    ('/edit', editing),
    #('/', MainHandler)
], debug=True)
