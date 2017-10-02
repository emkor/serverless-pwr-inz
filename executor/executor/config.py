broker_url = 'pyamqp://rabbitmq:rabbitmq@rabbit1//'
result_backend = 'db+mysql://celery:celery@mysql1/results'
# redis_max_connections = 1
# redis_socket_connect_timeout = 5
# redis_socket_timeout = 5

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Warsaw'
enable_utc = True

worker_concurrency = 16  # maximum executor-processes -> 10 tasks at a time per worker
task_acks_late = True

broker_pool_limit = None

worker_prefetch_multiplier = 1
worker_max_tasks_per_child = 1
worker_max_memory_per_child = 128 * 1000  # 128 MB
worker_send_task_events = True
task_send_sent_event = True
task_track_started = True
task_soft_time_limit = 8  # exception within task is raised after: 10 seconds
task_time_limit = 15  # executor process is killed after: 20 seconds
