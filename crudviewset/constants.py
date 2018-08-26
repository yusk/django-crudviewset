class VIEWKIND:
    LIST = 'list'
    CREATE = 'create'
    DETAIL = 'detail'
    UPDATE = 'update'
    DELETE = 'delete'


DEFAULT_ROUTING_TABLE = {
    VIEWKIND.LIST: {
        'route': '{name}s/',
        'name': '{name}_list',
    },
    VIEWKIND.CREATE: {
        'route': '{name}s/create/',
        'name': '{name}_create',
    },
    VIEWKIND.DETAIL: {
        'route': '{name}s/<uuid:pk>/',
        'name': '{name}_detail',
    },
    VIEWKIND.UPDATE: {
        'route': '{name}s/<uuid:pk>/update/',
        'name': '{name}_update',
    },
    VIEWKIND.DELETE: {
        'route': '{name}s/<uuid:pk>/delete/',
        'name': '{name}_delete',
    }
}

DEFAULT_TEMPLATE_VIEWS = {
    VIEWKIND.LIST: 'crudviewset/list.html',
    VIEWKIND.CREATE: 'crudviewset/form.html',
    VIEWKIND.DETAIL: 'crudviewset/detail.html',
    VIEWKIND.UPDATE: 'crudviewset/form.html',
    VIEWKIND.DELETE: 'crudviewset/delete.html'
}
