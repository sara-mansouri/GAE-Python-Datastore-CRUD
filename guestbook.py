import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb


import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
counter = 0

# We set a parent key on the 'Greetings' to ensure that they are all in the
# same
# entity group.  Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.
def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Guestbook', guestbook_name)
       
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

        global counter
        counter +=1
        greeting.id2=counter 
        greeting.name = self.request.get('name')
        greeting.fname = self.request.get('fname')
        greeting.email = self.request.get('email')
        greeting.content = self.request.get('content')
        greeting.put()

       
        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))

class Greeting(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    
    id2 = ndb.IntegerProperty(indexed=True)
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
            'VIS':'hidden',
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class deleting(webapp2.RequestHandler):
    
    def post(self):
        delWhat = self.request.get("deletewhat")
        
        report = Greeting.query(Greeting.id2 == int(delWhat)).get()
        # Delete the entity
        report.key.delete()
        #ndb.Key(Greeting, int(delWhat)).delete()    
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))


class retrieving(webapp2.RequestHandler):
    def post(self):
        
        edWhat = self.request.get("editwhat")
        
       
        report = Greeting.query(Greeting.id2 == int(edWhat)).get()
        
        template_values = {
            'aaa_id2':edWhat,
            'aaa_name': report.name,
            'aaa_fname': report.fname,
            'aaa_email': report.email,
            'aaa_note': report.content,
            'VIS':'visibile',
            'VIS1':'hidden',
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

        #visibility = self.find_element_by_id("EditMode").get_attribute("visibility")
       # find_element_by_id("EditMode").setAttribute('style', 'visibility: visibile');
        #is_displayed()
       # visibility = visible
        #driver.find_element_by_id("capchta").send_keys(captcha_value)


        #-----------------------
        
class editing(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group.  Queries across the single entity group
        # will be consistent.  However, the write rate to a single entity group
        # should be limited to ~1/second.

        edWhat = self.request.get("edwhat")


        report = Greeting.query(Greeting.id2 == int(edWhat)).get()
        

        report.name = self.request.get('name')
        report.fname = self.request.get('fname')
        report.email = self.request.get('email')
        report.content = self.request.get('content')
        report.put()
        guestbook_name = DEFAULT_GUESTBOOK_NAME

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))

 


application = webapp2.WSGIApplication([('/', MainPage),
    ('/sign', Guestbook),
    ('/edit', editing),
    ('/delete', deleting),
    ('/retrieve', retrieving),
   
], debug=True)
