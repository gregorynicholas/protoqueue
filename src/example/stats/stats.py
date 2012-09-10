from google.appengine.ext import ndb
from prototask.handler import ProtoTaskHandler
from taskmessages import TaskMessage
from datetime import datetime


class TaskDispatcher(ProtoTaskHandler):
  message_type = TaskMessage
  def run(self, task, message):
    if task == 'count':
      generate_counts(message)


def generate_counts(message):
  """Query entities for a given time slice and increments a counter for each."""
  # todo
  # generate a query based on the task paramters..
  start_datetime = datetime.utcfromtimestamp(message.start)
  end_datetime = datetime.utcfromtimestamp(message.end)
  query = ndb.Query(kind=message.kind, keys_only=True)
  query = query.filter(ndb.GenericProperty('created') >= start_datetime)
  query = query.filter(ndb.GenericProperty('created') < end_datetime)
  entities = query.fetch()
  # write the count to the datastore..
  counter = Stat_EntityKindCount(
    kind=message.kind,
    value=len(entities),
    start_slice=start_datetime,
    end_slice=end_datetime)
  counter.put()


class Stat_EntityKindCount:
  created = ndb.DateTimeProperty(auto_now_add=True)
  value = ndb.IntegerProperty(default=0)
  kind = ndb.StringProperty()
  start_slice = ndb.DateTimeProperty()
  end_slice = ndb.DateTimeProperty()
