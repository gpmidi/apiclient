import json


class JSONSerializer(object):
    """
    Simple wrapper around json
    """
    def dumps(self, obj):
        return json.dumps(obj, separators=(',', ':'))

    def loads(self, data):
        return json.loads(data)


class TextSerializer(object):
    """
    Dummy wrapper for text
    """
    def dumps(self, obj):
        return obj

    def loads(self, data):
        return data


def get_serializer(content_type):
    """
    Returns the appropriate serializer for the Content-Type
    """
    wrappers = {
        'application/json': JSONSerializer,
        'text/javascript': JSONSerializer,
        'text/plain': TextSerializer,
    }
    if content_type is not None:
        for mime, wrapper in wrappers.iteritems():
            if mime in content_type.lower():
                return wrapper()

    # Fallback
    return TextSerializer()
