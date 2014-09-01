import morepath
from morepath.directive import JsonDirective


class JsonldApp(morepath.App):
    pass


@JsonldApp.directive('jsonld')
class JsonldDirective(JsonDirective):
    pass
