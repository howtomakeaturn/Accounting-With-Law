from google.appengine.ext import db

import datetime
#this module defines the data structure the systems uses.
from datetime import tzinfo, timedelta  
  
class TaiwanTimeZone(tzinfo):  
  def utcoffset(self, dt):  
    return timedelta(hours=8)  
  
  def tzname(self, dt):  
    return 'CST'  
 
  def dst(self, dt):  
    return timedelta(hours=0)  


class Article(db.Model):
  author = db.StringProperty(required = True)
  title = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  created = db.DateTimeProperty(required = True)
  number = db.IntegerProperty(required=True)
  
  def sorted_and_adjusted_answers(self):
    answers = []
    for answer in self.answers.order('created'):
      answer.content = escape(answer.content)
      answer.content = answer.content.replace('\n','<br />')
      answers.append(answer)
      
    return answers
  
class Answer(db.Model):
  article = db.ReferenceProperty(required = True, reference_class=Article, collection_name='answers')
  author = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add=True)
  
class Counter(db.Model):
  value = db.IntegerProperty(required = True, default=0)
  
  
def escape(html):
  return html.replace('&', '&amp;').replace('<','&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'",'&#39;')
   
  