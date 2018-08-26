from django.urls import reverse_lazy
from copy import deepcopy

from django.urls import path
from django.views.generic import (
    ListView, DetailView, CreateView,
    UpdateView, DeleteView
)

from .constants import VIEWKIND, DEFAULT_ROUTING_TABLE, DEFAULT_TEMPLATE_VIEWS
from .utils import get_editable_field_names
from .valueobjects import ViewParams


class CRUDViewSet:
    def __set_view(self, vp):
        # 継承するための superclass を取得
        base_class = globals()[vp.role.capitalize() + 'View']
        if vp.superclasses is not None:
            superclasses = deepcopy(vp.superclasses)
        else:
            superclasses = deepcopy(self.base_superclasses)
        superclasses.append(base_class)

        # クラス変数、メソッドの取得
        variables = deepcopy(self.base_variables)
        if vp.variables is not None:
            variables.update(vp.variables)

        # ルーティング
        route = vp.route if vp.route is not None else DEFAULT_ROUTING_TABLE[vp.role]['route'].format(name=self.name)
        route_name = vp.route_name if vp.route_name is not None else DEFAULT_ROUTING_TABLE[vp.role]['name'].format(name=self.name)

        # デフォルトのモデルを指定
        if 'model' not in variables:
            variables['model'] = self.model

        # デフォルトのfieldsを指定
        if vp.role in [VIEWKIND.CREATE, VIEWKIND.UPDATE]:
            if 'form_class' not in variables and 'fields' not in variables:
                variables['fields'] = get_editable_field_names(variables['model'])

        # デフォルトのsuccess_urlを指定
        if vp.role in [VIEWKIND.CREATE, VIEWKIND.UPDATE, VIEWKIND.DELETE]:
            if 'success_url' not in variables and 'get_success_url' not in variables:
                list_route_name = DEFAULT_ROUTING_TABLE[VIEWKIND.LIST]['name'].format(name=self.name)
                if self.app_name is not None:
                    variables['success_url'] = reverse_lazy('%s:%s' % (self.app_name, list_route_name))
                else:
                    variables['success_url'] = reverse_lazy('%s' % list_route_name)

        # デフォルトのviewの利用
        if vp.use_sample_template:
            variables['template_name'] = DEFAULT_TEMPLATE_VIEWS[vp.role]

        # クラスを作成
        setattr(
            self,
            base_class.__name__,
            type(
                'CRUD%sView' % route_name.capitalize(),
                tuple(superclasses),
                variables
            )
        )
        self.urlpattern_dict[route_name] = path(
            route,
            getattr(self, base_class.__name__).as_view(),
            name=route_name
        )

    def __init__(self, name, model, app_name=None, base_superclasses=[],
                 base_variables={},
                 list_vp=ViewParams(role='list', use_sample_template=True),
                 detail_vp=ViewParams(role='detail', use_sample_template=True),
                 create_vp=ViewParams(role='create', use_sample_template=True),
                 update_vp=ViewParams(role='update', use_sample_template=True),
                 delete_vp=ViewParams(role='delete', use_sample_template=True),
                 vp_list=[]):
        self.name = name
        self.model = model
        self.app_name = app_name
        self.base_superclasses = base_superclasses
        self.base_variables = base_variables

        self.urlpattern_dict = {}

        for vp in [list_vp, detail_vp, create_vp, update_vp, delete_vp]:
            if vp is not None:
                self.__set_view(vp)

        for vp in vp_list:
            self.__set_view(vp)

    def get_urlpatterns(self):
        return self.urlpattern_dict.values()
