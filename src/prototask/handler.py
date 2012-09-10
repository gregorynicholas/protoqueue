from webapp2 import RequestHandler
from google.appengine.ext.ndb import toplevel
from google.appengine.api.taskqueue import InvalidTaskError
from .proto import message_from_json_str


__all__ = ['ProtoTaskHandler']


class ProtoTaskHandler(RequestHandler):
  """Provides helper methods for serializing Request objects into protorpc
  message objects.

    :member message_type: Class type of a protorpc message.
  """

  message_type = None

  def parse_request_to_message(self):
    try:
      return message_from_json_str(
        self.message_type, self.request.get('_message') or '{}')
    except Exception, e:
      raise InvalidTaskError, e.message

  @toplevel # this decorator is for async calls with the ndb library..
  def post(self, task=None, *args, **kwds):
    self.run(
      task=task, message=self.parse_request_to_message())
    self.success()

  def run(self, task, message):
    raise NotImplementedError(
      'MessageHandler subclass must implement method "run".')

  def success(self):
    self.response.set_status(200, self.response.http_status_message(200))


class ProtoHandler(RequestHandler):
  """
      :member message_type: Class type of a protorpc message.
  """
  message_type = None

  def parse_message_from_body(self):
    return message_from_json_str(self.message_type, self.request.body)
