# Django CRUDViewSet

# Requirements

* Python 3.6.*
* Django 2.*

# Installation

Install using `pip` ...

```bash
pip install django-crudviewset
```

Add `'crudviewset'` to your `INSTALLED_APPS` setting.

```python
INSTALLED_APPS = (
    ...
    'crudviewset',
)
```

# Example

## Simple Example

`example/views.py`

```python
from crudviewset import CRUDViewSet

from example.models import Board

BoardCRUDViewSet = CRUDViewSet('board', Board)
```

`example/urls.py`

```python
from . import views

urlpatterns = []
urlpatterns.extend(views.BoardCRUDViewSet.get_urlpatterns())
```

## Custom Example

`example/views.py`

```python
from django.contrib.auth.mixins import UserPassesTestMixin

from crudviewset import CRUDViewSet, ViewParams, VIEWKIND

from example.models import Board
from example.forms import BoardForm


class BoardFormViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


BoardCRUDViewSet = CRUDViewSet(
    'board', Board, app_name='example',
    base_superclasses=[UserPassesTestMixin],
    base_variables={
        'test_func': lambda self: self.request.user.is_authenticated,
        'get_queryset': lambda self: Board.objects.filter(user=self.request.user).order_by('-created_at'),
    },
    list_vp=ViewParams(
        role=VIEWKIND.LIST,
        variables={
            'paginate_by': 10,
        }
    ),
    detail_vp=ViewParams(
        role=VIEWKIND.DETAIL,
        superclasses=[],
        variables={
            'get_queryset': lambda self: Board.objects.all().order_by('-created_at'),
        }
    ),
    create_vp=ViewParams(
        role=VIEWKIND.CREATE,
        superclasses=[UserPassesTestMixin, BoardFormViewMixin],
        variables={
            'form_class': BoardForm,
            'template_name': 'example/example_form.html',
        }
    ),
    update_vp=ViewParams(
        role=VIEWKIND.UPDATE,
        superclasses=[UserPassesTestMixin, BoardFormViewMixin],
        variables={
            'form_class': BoardForm,
            'template_name': 'example/example_form.html',
        }
    ),
    delete_vp=ViewParams(
        role=VIEWKIND.DELETE,
        variables={
            'success_url': reverse_lazy('main:example_list'),
        }
    ),
    vp_list=[
        ViewParams(
            role=VIEWKIND.LIST,
            route='latest/',
            route_name='latest',
            variables={
                'paginate_by': 10,
                'template_name': 'example/latest.html',
                'get_queryset': lambda self: Board.objects.all().order_by('-created_at'),
            }
        ),
    ]
)
```

`example/urls.py`

```python
from . import views

app_name = 'example'
urlpatterns = []
urlpatterns.extend(views.BoardCRUDViewSet.get_urlpatterns())
```

