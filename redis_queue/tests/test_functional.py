import unittest
from redis import Redis
from redis_queue import Queue, ExclusiveQueue

class TestRedisQueue(unittest.TestCase):
    def setUp(self):
        self.redis_args = dict(host='127.0.0.1', port=6379)
        self.key = 'test_redis_queue'
        self.queue = Queue(self.key, **self.redis_args)
    
    def tearDown(self):
        redis = Redis(**self.redis_args)
        redis.delete(self.key)
    
    def test_right(self):
        self.queue.append('one')
        self.queue.append('two')
        self.queue.append('three')
        self.assertEqual(self.queue.pop(), 'three')
        self.assertEqual(self.queue.pop(), 'two')
        self.assertEqual(self.queue.pop(), 'one')
        self.assertRaises(IndexError, self.queue.pop)
    
    def test_left(self):
        self.queue.appendleft('one')
        self.queue.appendleft('two')
        self.queue.appendleft('three')
        self.assertEqual(self.queue.popleft(), 'three')
        self.assertEqual(self.queue.popleft(), 'two')
        self.assertEqual(self.queue.popleft(), 'one')
        self.assertRaises(IndexError, self.queue.pop)
    
    def test_right_left(self):
        self.queue.append('one')
        self.queue.append('two')
        self.queue.append('three')
        self.assertEqual(self.queue.popleft(), 'one')
        self.assertEqual(self.queue.popleft(), 'two')
        self.assertEqual(self.queue.popleft(), 'three')
        self.assertRaises(IndexError, self.queue.pop)
    
    def test_left_right(self):
        self.queue.appendleft('one')
        self.queue.appendleft('two')
        self.queue.appendleft('three')
        self.assertEqual(self.queue.pop(), 'one')
        self.assertEqual(self.queue.pop(), 'two')
        self.assertEqual(self.queue.pop(), 'three')
        self.assertRaises(IndexError, self.queue.pop)

    def test_clear(self):
        self.queue.appendleft('one')
        self.queue.appendleft('two')
        self.queue.appendleft('three')
        self.queue.clear()
        self.assertRaises(IndexError, self.queue.pop)
        self.assertRaises(IndexError, self.queue.popleft)
    
    def test_remove(self):
        self.queue.append('one')
        self.queue.append('two')
        self.queue.append('two')
        self.queue.append('three')
        self.queue.append('two')
        self.queue.remove('two')
        self.assertEqual(self.queue.pop(), 'three')
        self.assertEqual(self.queue.pop(), 'one')
        self.assertRaises(IndexError, self.queue.pop)
    
    def test_contains(self):
        self.queue.append('one')
        self.queue.append('two')
        self.queue.append('three')
        self.assert_('one' in self.queue)
        self.assert_('two' in self.queue)
        self.assert_('three' in self.queue)
        self.assert_('four' not in self.queue)
    
    def test_extend_right(self):
        self.queue.extend(['one', 'two', 'three'])
        self.assertEqual(self.queue.pop(), 'three')
        self.assertEqual(self.queue.pop(), 'two')
        self.assertEqual(self.queue.pop(), 'one')
        self.assertRaises(IndexError, self.queue.pop)
    
    def test_extend_left(self):
        self.queue.extendleft(['one', 'two', 'three'])
        self.assertEqual(self.queue.popleft(), 'three')
        self.assertEqual(self.queue.popleft(), 'two')
        self.assertEqual(self.queue.popleft(), 'one')
        self.assertRaises(IndexError, self.queue.pop)
    
    def test_iteration(self):
        self.queue.append('one')
        self.queue.append('two')
        self.queue.append('three')
        self.assertEqual(list(iter(self.queue)), ['one', 'two', 'three'])
    
    def test_length(self):
        self.queue.append('one')
        self.queue.append('two')
        self.queue.append('three')
        self.assertEqual(len(self.queue), 3)

class TestRedisExclusiveQueue(unittest.TestCase):
    def setUp(self):
        self.redis_args = dict(host='127.0.0.1', port=6379)
        self.key = 'test_redis_queue'
        self.queue = ExclusiveQueue(key=self.key, **self.redis_args)
    
    def tearDown(self):
        redis = Redis(**self.redis_args)
        redis.delete(self.key)
    
    def test_right(self):
        self.queue.append('two')
        self.queue.append('two')
        self.queue.append('two')
        self.queue.append('one')
        self.queue.append('two')
        self.queue.append('three')
        self.assertEqual(self.queue.pop(), 'three')
        self.assertEqual(self.queue.pop(), 'two')
        self.assertEqual(self.queue.pop(), 'one')
        self.assertRaises(IndexError, self.queue.pop)
    
    def test_left(self):
        self.queue.appendleft('two')
        self.queue.appendleft('two')
        self.queue.appendleft('two')
        self.queue.appendleft('one')
        self.queue.appendleft('two')
        self.queue.appendleft('three')
        self.assertEqual(self.queue.popleft(), 'three')
        self.assertEqual(self.queue.popleft(), 'two')
        self.assertEqual(self.queue.popleft(), 'one')
        self.assertRaises(IndexError, self.queue.pop)
    
    def test_right_left(self):
        self.queue.append('one')
        self.queue.append('two')
        self.queue.append('three')
        self.queue.append('two')
        self.queue.append('two')
        self.queue.append('two')
        self.assertEqual(self.queue.popleft(), 'one')
        self.assertEqual(self.queue.popleft(), 'two')
        self.assertEqual(self.queue.popleft(), 'three')
        self.assertRaises(IndexError, self.queue.pop)
    
    def test_left_right(self):
        self.queue.appendleft('one')
        self.queue.appendleft('two')
        self.queue.appendleft('three')
        self.queue.appendleft('two')
        self.queue.appendleft('two')
        self.queue.appendleft('two')
        self.assertEqual(self.queue.pop(), 'one')
        self.assertEqual(self.queue.pop(), 'two')
        self.assertEqual(self.queue.pop(), 'three')
        self.assertRaises(IndexError, self.queue.pop)
