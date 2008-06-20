
import os
import webtest

def test_one():
    assert True

def test_trivial():
    assert 2 + 2 == 4

def create_testserver():
    cfgstr = 'config:%s' % (os.path.join(os.getcwd(), '..', 'server.cfg'))
    app = webtest.TestApp(cfgstr)
    return app

if __name__ == '__main__':
    create_testserver()
