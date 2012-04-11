from django.db import models
from django.utils.text import compress_string
from django.db.models.signals import post_init

def uncompress_string(s):
    '''helper function to reverse django.utils.text.compress_string'''
    import cStringIO, gzip
    try:
        zbuf = cStringIO.StringIO(s)
        zfile = gzip.GzipFile(fileobj=zbuf)
        ret = zfile.read()
        zfile.close()
    except:
        ret = s
    return ret


class CompressedTextField(models.TextField):
    '''transparently compress data before hitting the db and uncompress after fetching'''

    def get_db_prep_save(self, value, connection):
        if value is not None:
            value = compress_string(value.encode("utf-8"))
        return models.TextField.get_db_prep_save(self, value, connection=connection)

    def _get_val_from_obj(self, obj):
        if obj:
            return uncompress_string(getattr(obj, self.attname))
        else:
            return self.get_default()

    def post_init(self, instance=None, **kwargs):
        value = self._get_val_from_obj(instance)
        if value:
            setattr(instance, self.attname, value)

    def contribute_to_class(self, cls, name):
        super(CompressedTextField, self).contribute_to_class(cls, name)
        post_init.connect(self.post_init, sender=cls)

    def get_internal_type(self):
        return "TextField"

    def db_type(self, connection):
        from django.conf import settings
        db_types = {'django.db.backends.mysql':'longblob', 'django.db.backends.sqlite3':'blob'}
        try:
            return db_types[settings.DATABASES['default']['ENGINE']]
        except KeyError:
            raise Exception, '%s currently works only with: %s'%(self.__class__.__name__,','.join(db_types.keys()))