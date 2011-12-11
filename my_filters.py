from google.appengine.ext import webapp  
from datetime import datetime, timedelta, tzinfo
  
register = webapp.template.create_template_register()  
 
@register.filter  
def twtz_m_d(value):
  datetime = (value + timedelta(hours=8)).replace(tzinfo=TaiwanTimeZone())
  return str(datetime.month) + "/" + str(datetime.day)

@register.filter  
def twtz(value):
  return (value + timedelta(hours=8)).replace(tzinfo=TaiwanTimeZone())
    
class TaiwanTimeZone(tzinfo):  
  def utcoffset(self, dt):  
    return timedelta(hours=8)  
  
  def tzname(self, dt):  
    return 'CST'  
 
  def dst(self, dt):  
    return timedelta(hours=0)      