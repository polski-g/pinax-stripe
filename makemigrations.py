#!/usr/bin/env python
import os
import sys

import django

from django.conf import settings


DEFAULT_SETTINGS = dict(
    DEBUG=True,
    USE_TZ=True,
    TIME_ZONE='UTC',
    DATABASES={
        "default": {
            "ENGINE": os.environ.get("PINAX_STRIPE_DATABASE_ENGINE", "django.db.backends.postgresql_psycopg2"),
            "HOST": os.environ.get("PINAX_STRIPE_DATABASE_HOST", "127.0.0.1"),
            "PORT": os.environ.get("PINAX_STRIPE_DATABASE_PORT", "5432"),
            "NAME": os.environ.get("PINAX_STRIPE_DATABASE_NAME", "pinax_stripe"),
            "USER": os.environ.get("PINAX_STRIPE_DATABASE_USER", ""),
        }
    },
    MIDDLEWARE_CLASSES=[
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware"
    ],
    ROOT_URLCONF="pinax.stripe.urls",
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.sites",
        "pinax.stripe",
    ],
    SITE_ID=1,
    PINAX_STRIPE_PUBLIC_KEY="",
    PINAX_STRIPE_SECRET_KEY="",
    PINAX_STRIPE_SUBSCRIPTION_REQUIRED_EXCEPTION_URLS=["pinax_stripe_subscription_create"],
    PINAX_STRIPE_SUBSCRIPTION_REQUIRED_REDIRECT="pinax_stripe_subscription_create",
    PINAX_STRIPE_HOOKSET="pinax.stripe.tests.hooks.TestHookSet"
)


def run(*args):
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)

    django.setup()

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    django.core.management.call_command(
        "makemigrations",
        "pinax_stripe",
        *args
    )


if __name__ == "__main__":
    run(*sys.argv[1:])
