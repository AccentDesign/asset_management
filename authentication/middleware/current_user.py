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


def get_current_team():
    user = get_current_user()
    if user and user.is_authenticated:
        return user.activated_team
    return None


def set_current_team(request, team_id):
    request.user.activated_team = None
    if request.user and team_id:
        team_qs = request.user.get_teams().filter(pk=team_id)
        if team_qs.exists():
            request.user.activated_team = team_qs.get()

    request.user.save()
