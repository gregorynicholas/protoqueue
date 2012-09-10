from protorpc import messages


class TaskMessage(messages.Message):
  kind = messages.StringField(1)
  start = messages.FloatField(2, default=0.0)
  end = messages.FloatField(3, default=0.0)
