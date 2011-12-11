import os
import re
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import mydb


class MainPage(webapp.RequestHandler):
  def get(self):
    
    articles = mydb.Article.all().order('-created')
	
    template_values = {
      'articles': articles
      }

    path = os.path.join(os.path.dirname(__file__), 'admin/index.html')
    self.response.out.write(template.render(path, template_values))

class ReadArticle(webapp.RequestHandler):
  def get(self):
    article = mydb.Article.get(self.request.get('key'))
    
    article.content = escape(article.content)#escape the dangerous characters
    article.content = article.content.replace('\n','<br />')#replace the line break flags
        
    template_values={
      'article': article
    }    
    path = os.path.join(os.path.dirname(__file__), 'admin/read_article.html')
    self.response.out.write(template.render(path, template_values))
    
    
    
class EditArticle(webapp.RequestHandler):
  def get(self):
    article = mydb.Article.get(self.request.get('key'))
#    article.content = article.content.replace('<br />','\n')
#    article.content = article.content.replace("</a>", "")

##    the_tag = re.compile(r"<a .*>")
##    article.content = the_tag.sub("", article.content)
   
    template_values={
      'article': article
    }    
    path = os.path.join(os.path.dirname(__file__), 'admin/edit_article.html')
    self.response.out.write(template.render(path, template_values))
  
  def post(self):
    article = mydb.Article.get(self.request.get('key'))
    article.author = self.request.get('author')
    article.title = self.request.get('title')
    article.content = self.request.get('content')
    
#    article.content = self.request.get('content').replace("\n", "<br />")
##    hyper_link = re.compile(r"(http://[^ ]+)")
##    article.content = hyper_link.sub(r'<a href="\1" target="_blank">\1</a>', article.content)    

    article.put()

    self.redirect('/admin/read_article?key=' + str(article.key()))
  
  
    
class DeleteArticle(webapp.RequestHandler):
  def post(self):
    article = mydb.Article.get(self.request.get('key'))
    article.delete()
    self.redirect('/admin')

    
class EditAnswer(webapp.RequestHandler):
  def get(self):
    answer = mydb.Answer.get(self.request.get('key'))
   
    template_values={
      'answer': answer
    }    
    path = os.path.join(os.path.dirname(__file__), 'admin/edit_answer.html')
    self.response.out.write(template.render(path, template_values))
  
  def post(self):
    answer = mydb.Answer.get(self.request.get('key'))
    answer.author = self.request.get('author')
    answer.content = self.request.get('content')
    
    answer.put()

    self.redirect('/admin/read_article?key=' + str(answer.article.key()))
  
      
    
    
def escape(html):
  return html.replace('&', '&amp;').replace('<','&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'",'&#39;')
     
	
application = webapp.WSGIApplication(
                                     [('/admin', MainPage),
                                      ('/admin/read_article', ReadArticle),
                                      ('/admin/edit_article', EditArticle),
                                      ('/admin/delete_article', DeleteArticle),
                                      
                                      ('/admin/edit_answer', EditAnswer),

                                      
									  ],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()