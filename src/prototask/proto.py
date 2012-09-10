from json import dumps
from protorpc.protojson import encode_message, decode_message
from protorpc.messages import MessageField


__all__ = [
  'encode_message_to_json',
  'decode_json_to_message',
  'message_to_json_str',
  'message_from_json_str',
  'create']


def encode_message_to_json(value):
  return encode_message(value)

# goal is really just to create a readable version of the function..
# i could also just do an import .. as ..
def decode_json_to_message(message_type, value):
  return decode_message(message_type, dumps(value))


def message_to_json_str(message):
  return dumps(encode_message_to_json(message))

def message_from_json_str(message_type, value):
  return decode_message(message_type, value)


def create(message_type):
  """Creates an instance of the Message class and recursively creates an
  instance value for each MessageField property. This takes away from some
  pain of tedious property instantiation when creating Message objects."""
  result = message_type()
  _init_messagefields(result)
  return result

def _init_messagefields(node):
  for field in sorted(node.all_fields(), key=lambda f: f.number):
    if isinstance(field, MessageField):
      # create an instance of the type..
      _node = field.type()
      setattr(node, field.name, _node)
      _init_messagefields(_node)
