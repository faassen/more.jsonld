import morepath
from more.jsonld import JsonldApp
import more.jsonld
from webtest import TestApp as Client


def setup_module(module):
    morepath.disable_implicit()


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


def test_id():
    config = morepath.setup()
    config.scan(more.jsonld)

    class app(JsonldApp):
        testing_config = config

    class Foo(object):
        def __init__(self, id):
            self.id = id

    @app.path(path='/foos/{id}', model=Foo)
    def get_foo(id):
        return Foo(id)

    @app.jsonld(model=Foo)
    def foo_default(self, request):
        return {}

    @app.ld_id(model=Foo)
    def foo_id(self, request):
        return request.link(self)

    config.commit()

    c = Client(app())
    r = c.get('/foos/10')
    assert r.json == { '@id': '/foos/10' }
