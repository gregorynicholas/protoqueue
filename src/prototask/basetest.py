import logging
import unittest2 as unittest

from webapp2 import Request
from webapp2 import _local
from google.appengine.ext import testbed

import json
import proto


class BaseTestCase(unittest.TestCase):
  '''Base class for prototask unit tests.'''
  wsgiapp = None
  testbed = None

  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    self.testbed.init_taskqueue_stub()

    # hack to set the direct location of the queue.yaml:
    # https://groups.google.com/forum/?fromgroups=#!msg/google-appengine/VoVrMQZrNEg/KbIIAkq29rkJ
    # stub = self.testbed.get_stub('taskqueue')
    # stub._root_path = (app_config.ROOT_DIRECTORY)

    self.testbed.init_mail_stub()
    self.testbed.init_blobstore_stub()
    self.testbed.init_xmpp_stub()
    self.testbed.init_urlfetch_stub()
    self.testbed.init_images_stub()
    self.testbed.init_user_stub()
    self.setup_name = 'test'
    self.setup_name_int = 'int_model'
    self.testbed.setup_env(app_id='prototask-example')

  def tearDown(self):
    '''This restores the original stubs so that tests do not
    interfere with each other.'''
    if self.testbed:
      self.testbed.deactivate()
      self.clear_globals()

  # Method could be a function
  # pylint: disable-msg=R0201
  def clear_globals(self):
    '''Clear thread-local variables.'''
    _local.__release_local__()

  def post(self, url, post=None, headers=None, ajax=False):
    if not headers:
      headers = {}
    request = Request.blank(url, POST=post)
    if post:
      request.method = 'POST'
    if ajax:
      request.headers['Content-Type'] = 'application/json'
    if headers:
      request.headers.update(headers)
    return request.get_response(self.wsgiapp)

  def json(self, content):
    try:
      return json.loads(content)
    except Exception, e:
      logging.error('Exception encoding json object: %s', e)
      self.fail('Exception encoding json: %s' % content)

  def assertSuccessfulResponse(self, response):
    if response.status_int > 299:
      logging.error(response)
    self.assertEqual(response.status_int, 200)

  def encode_message_to_json(self, value):
    return proto.encode_message(value)

  def decode_json_to_message(self, message_type, value):
    return proto.decode_message(message_type, value)

  def message_from_json_str(self, message_type, value):
    return proto.decode_message(message_type, value)

  def message_to_json_str(self, message):
    return json.dumps(self.encode_message_to_json(message))

  def rpc_post(self, url, post, message_type):
    response = self.post(url, post)
    self.assertSuccessfulResponse(response)
    return self.message_from_json_str(message_type, response.body)
