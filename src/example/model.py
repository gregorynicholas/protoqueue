from google.appengine.ext import ndb


class TestModel(ndb.Model):
  """Example entity model with a datetime property to generate counts
  for different time slices."""
  created = ndb.DateTimeProperty(auto_now_add=True)
