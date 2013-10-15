from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from south.modelsinspector import introspector
from emserver import settings
import uuid, re, hashlib, logging

# -------------------------------------------------------------------------
# Custom fields
# -------------------------------------------------------------------------

class UUIDField(models.Field):
    """
    UUIDField is for primary keys, since databases may need to support
    master-master replication, and/or may need to import records from
    other systems.
    """

    _re_uuid = re.compile("[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}", re.UNICODE)

    def __init__(self, *args, **kwargs):

        # We cannot set min_length or max_length on this field because
        # the Django Rest Framework will try to validate the length
        # without first converting the UUID to a string. This results
        # in the exception "TypeError: object of type 'UUID' has no len()".
        #
        # We have a custom validate function below that ensures not only
        # the length requirements for a UUID but also enforces a regex match.
        kwargs.pop('min_length', None)
        kwargs.pop('max_length', None)

        kwargs['blank'] = True
        models.Field.__init__(self, *args, **kwargs)

    def pre_save(self, model_instance, add):
        """
        UUID fields are used in primary and foreign key columns.
        This pre_save hook ensures that we assign a value to a UUID
        field before saving if 1) we are saving a new model and
        2) the UUID field is the model's primary key.
        """
        if add and self.primary_key:
            value = uuid.uuid4()
            setattr(model_instance, self.attname, value)
            return value
        else:
            value = getattr(model_instance, self.attname)
            return None if value == '' else value


    def db_type(self, connection):
        """
        Specify the data type to use when creating this field in the
        SQL table.
        """
        engine = connection.settings_dict['ENGINE']
        if (engine.endswith('postgresql_psycopg2') or
            engine.endswith('postgresql')):
            return 'uuid'
        else:
            return 'char(36)'

    @classmethod
    def looks_like_uuid(self, value):
        """
        Returns true if the value is or looks like a valid UUID.
        """
        return UUIDField._re_uuid.match(str(value)) != None

    def to_python(self, value):
        """
        When retrieving the value from the database, we'll get a
        binary UUID from Postgres and a string from MySQL and Sqlite.
        Make sure that the python value is a UUID.
        """
        if not value:
            return None
        elif isinstance(value, uuid.UUID):
            return value
        else:
            try:
                value_as_uuid = uuid.UUID(value)
            except ValueError, ve:
                # Django Rest Framework does not handle ValueError
                # when deserializing JSON. It only handles ValidationError.
                # So we have to translate the exception here.
                raise ValidationError(
                    "{0} is not a valid UUID".format(self.name))
            return value_as_uuid

    def get_db_prep_value(self, value, connection, prepared = False):
        """
        Returns the UUID as a unicode string, so the ORM can construct
        a SQL statement. Django ORM wants UUIDs as unicode strings when
        it builds SQL! Don't pass it an actual UUID, or it will blow up.
        """
        return self.get_prep_value(value)

    def get_prep_value(self, value):
        """
        Returns the UUID as a unicode string, so the ORM can construct
        a SQL statement. Django ORM wants UUIDs as unicode strings when
        it builds SQL! Don't pass it an actual UUID, or it will blow up.
        """
        if not value:
            return None
        elif isinstance(value, uuid.UUID):
            return unicode(value)
        else:
            return value

    def validate(self, value, model_instance):
        """
        This ensures that any non-blank value looks like a valid UUID.
        """
        if not self.blank and not UUIDField.looks_like_uuid(value):
            raise exceptions.ValidationError(
                format("{0} is not a valid UUID", self.name))

    def south_field_triple(self):
        """
        Returns information about this field type so that South understands
        how to deal work with it in migrations.
        """
        field_class = "emserver.em.customfields.UUIDField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)
