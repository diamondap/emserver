import sys
from os.path import realpath, abspath, join, normpath, dirname
from django.test.client import Client

test_dir = dirname(realpath(__file__))
code_dir = abspath(normpath(join(test_dir, '..')))
fixture_dir = abspath(join(test_dir, 'fixtures'))
sys.path.append(code_dir)

SU_LOGIN = 'admin'
SU_PASSWORD = 'admin'

# These are the database fixtures.
#DB_FIXTURES = ["{0}/initial_data.json".format(fixture_dir)]
DB_FIXTURES = ["initial_data.json"]

def load_fixture(filename):
    """
    Returns the entire contents of a fixture file. The filename must be
    relative to the fixture directory.
    """
    full_path = join(fixture_dir, filename)
    with open(full_path, 'r') as f:
        return f.read()

def get_client(username, password):
    """
    Returns a client already logged in with the specified login.
    Login should be one of the email address constants defined above.
    """
    client = Client()
    #client.post('/login/', credentials_for(login))
    return client

def admin_client():
    return get_client(SU_LOGIN, SU_PASSWORD)
