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
        return {'some': 'value'}

    config.commit()

    c = Client(app())
    r = c.get('/')
    assert r.json == {'some': 'value'}


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
        return {'some': 'value'}

    @app.ld_id(model=Foo)
    def foo_id(self, request):
        return request.link(self)

    config.commit()

    c = Client(app())
    r = c.get('/foos/10')
    assert r.json == {
        'some': 'value',
        '@id': 'http://localhost/foos/10'
    }


def test_type():
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
        return {'some': 'value'}

    @app.ld_type(model=Foo)
    def foo_type(self, request):
        return 'FooType'

    config.commit()

    c = Client(app())
    r = c.get('/')

    assert r.json == {
        'some': 'value',
        '@type': 'FooType'
    }


def test_context():
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
        return {'some': 'value'}

    @app.ld_context(model=Foo)
    def foo_context(self, request):
        return {'term': 'definition'}

    config.commit()

    c = Client(app())
    r = c.get('/')

    assert r.json == {
        'some': 'value',
        '@context': {'term': 'definition'},
    }


def test_id_type_and_context():
    config = morepath.setup()
    config.scan(more.jsonld)

    class app(JsonldApp):
        testing_config = config

    class Foo(object):
        def __init__(self, id):
            self.id = id

    @app.path(path='/foos/10', model=Foo)
    def get_foo(id):
        return Foo(id)

    @app.jsonld(model=Foo)
    def foo_default(self, request):
        return {'some': 'value'}

    @app.ld_id(model=Foo)
    def foo_id(self, request):
        return request.link(self)

    @app.ld_type(model=Foo)
    def foo_type(self, request):
        return 'FooType'

    @app.ld_context(model=Foo)
    def foo_context(self, request):
        return {'term': 'definition'}

    config.commit()

    c = Client(app())
    r = c.get('/foos/10')

    assert r.json == {
        'some': 'value',
        '@id': 'http://localhost/foos/10',
        '@type': 'FooType',
        '@context': {'term': 'definition'},
    }


def test_explicit_overrides():
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
        return {'some': 'value',
                '@id': self.id}

    @app.ld_id(model=Foo)
    def foo_id(self, request):
        assert False, "Should not be called"

    config.commit()

    c = Client(app())
    r = c.get('/foos/10')
    assert r.json == {
        'some': 'value',
        '@id': '10'
    }
