import datetime as dt

import pytest
from django.utils import timezone


@pytest.fixture
def user_factory(db):
    from apps.users.models import TelegramUser

    counter = {"n": 0}

    def make(**kw):
        counter["n"] += 1
        kw.setdefault("tg_id", 100000 + counter["n"])
        kw.setdefault("first_name", f"User{counter['n']}")
        kw.setdefault("has_dm_started", True)
        return TelegramUser.objects.create(**kw)

    return make


@pytest.fixture
def circle_factory(db, user_factory):
    from apps.circles.models import Circle, RotationPolicy

    def make(**kw):
        kw.setdefault("title", "Sinfdoshlar")
        kw.setdefault("owner", user_factory())
        kw.setdefault("timezone", "Asia/Tashkent")
        kw.setdefault("chat_id", -1000000000000 - Circle.objects.count())
        circle = Circle.objects.create(**kw)
        RotationPolicy.objects.create(circle=circle)
        return circle

    return make


@pytest.fixture
def membership_factory(db, user_factory):
    from apps.circles.models import Membership

    def make(circle, **kw):
        kw.setdefault("user", user_factory())
        kw.setdefault("rotation_position", circle.memberships.count())
        return Membership.objects.create(circle=circle, **kw)

    return make


@pytest.fixture
def utc():
    return dt.UTC


@pytest.fixture
def now():
    return timezone.now()
