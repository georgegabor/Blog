import os 
import jinja2
import webapp2 
from datetime import datetime, timedelta
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

################################################## The default Handler Class #################################################################################

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


################################################## The Database Model #################################################################################

class Content(db.Model):
	subject = db.StringProperty( required = True)
	content = db.TextProperty( required = True)
	created = db.DateTimeProperty( auto_now_add = True)

################################################## The FrontPage Handler #################################################################################

class MainPage(Handler):
	def render_front(self, contents=""):
		contents = db.GqlQuery("select * from Content order by created desc")
		self.render("content.html", contents=contents)

	def get(self):
		self.render_front()

################################################## The Newpost Handler #################################################################################

class NewPost(Handler):
	def render_newpost(self, subject="", contents="", error=""):
		self.render("blog.html", subject=subject , contents=contents , error=error)

	def get(self):
		self.render_newpost()

	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")		

		if subject and content:
			a = Content(subject = subject, content = content)
			a.put()
			a_id = a.key().id()
			self.redirect("/blog/%d" % a_id)
		else:
			error = "Subject and/or content missing ! Try again !"
			self.render_newpost(error=error)

################################################## The Newpost Handler #################################################################################

class PermaLink(Handler):
	def get(self, blog_id):
		# blog_id = self.request.get("")
		# blog_id = 17
		s = Content.get_by_id(int(blog_id))
		self.render("content.html", contents= [s] )

#################################################### The app ###############################################################################

				
app = webapp2.WSGIApplication([
	webapp2.Route(r'/blog', handler=MainPage),
    webapp2.Route(r'/blog/newpost', handler=NewPost),
    webapp2.Route(r'/blog/<:\d+>', handler=PermaLink)],
	debug = True)		