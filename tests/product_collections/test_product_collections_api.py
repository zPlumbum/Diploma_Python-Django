import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN
from rest_framework.authtoken.models import Token
from user.models import User
from product_collection.models import ProductInCollection


@pytest.mark.django_db
def test_product_collections_get(api_client, product_factory, product_collection_factory):
    product_collection = product_collection_factory()
    product = product_factory()
    products = ProductInCollection.objects.create(product=product, collection=product_collection)
    url = reverse('product-collection-detail', args=[product_collection.id])

    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK
    response_json = response.json()
    assert response_json['id'] == product_collection.id
    assert response_json['products_in'][0]['product_id'] == product.id


@pytest.mark.django_db
def test_product_collections_list(api_client, product_factory, product_collection_factory):
    product_collection1 = product_collection_factory()
    product_collection2 = product_collection_factory()
    product1 = product_factory()
    product2 = product_factory()
    products1 = ProductInCollection.objects.create(product=product1, collection=product_collection1)
    products2 = ProductInCollection.objects.create(product=product1, collection=product_collection2)
    products3 = ProductInCollection.objects.create(product=product2, collection=product_collection2)
    url = reverse('product-collection-list')

    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == 2

    result_ids = {collection['id'] for collection in response_json}
    assert {product_collection1.id, product_collection2.id} == result_ids


@pytest.mark.parametrize(
    ['is_staff', 'result'],
    (
        (True, HTTP_201_CREATED),
        (False, HTTP_403_FORBIDDEN)
    )
)
@pytest.mark.django_db
def test_product_collections_create(api_client, product_factory, is_staff, result):
    user = User.objects.create_user('user', 'user@example.org', 'user12345', is_active=True, is_staff=is_staff)
    token = Token.objects.create(user=user)
    product1 = product_factory()
    product2 = product_factory()
    url = reverse('product-collection-list')
    payload = {
        "title": "Clothes",
        "text": "These things will help you stay warm",
        "products_in": [
            {
                "product_id": product1.id
            },
            {
                "product_id": product2.id
            }
        ]
    }
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    response = api_client.post(url, payload, format='json')

    assert response.status_code == result
