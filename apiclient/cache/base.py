''' Various caches that can be used with the API client
Created on Jan 27, 2013

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import hashlib

class CacherBase(object):
    """ Base class for caching stuff in a way that 
    APIClient can take advantage of. 
    """
    # A hashlib function to use for serializing cache keys
    HASH_TYPE = hashlib.md5
    # Default time limit for all cached data. 
    DEFAULT_MAX_TIME = None
    
    def varyBy(self, *keys):
        """ Hash the given keys for use as caching keys """
        if isinstance(keys, list):
            return self.HASH_TYPE(' - '.join(keys)).hexdigest()
        elif isinstance(keys, str):
            return self.HASH_TYPE(keys).hexdigest()
        else:
            return self.HASH_TYPE(str(keys)).hexdigest()

    def set(self, value, keys):
        """ Cache a value based on a hash of the str() of all *keys """
        if self.DEFAULT_MAX_TIME is not None:
            return self._set(
                             key = self.varyBy(keys),
                             value = value,
                             time = self.DEFAULT_MAX_TIME,
                             )
        return self._set(key = self.varyBy(*keys), value = value)
    
    def setLimited(self, value, keys, time = 0):
        """ Cache a value based on a hash of the str() of all *keys """
        if time is None and self.DEFAULT_MAX_TIME is not None:
            time = self.DEFAULT_MAX_TIME
        return self._set(key = self.varyBy(*keys), value = value, time = time)
    
    def get(self, keys, defaultValue = None):
        """ Retrieve a cached value. Returns None or defaultValue if not found. """
        ret = self._get(key = self.varyBy(*keys))
        if ret is None:
            return defaultValue
        return ret        

    def _set(self, key, value, time = None):
        """ Cache value by key """
        raise NotImplementedError("Can't set anything with %r" % type(self))
    
    def _get(self, key):
        """ Retrieve a cached by key """
        raise NotImplementedError("Can't get anything with %r" % type(self))
    
