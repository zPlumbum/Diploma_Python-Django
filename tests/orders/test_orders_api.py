import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
from user.models import User
from order.models import OrderProduct


@pytest.mark.django_db
def test_orders_get(api_client, product_factory, order_factory):
    user = User.objects.create_user('user', 'user@example.org', 'user12345', is_active=True)
    token = Token.objects.create(user=user)
    product = product_factory()
    order = order_factory(creator_id=user)
    positions = OrderProduct.objects.create(product=product, order=order, quantity=2)

    url = reverse('order-detail', args=[order.id])
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK
    response_json = response.json()
    assert response_json['id'] == order.id
    assert response_json['order_positions'][0]['product'] == product.id


@pytest.mark.django_db
def test_orders_list(api_client, product_factory, order_factory):
    user = User.objects.create_user('user', 'user@example.org', 'user12345', is_active=True)
    token = Token.objects.create(user=user)
    product = product_factory()
    order1 = order_factory(creator_id=user)
    order2 = order_factory(creator_id=user)
    positions = OrderProduct.objects.create(product=product, order=order1, quantity=2)
    positions = OrderProduct.objects.create(product=product, order=order2, quantity=1)

    url = reverse('order-list')
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == 2

    result_ids = {order['id'] for order in response_json}
    assert {order1.id, order2.id} == result_ids


@pytest.mark.django_db
def test_orders_not_authorized(api_client, product_factory, order_factory):
    user = User.objects.create_user('user', 'user@example.org', 'user12345', is_active=True)
    token = Token.objects.create(user=user)
    product = product_factory()
    order = order_factory(creator_id=user)
    positions = OrderProduct.objects.create(product=product, order=order, quantity=2)

    url = reverse('order-list')

    response = api_client.get(url)

    assert response.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_orders_not_owner(api_client, product_factory, order_factory):
    user1 = User.objects.create_user('user1', 'user1@example.org', 'user12345', is_active=True)
    token1 = Token.objects.create(user=user1)
    user2 = User.objects.create_user('user2', 'user2@example.org', 'user12345', is_active=True)
    token2 = Token.objects.create(user=user2)
    product = product_factory()
    order = order_factory(creator_id=user1)
    positions = OrderProduct.objects.create(product=product, order=order, quantity=2)

    url = reverse('order-detail', args=[order.id])
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token2.key)

    response = api_client.delete(url)

    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_orders_filter_id(api_client, product_factory, order_factory):
    user = User.objects.create_user('user', 'user@example.org', 'user12345', is_active=True)
    token = Token.objects.create(user=user)
    product = product_factory()
    order = order_factory(creator_id=user)
    positions = OrderProduct.objects.create(product=product, order=order, quantity=2)

    url = reverse('order-list')
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    response = api_client.get(url, {'id': order.id})

    assert response.status_code == HTTP_200_OK
    response_json = response.json()
    assert len(response_json) == 1
    assert response_json[0]['id'] == order.id


@pytest.mark.parametrize(
    ['status', 'total_count'],
    (
        ('NEW', 1),
        ('IN_PROGRESS', 0)
    )
)
@pytest.mark.django_db
def test_orders_filter_status(api_client, product_factory, order_factory, status, total_count):
    user = User.objects.create_user('user', 'user@example.org', 'user12345', is_active=True)
    token = Token.objects.create(user=user)
    product = product_factory()
    order = order_factory(creator_id=user)
    positions = OrderProduct.objects.create(product=product, order=order, quantity=2)

    url = reverse('order-list')
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    response = api_client.get(url, {'status': status})

    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == total_count


@pytest.mark.parametrize(
    ['date', 'total_count'],
    (
        ('2025-03-10', 1),
        ('2018-03-10', 0),
    )
)
@pytest.mark.django_db
def test_orders_filter_created_at(api_client, product_factory, order_factory, date, total_count):
    user = User.objects.create_user('user', 'user@example.org', 'user12345', is_active=True)
    token = Token.objects.create(user=user)
    product = product_factory()
    order = order_factory(creator_id=user)
    positions = OrderProduct.objects.create(product=product, order=order, quantity=2)

    url = reverse('order-list')
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    response = api_client.get(url, {'created_at_before': date})

    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == total_count


