import morepath
from morepath.directive import JsonDirective
import reg


@reg.generic
def ld_id(request, self):
    return None


class JsonldApp(morepath.App):
    pass


@JsonldApp.directive('jsonld')
class JsonldDirective(JsonDirective):
    def perform(self, registry, obj):
        def view(self, request):
            result = obj(self, request)
            if '@id' not in result:
                id = ld_id(request, self, lookup=request.lookup)
                if id is not None:
                    result['@id'] = id
            return result
        super(JsonldDirective, self).perform(registry, view)


@JsonldApp.directive('ld_id')
class LdIdDirective(morepath.Directive):
    def __init__(self, app, model):
        super(LdIdDirective, self).__init__(app)
        self.model = model

    def identifier(self, app):
        return (self.model,)

    def perform(self, registry, obj):
        def f(request, model):
            return obj(model, request)
        registry.register(ld_id, [morepath.Request, self.model], f)

