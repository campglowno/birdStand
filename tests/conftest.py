import pytest
from birdstandy.models import Bird, Place, BirdStand, Watcher, BirdPhoto
from django.test import Client
from django.contrib.auth.models import User, Permission
import credentials


@pytest.fixture
def client():
    client = Client()
    return client



@pytest.fixture
def bird():
    return Bird.objects.create(
        name='Test bird',
        scientific_name='test-bird'
    )


@pytest.fixture
def birds():
    return [
        Bird.objects.create(
            name=f'Bird {i}',
            scientific_name=f'bird-{i}'
        )
        for i in range(5)
    ]


@pytest.fixture
def place():
    return Place.objects.create(
        name='Test place',
        city='test-city',
        country='test-country'
    )


@pytest.fixture
def watcher():
    return Watcher.objects.create(
        first_name='Test name',
        last_name='test-name',
    )


@pytest.fixture
def watchers():
    return [
        Watcher.objects.create(
            first_name=f'Watcher {i}',
            last_name=f'watcher-{i}'
        )
        for i in range(5)
    ]



@pytest.fixture
def birdstands():
    return [
        BirdStand.objects.create(
            bird='1',
            place='1',
            watcher='1'
        )
    ]


@pytest.fixture
def superuser():
    return User.objects.create_superuser(
        username=credentials.SUPERUSER,
        email='superuser@email.com',
        password=credentials.SUPERUSER_PASS,
    )


@pytest.fixture
def common_user():
    return User.objects.create_user(
        username=credentials.USER,
        email='cmnuser@email.com',
        password=credentials.USER_PASS
    )


@pytest.fixture
def users():
    return [
        User.objects.create_user(
        username=f'user {i}',
        email=f'cmnuser{i}@email.com',
        password=f'pass{i}'
        )
        for i in range(5)
    ]


@pytest.fixture
def photo():
    return BirdPhoto.objects.create(
        image='static/drozd.jpg',
        name_id='1',
    )

