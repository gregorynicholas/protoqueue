from prototask.handler import ProtoHandler
from prototask import queue
from taskmessages import TaskMessage


class TaskLauncher(ProtoHandler):
  """Request handler that queues a task to generate a count of entities."""
  message_type = TaskMessage

  def get(self, *args, **kwargs):
    """Queues a task via page request with get parameters."""
    if self.request.get('kind'):
      message = TaskMessage()
      message.kind = self.request.get('kind')
      message.start = float(self.request.get('start'))
      message.end = float(self.request.get('end'))
      queue.add(
        url='/stats/_tasks/count', message=message)

  def post(self, *args, **kwargs):
    """Queue up a task via a json post request."""
    message = self.parse_message_from_body()
    queue.add(
      url='/stats/_tasks/count', message=message)