@pytest.mark.parametrize(
    ['date', 'total_count'],
    (
        ('2025-03-10', 0),
        ('2018-03-10', 1),
    )
)
@pytest.mark.django_db
def test_orders_filter_updated_at(api_client, product_factory, order_factory, date, total_count):
    user = User.objects.create_user('user', 'user@example.org', 'user12345', is_active=True)
    token = Token.objects.create(user=user)
    product = product_factory()
    order = order_factory(creator_id=user)
    positions = OrderProduct.objects.create(product=product, order=order, quantity=2)

    url = reverse('order-list')
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    response = api_client.get(url, {'updated_at_after': date})

    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == total_count


@pytest.mark.django_db
def test_orders_filter_positions(api_client, product_factory, order_factory):
    user = User.objects.create_user('user', 'user@example.org', 'user12345', is_active=True)
    token = Token.objects.create(user=user)
    product = product_factory()
    order = order_factory(creator_id=user)
    positions = OrderProduct.objects.create(product=product, order=order, quantity=2)

    url = reverse('order-list')
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    response = api_client.get(url, {'positions': product.id})

    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == 1
    assert response_json[0]['order_positions'][0]['product'] == product.id


@pytest.mark.django_db
def test_orders_create(api_client, product_factory):
    user = User.objects.create_user('user', 'user@example.org', 'user12345', is_active=True)
    token = Token.objects.create(user=user)
    product = product_factory()
    url = reverse('order-list')
    order_payload = {
        'creator_id': user.id,
        'order_positions': [
            {
                'product': product.id,
                'quantity': 3
            }
        ]
    }
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    response = api_client.post(url, order_payload, format='json')

    assert response.status_code == HTTP_201_CREATED
    response_json = response.json()
    assert len(response_json['order_positions']) == 1
    assert response_json['order_positions'][0]['product'] == product.id


@pytest.mark.parametrize(
    ['total_price_min', 'total_count'],
    (
        (100, 1),
        (99999, 0),
    )
)
@pytest.mark.django_db
def test_orders_filter_total_price(api_client, product_factory, total_price_min, total_count):
    user = User.objects.create_user('user', 'user@example.org', 'user12345', is_active=True)
    token = Token.objects.create(user=user)
    product = product_factory(price=100)
    url = reverse('order-list')
    order_payload = {
        'creator_id': user.id,
        'order_positions': [
            {
                'product': product.id,
                'quantity': 3
            }
        ]
    }
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    response_post = api_client.post(url, order_payload, format='json')
    response_get = api_client.get(url, {'total_price_min': total_price_min})

    assert response_post.status_code == HTTP_201_CREATED
    assert response_get.status_code == HTTP_200_OK

    response_json = response_get.json()
    assert len(response_json) == total_count


@pytest.mark.parametrize(
    ['is_staff', 'total_count'],
    (
        (False, 1),
        (True, 2),
    )
)
@pytest.mark.django_db
def test_orders_display_order(api_client, product_factory, order_factory, is_staff, total_count):
    user1 = User.objects.create_user('user1', 'user1@example.org', 'user12345', is_active=True, is_staff=is_staff)
    token1 = Token.objects.create(user=user1)
    user2 = User.objects.create_user('user2', 'user2@example.org', 'user12345', is_active=True)
    token2 = Token.objects.create(user=user2)

    product = product_factory()
    order1 = order_factory(creator_id=user1)
    order2 = order_factory(creator_id=user2)
    positions1 = OrderProduct.objects.create(product=product, order=order1, quantity=2)
    positions2 = OrderProduct.objects.create(product=product, order=order2, quantity=2)

    url = reverse('order-list')
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token1.key)

    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == total_count
