import morepath
from more.jsonld import JsonldApp
import more.jsonld
from webtest import TestApp as Client


def test_noop():
    config = morepath.setup()
    config.scan(more.jsonld)

    class app(JsonldApp):
        testing_config = config

    class Foo(object):
        pass

    @app.path(path='/', model=Foo)
    def get_foo():
        return Foo()

    @app.jsonld(model=Foo)
    def foo_default(self, request):
        return {}

    config.commit()

    c = Client(app())
    r = c.get('/')
    assert r.json == {}

