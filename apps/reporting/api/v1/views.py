from 

from celery.result import AsyncResult
res = AsyncResult("your-task-id")
res.ready()