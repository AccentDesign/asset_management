from threading import local


_user = local()
_team = local()


class CurrentUserMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = getattr(request, 'user', None)
        return self.get_response(request)


def get_current_user():
    if hasattr(_user, 'value'):
        return _user.value
    return None


def get_current_team():
    if hasattr(_team, 'value'):
        return _team.value
    return None


def set_current_team(team):
    _team.value = team
