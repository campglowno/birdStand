import pytest
from django.urls import reverse
from birdstandy.models import Bird, Watcher, Place, BirdStand, BirdPhoto
from django.contrib.auth.models import User, Permission
#pawel-lis-cl - github Pawła Lisa


@pytest.mark.django_db
def test_bird(client, birds):
    response = client.get('/birds_list/')
    assert response.status_code == 200
    assert list(response.context['birds']) == birds


@pytest.mark.django_db
def test_add_bird(client):
    response = client.post(
        reverse('add_bird'),
        {
            'name': 'Test bird2',
            'scientific_name': 'test-bird2'
        }
    )
    assert response.status_code == 302
    b = Bird.objects.get(scientific_name='test-bird2')
    assert b.name == 'Test bird2'


@pytest.mark.django_db
def test_add_bird2(client, bird):
    r = client.post(
        reverse('add_bird'),
        {
            'name': bird.name,
            'scientific_name': bird.scientific_name
        }
    )
    assert r.status_code == 302

@pytest.mark.django_db
def test_details(client):
    response = client.get('/add_bird/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_bird_detail(client, bird):
    r = client.get(reverse('bird', args=[bird.pk]))
    assert r.status_code == 200
    assert r.context['bird'] == bird


@pytest.mark.django_db
def test_add_place(client):
    r = client.post(
        reverse('add_place'),
        {
            'name': 'Test place',
            'city': 'test city',
            'country': 'test country'
        }
    )
    assert r.status_code == 302
    p = Place.objects.get(name='Test place')
    assert p.city == 'test city'


@pytest.mark.django_db
def test_place_view(client, place):
    r = client.get(reverse('place', args=[place.pk]))
    assert r.status_code == 200
    p = Place.objects.get(pk=place.pk)
    assert p.name == 'Test place'


@pytest.mark.django_db
def test_birdstand(client, bird, place, watcher):
    r = client.post('/add_birdstand/',
        {
            'bird': bird.pk,
            'place': place.pk,
            'watcher': watcher.pk
        }
    )
    print(r)
    assert r.status_code == 302
    assert BirdStand.objects.all()


@pytest.mark.django_db
def test_birdstand_bad_data(client):
    r = client.post('/add_birdstand/',
        {
            'bird': '...',
            'place': 'bzdury_place1',
            'watcher': 'bzdury_watecher1'
        }
    )
    assert len(r.context['form'].errors) > 0


@pytest.mark.django_db
def test_show_birds(client):
    r = client.get(reverse('birds'))
    assert r.status_code == 200



@pytest.mark.django_db
def test_watcher(client, watcher):
    r = client.get(reverse('watcher', args=[watcher.pk]))
    assert r.status_code == 200
    assert r.context['watcher'] == watcher

@pytest.mark.django_db
def test_watcher2(client, watchers):
    r = client.get(reverse('watcher', args=[watchers[0].pk]))
    assert r.status_code == 200
    assert r.context['watcher'] == watchers[0]



@pytest.mark.django_db
def test_add_watcher_no_permission(client, common_user):
    client.force_login(common_user)
    r = client.post(
        reverse('add_watcher'),
        {
            'first_name': 'New watecher',
            'last_name': 'test'
        }
    )
    assert r.status_code == 403  # forbidden

@pytest.mark.django_db
def test_add_watcher_permission(client, superuser):
    client.force_login(superuser)
    r = client.post(
        reverse('add_watcher'),
        {
            'first_name': 'New watecher',
            'last_name': 'test'
        }
    )
    assert r.status_code == 302


@pytest.mark.django_db
def test_birdstand_view(client, bird, place):
    r = client.get(reverse('birdstand', args=[bird.pk, place.pk]))
    assert r.status_code == 200

#ten nie działa w pytest .
# @pytest.mark.django_db
# def test_list_user(client, common_user):
#     r = client.get(reverse('list_users'))
#     assert r.status_code == 200
#     u = User.objects.get(pk=1)
#     assert u.username == 'cmnuser'
#     assert User.objects.all()


@pytest.mark.django_db
def test_list_user2(client, users):
    r = client.get(reverse('list_users'))
    assert r.context['users']


@pytest.mark.django_db
def test_logout(client):
    r = client.get(reverse('logout'))
    assert r.status_code == 302


@pytest.mark.django_db
def test_create_user(client):
    r = client.post(
        reverse('add_user'),
        {
            'user_name': 'user_name11111',
            'password': 'password',
            'password_rep': 'password',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email'
        }
    )
    assert r.status_code == 200
    assert 'form' in r.context


# @pytest.mark.django_db
# def test_create_user(client):
#     r = client.post(
#         reverse('add_user'),
#         {
#             'user_name': '___',
#             'password': '',
#             'password_rep': 'password',
#             'first_name': 'first_name',
#             'last_name': 'last_name',
#             'email': 'email'
#         }
#     )
#     assert r.status_code == 200
#     assert len(r.context['form'].errors) > 0


@pytest.mark.django_db
def test_add_bird_photo(client):
    r = client.get(reverse('addbird_photo'))
    assert r.status_code == 200



@pytest.mark.django_db
def test_add_bird_photo(client, bird):
    newphoto = BirdPhoto()
    newphoto.image = 'static/bw.jpg'
    newphoto.save()
    r = client.post('/addbird_photo/',
                    {
                        'image': newphoto.image,
                        'name': bird.pk
                    }
    )
    assert r.status_code == 302
    assert BirdPhoto.objects.all()
