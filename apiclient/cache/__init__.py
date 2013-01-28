''' Various caches that can be used with the API client
Created on Jan 27, 2013

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''

try:
    from .memcached import MemcachdCacher
except ImportError, e:
    MemcachdCacher = None




