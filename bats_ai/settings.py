from __future__ import annotations

import os
from pathlib import Path

from composed_configuration import (
    ComposedConfiguration,
    ConfigMixin,
    DevelopmentBaseConfiguration,
    HerokuProductionBaseConfiguration,
    ProductionBaseConfiguration,
    TestingBaseConfiguration,
)
from configurations import values


class BatsAiMixin(ConfigMixin):
    SCHEMA_TO_INSPECT = 'nabatmonitoring'
    WSGI_APPLICATION = 'bats_ai.wsgi.application'
    ROOT_URLCONF = 'bats_ai.urls'

    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

    @staticmethod
    def mutate_configuration(configuration: ComposedConfiguration) -> None:
        # Install local apps first, to ensure any overridden resources are found first
        configuration.INSTALLED_APPS = [
            'bats_ai.core.apps.CoreConfig',
        ] + configuration.INSTALLED_APPS

        # Install additional apps
        configuration.INSTALLED_APPS += [
            's3_file_field',
            'django.contrib.gis',
        ]

        configuration.MIDDLEWARE = [
            'allauth.account.middleware.AccountMiddleware',
        ] + configuration.MIDDLEWARE

    @property
    def DATABASE_ROUTERS(self): # noqa
        if 'DJANGO_BATS_AI_DATABASE_URI' in os.environ:
            return ['bats_ai.router.BatsDBRouter']
        else:
            return []

    @property
    def DATABASES(self): # noqa
        db_val = values.DatabaseURLValue(
            alias='default',
            environ_prefix='DJANGO',
            environ_name='DATABASE_URL',
            environ_required=True,
            # Additional kwargs to DatabaseURLValue are passed to dj-database-url
            engine='django.db.backends.postgresql',
            conn_max_age=600,
        )
        db_dict = db_val.value
        if 'DJANGO_BATS_AI_DATABASE_URI' in os.environ:
            bats_val = values.DatabaseURLValue(
                alias='batsdb',
                environ_prefix='DJANGO',
                environ_name='BATS_AI_DATABASE_URI',
                environ_required=True,
                # Additional kwargs to DatabaseURLValue are passed to dj-database-url
                engine='django.contrib.gis.db.backends.postgis',
            )
            bats_dict = bats_val.value
            bats_dict['OPTIONS'] = {'options': '-c search_path=nabat,nabatmonitoring,public'}
            db_dict.update(bats_dict)
        return db_dict


class DevelopmentConfiguration(BatsAiMixin, DevelopmentBaseConfiguration):
    pass


class TestingConfiguration(BatsAiMixin, TestingBaseConfiguration):
    pass


class ProductionConfiguration(BatsAiMixin, ProductionBaseConfiguration):
    pass


class HerokuProductionConfiguration(BatsAiMixin, HerokuProductionBaseConfiguration):
    pass
