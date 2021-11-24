import json
from django.http import JsonResponse


def in_group(user, groups):
    from .permissions import Admin, Developer, Project_Manager, Client
    if not isinstance(groups, (list, tuple)):
        groups = [groups]
    gm = {
        "admin": Admin,
        "dev": Developer,
        "pm": Project_Manager,
        "client": Client,
    }

    if "admin" in groups and user.is_superuser:
        return True

    groups = [gm[g] for g in groups]

    return any([grp in groups for grp in user.groups.all()])


def json_view(decode_request=True, encode_response=True):
    def decorator(view):
        """
        'view' is the Django view being decorated
        """

        def inner(request, *args, **kwargs):
            if decode_request and request.method not in {'HEAD', 'GET'}:
                try:
                    payload = json.loads(request.body)
                    request.json = payload
                except ValueError as e:
                    return JsonResponse({'error': 'Request body is not valid JSON'}, status=400)

            if not encode_response:
                return view(request, *args, **kwargs)

            response = None
            try:
                response = view(request, *args, **kwargs)
                assert isinstance(response, dict)
                status = 200
                if 'result' not in response:
                    response['result'] = 'ok'
            except Exception as e:
                status = 400
                if hasattr(e, 'message'):
                    msg = e.message
                else:
                    msg = 'Internal error: ' + str(e)
                response = {'result': 'error', 'text': msg}

            return JsonResponse(response, status=status, safe=False)

        return inner
    return decorator
