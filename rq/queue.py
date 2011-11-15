from pickle import loads
from .proxy import conn

def to_queue_key(queue_name):
    return 'rq:%s' % (queue_name,)


class Queue(object):
    def __init__(self, friendly_name):
        if not friendly_name:
            raise ValueError("Please specify a valid queue name (Got '%s')." % friendly_name)
        self.name = friendly_name
        self._key = to_queue_key(friendly_name)

    @property
    def key(self):
        return self._key

    @property
    def empty(self):
        return self.count == 0

    @property
    def messages(self):
        return conn.lrange(self.key, 0, -1)

    @property
    def count(self):
        return conn.llen(self.key)

    def enqueue(self, job):
        return job.enqueue(self)

    def dequeue(self):
        s = conn.lpop(self.key)
        return loads(s)

    def __str__(self):
        return self.name
