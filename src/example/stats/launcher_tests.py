from prototask.basetest import BaseTestCase


class ServiceTests(BaseTestCase):
  def setUp(self):
    from main import application
    self.wsgiapp = application
    BaseTestCase.setUp(self)


  def test_create(self):
    post = '''{
      "kind": "Stat_EntityKindCount",
      "start": 1347310102.0,
      "end": 1347310102.0
    }'''
    self.post('/stats', post, ajax=True)

    # assert that a task was added to the task queue
    stub = self.testbed.get_stub('taskqueue')
    tasks = stub.GetTasks('default')
    self.assertTrue(len(tasks), 1)
