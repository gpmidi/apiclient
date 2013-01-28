''' Cache stuff using memcached
Created on Jan 27, 2013

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''

# FIXME: Add in support for a C-based lib
# Pure-python lib
import memcache

from .base import CacherBase
import hashlib


class MemcachdCacher(CacherBase):
    """ Cache stuff using memcached
    """
    # A hashlib function to use for serializing cache keys
    # Should be secure
    HASH_TYPE = hashlib.md5
    
    def __init__(self, servers):
        self.client = memcache.Client(servers = servers)
    
    def _set(self, key, value, time = 0):
        """ Cache value by key """
        return self.client.set(
                               key = key,
                               val = value,
                               time = time,
                               )
        
    def _get(self, key):
        """ Retrieve a cached by key """
        return self.client.get(key = key)
    
