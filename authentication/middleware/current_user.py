from django.utils.functional import SimpleLazyObject
from threading import local


_user = local()


class CurrentUserMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # sets the local user to use in code that lives outside the request
        _user.value = getattr(request, 'user', None)

        return self.get_response(request)


def get_current_user():
    if hasattr(_user, 'value'):
        return _user.value
    return None


def get_current_collection():
    user = get_current_user()
    if user and user.is_authenticated:
        return user.activated_collection
    return None


def set_current_collection(request, collection_id):
    request.user.activated_collection = None
    collection_qs = request.user.get_collections().filter(pk=collection_id)
    if collection_qs.exists():
        request.user.activated_collection = collection_qs.get()

    request.user.save()
