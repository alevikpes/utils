
# django help


### Permissions in Django Rest Framework

Example of using permissions in Django Rest Framework views
```python
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView


class IsAuthenticatedAndConfirmed(BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise  # UserNotAuthenticated exception

        if not request.user.email_confirmed:
            raise  # EmailNotConfirmed exception

        return True


class SomeView(APIView):

    permission_classes = (IsAuthenticatedAndConfirmed,)
```
