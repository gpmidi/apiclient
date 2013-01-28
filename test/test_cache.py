import unittest

from apiclient.cache import MemcachdCacher

class Test_MemcachdCacher(unittest.TestCase):
    SERVERS = [
           "127.0.0.1:11211",
           ]
    TEST_VALUES = {
                   'abc':'bogus12345',
                   'efg':'92845092834',
                   ('a', 'b', 3,):'two',
                   }
    
    def setUp(self):
        from ConfigParser import SafeConfigParser
        import os, os.path, sys
        servers = self.SERVERS
        if os.access('test_cache.ini', os.R_OK):
            self.cfg = SafeConfigParser()
            self.cfg.read(['test_cache.ini', ])
            servers = self.cfg.get('memcached', 'servers').split(',')
        self.cache = MemcachdCacher(
                                    servers = servers,
                                    )
    
    def test_basicGetSet(self):
        for keys, val in self.TEST_VALUES.items():
            self.cache.set(
                           keys = keys,
                           value = val,
                           )
            got = self.cache.get(keys = keys)
            self.assertEqual(
                             val,
                             got,
                             "Expected %r:%r to match %r" % (keys, val, got)
                             )
    
    def test_getNone(self):
        key = "we shouldn't have this"
        got = self.cache.get(keys = key)
        self.assertTrue(got is None, "Should have gotten None, not %r for %r" % (got, key))
        


