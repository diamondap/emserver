import sys
import django.test.utils
from os.path import realpath, abspath, join, normpath, dirname
from django.test.client import Client

test_dir = dirname(realpath(__file__))
code_dir = abspath(normpath(join(test_dir, '..')))
fixture_dir = abspath(join(code_dir, 'fixtures'))
sys.path.append(code_dir)

SU_LOGIN = 'admin'
SU_PASSWORD = 'admin'

TEST_ENV_INITIALIZED = False
DB_FIXTURES = ["initial_data.json"]

# The one router in our fixture data
ROUTER_ID = 1

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
    # We have to call this when using the test client,
    # otherwise, no data goes into the client's response.context
    global TEST_ENV_INITIALIZED
    if TEST_ENV_INITIALIZED == False:
        django.test.utils.setup_test_environment()
        TEST_ENV_INITIALIZED = True
    client = Client()
    #client.post('/login/', credentials_for(login))
    return client

def admin_client():
    # TODO: Return a client logged in as admin
    return get_client(SU_LOGIN, SU_PASSWORD)
