#

import redis

class Queue(object):
    """Implements the same interface as collections.dequeue"""
    def __init__(self, redis, queue_name):
        self._redis = redis
        self.queue_name = queue_name
    
    def append(self, x):
        self._redis.push(self.queue_name, x)
    
    def appendleft(self, x):
        self._redis.push(self.queue_name, x, head=True)
    
    def clear(self):
        self._redis.delete(self.queue_name)
    
    def extend(self, iterable):
        """Non-atomic. append each of the items from iterable in turn."""
        for item in iterable:
            self.append(item)
    
    def extendleft(self, iterable):
        """Non-atomic. appendleft each of the items from iterable in turn."""
        for item in iterable:
            self.appendleft(item)
    
    def pop(self):
        item = self._redis.pop(self.queue_name, tail=True)
        if item is None:
            raise IndexError
        return item
    
    def popleft(self):
        item = self._redis.pop(self.queue_name)
        if item is None:
            raise IndexError
        return item
    
    def remove(self, value):
        num_removed = self._redis.lrem(self.queue_name, value)
        if num_removed == 0:
            raise ValueError()
    
    def rotate(self):
        """rotates the queue one step only."""
        self_redis.poppush(self.queue_name, self.queue_name)
        
    # Membership
    def __contains__(self, item):
        # This could stand to be a lot more efficient.
        # Why doesn't redis support this on the server side?
        members = self._redis.lrange(self.queue_name, 0, -1)
        return item in members
    
    # Length
    def __len__(self):
        return self._redis.llen(self.queue_name)
    
    # Subscript
    def __getitem__(self, key):
        item = self._redis.lindex(self.queue_name, key)
        if item is None:
            raise IndexError
        return item
    
    def __setitem__(self, key, value):
        try:
            self._redis.lset(self.queue_name, key, value)
        except redis.ResponseError, e:
            raise IndexError(e)
    
    # Iteration
    def __iter__(self):
        members = self._redis.lrange(self.queue_name, 0, -1)
        return iter(members)

class ExclusiveQueue(Queue):
    """A queue that implements exclusivity (a given thing can only be in the
    queue once. This is not at all atomic; it pops something off then removes
    all other instances from the queue."""
    
    def pop(self):
        item = super(ExclusiveQueue, self).pop()
        try:
            self.remove(item)
        except ValueError:
            pass
        return item
    
    def popleft(self):
        item = super(ExclusiveQueue, self).popleft()
        try:
            self.remove(item)
        except ValueError:
            pass
        return item
