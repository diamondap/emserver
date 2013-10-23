# EM Server

The Evil Mommy server.

## Running Tests

Run this command in the top-level directory:

<code>
./test.sh
</code>

Or this:

<code>
DJANGO_SETTINGS_MODULE=emserver.settings nosetests --nocapture
</code>

## Dumping Data

<code>
python manage.py dumpdata --exclude auth.permission --exclude contenttypes --natural --indent 4 > em/tests/fixtures/initial_data.json
</code>