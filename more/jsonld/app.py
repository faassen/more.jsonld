import morepath
from morepath.directive import JsonDirective
import reg


@reg.generic
def ld_id(request, self):
    return None


@reg.generic
def ld_type(request, self):
    return None


@reg.generic
def ld_context(request, self):
    return None


JSON_LD = {
    '@id': ld_id,
    '@type': ld_type,
    '@context': ld_context
}


class JsonldApp(morepath.App):
    pass


@JsonldApp.directive('jsonld')
class JsonldDirective(JsonDirective):
    def perform(self, registry, obj):
        def view(self, request):
            result = obj(self, request)
            for key, value in JSON_LD.items():
                if key not in result:
                    v = value(request, self, lookup=request.lookup)
                    if v is not None:
                        result[key] = v
            return result
        super(JsonldDirective, self).perform(registry, view)


class LdDirective(morepath.Directive):
    def __init__(self, app, model, generic_func):
        super(LdDirective, self).__init__(app)
        self.model = model
        self.generic_func = generic_func

    def identifier(self, app):
        return (self.model,)

    def perform(self, registry, obj):
        def f(request, model):
            return obj(model, request)
        registry.register(self.generic_func,
                          [morepath.Request, self.model], f)


@JsonldApp.directive('ld_id')
class LdIdDirective(LdDirective):
    def __init__(self, app, model):
        super(LdIdDirective, self).__init__(app, model, ld_id)


@JsonldApp.directive('ld_type')
class LdTypeDirective(LdDirective):
    def __init__(self, app, model):
        super(LdTypeDirective, self).__init__(app, model, ld_type)


@JsonldApp.directive('ld_context')
class LdContextDirective(LdDirective):
    def __init__(self, app, model):
        super(LdContextDirective, self).__init__(app, model, ld_context)
