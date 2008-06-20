
import os
import webtest

def setup():
    """Test fixture for nosetests: sets up the WSGI app server
    """
    global app
    cfgstr = 'config:%s' % (os.path.join(os.getcwd(), '..', 'server.cfg'))
    app = webtest.TestApp(cfgstr)

def test_trivial():
    assert True

def test_addition():
    assert 2 + 2 == 4

def test_get():
    res = app.get('/')

if __name__ == '__main__':
    pass
