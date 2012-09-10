from webapp2 import Route


def routes():
  return [
    Route(
      '/stats/_tasks/<task:([^/].+)>',
      handler='stats.stats.TaskDispatcher',
      name='stats_task_dispatcher'),
    Route(
      '/stats',
      handler='stats.launcher.TaskLauncher',
      name='stats_task_launcher'),
  ]


from webapp2 import WSGIApplication
application = WSGIApplication(
  routes(), config={}, debug=True)
