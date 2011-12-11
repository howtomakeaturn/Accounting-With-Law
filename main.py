import os
import re
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app

import mydb
import datetime


template.register_template_library('my_filters') 
  
class MainPage(webapp.RequestHandler):
  def get(self):
    articles = mydb.Article.all().order('-created')
	  
    template_values = {
      'articles': articles
      }

    path = os.path.join(os.path.dirname(__file__), 'main/index.html')
    self.response.out.write(template.render(path, template_values))

class AddArticle(webapp.RequestHandler):
  def get(self):
    template_values={}
    path = os.path.join(os.path.dirname(__file__), 'main/add_article.html')
    self.response.out.write(template.render(path, template_values))
  
  def post(self):
    author = self.request.get('author')
    title = "[" + self.request.get('category') + "] " + self.request.get('title')
    content = self.request.get('content')
#    content = escape(self.request.get('content'))#escape the dangerous characters
#    content = content.replace('\n','<br />')#replace the line break flags
    #the following codes are RE-related, try to understand them
    #content = re.sub(r'\bhttp://\b', 'wow', content)
 ##   hyper_link = re.compile(r"(http://[^ ]+)")
 ##   content = hyper_link.sub(r'<a href="\1" target="_blank">\1</a>', content)

    # temp = re.search('http://[a-zA-Z0-9_?&\-%/.,~＃!^*_+|`=<>:"]+(?=\s)', content)
    # if temp is not None:
    #   content = content.replace(temp.group(0), '<a class="link" href="%s" target="_blank">%s</a>') % (temp.group(0), temp.group(0))
    #end problem    
    
    article_number = mydb.Counter.get_by_key_name("article_number")
    if article_number is None:
      article_number = mydb.Counter(key_name='article_number')
    article_number.value += 1
    
    article = mydb.Article(author=author,title=title,content=content,number=article_number.value,created = datetime.datetime.now(mydb.TaiwanTimeZone()))
    article.put()
    article_number.put()

    self.redirect('/')


class ReadArticle(webapp.RequestHandler):
  def get(self, number):
    article = mydb.Article.gql('WHERE number = :number', number = int(number)).get()
    
    article.content = escape(article.content)#escape the dangerous characters
    article.content = article.content.replace('\n','<br />')#replace the line break flags
    
    template_values={
      'article': article
    }    
    path = os.path.join(os.path.dirname(__file__), 'main/read_article.html')
    self.response.out.write(template.render(path, template_values))

class AddAnswer(webapp.RequestHandler):
  def post(self):
    author = self.request.get('author')
    content = self.request.get('content')
#    content = escape(self.request.get('content')).replace('\n','<br />')
    article = mydb.Article.get(self.request.get('key'))
    
    answer = mydb.Answer(author=author,content=content,article=article)
    answer.put()

    self.redirect('/article/' + str(article.number))

def escape(html):
  return html.replace('&', '&amp;').replace('<','&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'",'&#39;')
 
application = webapp.WSGIApplication(
                                     [('/', MainPage),
									   ('/add_article', AddArticle),
                                       ('/article/(\d*)', ReadArticle),
									  
									   ('/add_answer', AddAnswer),
                                      
                                      ],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()