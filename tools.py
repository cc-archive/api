
import coverage
import nose

# list all the modules we care about, for reporting later
module_names = ('api_exceptions', 'rest_api', 'simplechooser', 
                'supportapi', 'support')

def analyze_coverage():
    '''Replacement for './bin/nosetests --with-coverage', since that
       call is broken for some reason.'''

    # clear out coverage results first
    coverage.erase()

    # begin collecting coverage data
    coverage.start()

    # start the nose test suite running
    nose.run() # ignore whether it passed or failed

    # stop collecting coverage data
    coverage.stop()

    # import modules, so we can report on them
    modules = [__import__(n) for n in module_names]

    # print coverage report
    coverage.report(modules)

if __name__ == '__main__':
    analyze_coverage()
