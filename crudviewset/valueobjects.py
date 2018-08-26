class ViewParams:
    def __init__(self, role, superclasses=None, variables=None,
                 route=None, route_name=None, use_sample_template=False):
        self.role = role
        self.superclasses = superclasses
        self.variables = variables
        self.route = route
        self.route_name = route_name
        self.use_sample_template = use_sample_template
