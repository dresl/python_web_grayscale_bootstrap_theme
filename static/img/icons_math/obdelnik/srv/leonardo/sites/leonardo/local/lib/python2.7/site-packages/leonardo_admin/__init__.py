
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


default_app_config = 'leonardo_admin.Config'


class Default(object):

    optgroup = 'Admin'

    # don't decorate admin urls
    public = True

    @property
    def apps(self):
        apps = [
            'django.contrib.admin',
            'django.contrib.admindocs',
            'leonardo_admin',
        ]
        return apps

    plugins = [
        ('leonardo_admin.apps.admin', _('Admin Site')),
    ]


class Config(AppConfig, Default):
    name = 'leonardo_admin'
    verbose_name = _("Admin")

default = Default()
