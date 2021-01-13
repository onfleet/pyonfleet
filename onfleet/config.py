class Config(object):
  data = dict(
    URL = dict(
      base_url = "https://onfleet.com/api/",
      version = "v2/",
      auth_test = "auth/test/"
    ),
    RESOURCES = dict(
      administrators = dict(
        GET = dict(
          get = "/admins"
        ),
        POST = dict(
          create = "/admins"
        ),
        PUT = dict(
          update = "/admins/:adminId"
        ),
        DELETE = dict(
          deleteOne = "/admins/:adminId"
        )
      ),
      containers = dict(
        GET = dict(
          get = "/containers/:param/:containerId"
        ),
        PUT = dict(
          update = "/containers/:containerId"
        )
      ),
      destinations = dict(
        GET = dict(
          get = "/destinations/:destinationId"
        ),     
        POST = dict(
          create = "/destinations"
        )
      ),
      hubs = dict(
        GET = dict(
          get = "/hubs"
        ) 
      ),
      organization = dict(
        GET = dict(
          get = ["/organization", "/organizations/:orgId"]
        ),
        PUT = dict(
          insertTask = "/containers/organization/:orgId"
        )
      ),
      recipients = dict(
        GET = dict(
          get = "/recipients/:recipientId"
        ),
        POST = dict(
          create = "/recipients"
        ),
        PUT = dict(
          update = "/recipients/:recipientId"
        )
      ),
      tasks = dict(
        GET = dict(
          get = ["/tasks/all", "/tasks/:taskId"]
        ),
        POST = dict(
          create = "/tasks",
          clone = "/tasks/:taskId/clone",
          forceComplete = "/tasks/:taskId/complete",
          batchCreate = "/tasks/batch",
          autoAssign = "/tasks/autoAssign"
        ),
        PUT = dict(
          update = "/tasks/:taskId"
        ),
        DELETE = dict(
          deleteOne = "/tasks/:taskId"
        )
      ),
      teams = dict(
        GET = dict(
          get = ["/teams", "/teams/:teamId"]
        ),
        POST = dict(
          create = "/teams"
        ),
        PUT = dict(
          update = "/teams/:teamId",
          insertTask = "/containers/teams/:teamId"
        ),
        DELETE = dict(
          deleteOne = "/teams/:teamId"
        )
      ),
      workers = dict(
        GET = dict(
          get = ["/workers", "/workers/:workerId"],
          getSchedule = "/workers/:workerId/schedule",
          getByLocation = "/workers/location"
        ),
        POST = dict(
          create = "/workers",
          setSchedule = "/workers/:workerId/schedule"
        ),
        PUT = dict(
          update = "/workers/:workerId",
          insertTask = "/containers/workers/:workerId"
        ),
        DELETE = dict(
          deleteOne = "/workers/:workerId"
        )
      ),
      webhooks = dict(
        GET = dict(
          get = "/webhooks"
        ),
        POST = dict(
          create = "/webhooks"
        ),
        DELETE = dict(
          deleteOne = "/webhooks/:webhookId"
        )
      )   
    )
  )