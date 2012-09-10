from google.appengine.api import taskqueue
from .proto import message_to_json_str


def add(message, **kwargs):
  """Enqueues a task in the Taskqueue API with a decoded TaskMessage
  protorpc parameter.

    :param message: An instance of a protorpc message.
  """
  if 'params' in kwargs:
    raise ValueError('Parameters should be passed as attributes of the message.')

  return taskqueue.add(
    params={'_message': message_to_json_str(message)}, **kwargs)
