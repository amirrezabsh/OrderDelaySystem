import redis
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class RedisQueue(metaclass=Singleton):
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def enqueue(self, queue_name, item):
        self.redis_client.lpush(queue_name, item)

    def dequeue(self, queue_name):
        item = self.redis_client.rpop(queue_name)
        return item.decode('utf-8') if item else None

    def count(self, queue_name):
        return self.redis_client.llen(queue_name)
