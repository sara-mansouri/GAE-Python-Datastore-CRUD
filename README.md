# Guestbook with Namespaces

This application is for practicing programming in Python an storing 
data in GAE Datastore. Main functionalities are entering, updating and 
deleting data of database. data is received from a small form and is 
displayed on a table.
You Can see a demo of application here:
http://s-mansouri.appspot.com/

This application implements the Python [Guestbook sample][7] but uses
datastore namespaces to keep values in separate places.
Guestbook is an example application showing basic usage of Google App
Engine.Data is stored in App Engine (NoSQL) High Replication Datastore 
(HRD) and retrieved using a strongly consistent(ancestor) query.

## Products
- [App Engine][1]

## Language
- [Python][2]

## APIs
- [NDB Datastore API][3]
- [Users API][4]

## Dependencies
- [webapp2][5]
- [jinja2][6]

[1]: https://developers.google.com/appengine
[2]: https://python.org
[3]: https://developers.google.com/appengine/docs/python/ndb/
[4]: https://developers.google.com/appengine/docs/python/users/
[5]: http://webapp-improved.appspot.com/
[6]: http://jinja.pocoo.org/docs/
[7]: https://github.com/GoogleCloudPlatform/appengine-guestbook-python/tree/part6-staticfiles
