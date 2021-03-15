import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN
from rest_framework.authtoken.models import Token
from user.models import User
from product.models import Product


@pytest.mark.django_db
def test_products_get(api_client, product_factory):
    # arrange
    product = product_factory()
    url = reverse('product-detail', args=[product.id])

    # act
    response = api_client.get(url)

    # assert
    assert response.status_code == HTTP_200_OK
    response_json = response.json()
    assert response_json
    assert response_json['id'] == product.id
    assert response_json['name'] == product.name


@pytest.mark.django_db
def test_products_list(api_client, product_factory):
    product1 = product_factory()
    product2 = product_factory()
    url = reverse('product-list')

    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == 2

    result_ids = {product['id'] for product in response_json}
    assert {product1.id, product2.id} == result_ids


@pytest.mark.django_db
def test_products_filter_id(api_client, product_factory):
    product1 = product_factory()
    product2 = product_factory()
    url = reverse('product-list')

    response = api_client.get(url, {'id': product1.id})

    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == 1

    result = response_json[0]
    assert result['id'] == product1.id


@pytest.mark.django_db
def test_products_filter_name(api_client, product_factory):
    product1 = product_factory()
    product_factory()
    url = reverse('product-list')

    response = api_client.get(url, {'name': product1.name})

    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == 1

    result = response_json[0]
    assert result['name'] == product1.name


@pytest.mark.django_db
def test_products_filter_description(api_client, product_factory):
    product1 = product_factory()
    product2 = product_factory()
    url = reverse('product-list')

    response = api_client.get(url, {'description': product1.description})

    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == 1

    result = response_json[0]
    assert result['description'] == product1.description


@pytest.mark.parametrize(
    ['price_min', 'price_max', 'total_products'],
    (
        (150, 300, 2),
        (50, 120, 1),
    )
)
@pytest.mark.django_db
def test_products_filter_price(api_client, product_factory, price_min, price_max, total_products):
    product1 = product_factory(price=200)
    product2 = product_factory(price=100)
    product3 = product_factory(price=170)
    url = reverse('product-list')

    response = api_client.get(url, {'price_min': {price_min}, 'price_max': {price_max}})

    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == total_products


@pytest.mark.parametrize(
    ['is_staff', 'status_code', 'length'],
    (
        (True, HTTP_201_CREATED, 1),
        (False, HTTP_403_FORBIDDEN, 0),
    )
)
@pytest.mark.django_db
def test_products_create(api_client, product_factory, is_staff, status_code, length):
    # arrange
    user = User.objects.create_user('user', 'user@example.org', 'user12345', is_active=True, is_staff=is_staff)
    token = Token.objects.create(user=user)
    url = reverse('product-list')
    product_payload = {
        'name': 'socks',
        'description': 'nice socks',
        'price': 100,
    }
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    # act
    response = api_client.post(url, product_payload)
    created_product = Product.objects.filter(name=product_payload['name'])

    # assert
    assert response.status_code == status_code
    assert len(created_product) == length
