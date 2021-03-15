import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN
from rest_framework.authtoken.models import Token
from user.models import User


@pytest.mark.django_db
def test_product_reviews_get(api_client, product_factory, product_review_factory):
    user = User.objects.create_user('user', 'user@example.org', 'user12345', is_active=True)
    product = product_factory()
    product_review = product_review_factory(creator_id=user, product_id=product)
    url = reverse('product-review-detail', args=[product_review.id])

    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK
    response_json = response.json()
    assert response_json['id'] == product_review.id
    assert response_json['creator_id']['id'] == user.id
    assert response_json['product_id'] == product.id


@pytest.mark.django_db
def test_product_reviews_list(api_client, product_factory, product_review_factory):
    user1 = User.objects.create_user('user1', 'user1@example.org', 'user12345', is_active=True)
    user2 = User.objects.create_user('user2', 'user2@example.org', 'user12345', is_active=True)
    product = product_factory()

    product_review1 = product_review_factory(creator_id=user1, product_id=product)
    product_review2 = product_review_factory(creator_id=user2, product_id=product)
    url = reverse('product-review-list')

    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == 2

    result_ids = {product_review['id'] for product_review in response_json}
    assert {product_review1.id, product_review2.id} == result_ids


@pytest.mark.django_db
def test_product_reviews_filter_id(api_client, product_factory, product_review_factory):
    user = User.objects.create_user('user', 'user@example.org', 'user12345', is_active=True)
    product = product_factory()
    product_review = product_review_factory(creator_id=user, product_id=product)
    url = reverse('product-review-list')

    response = api_client.get(url, {'id': product_review.id})

    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == 1

    result = response_json[0]
    assert result['id'] == product_review.id


@pytest.mark.django_db
def test_product_reviews_filter_creator_id(api_client, product_factory, product_review_factory):
    user = User.objects.create_user('user', 'user@example.org', 'user12345', is_active=True)
    product = product_factory()
    product_review = product_review_factory(creator_id=user, product_id=product)
    url = reverse('product-review-list')

    response = api_client.get(url, {'creator_id': product_review.creator_id.id})

    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == 1

    result = response_json[0]
    assert result['creator_id']['id'] == product_review.creator_id.id


@pytest.mark.django_db
def test_product_reviews_filter_product_id(api_client, product_factory, product_review_factory):
    user = User.objects.create_user('user', 'user@example.org', 'user12345', is_active=True)
    product = product_factory()
    product_review = product_review_factory(creator_id=user, product_id=product)
    url = reverse('product-review-list')

    response = api_client.get(url, {'product_id': product_review.product_id.id})

    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == 1

    result = response_json[0]
    assert result['product_id'] == product_review.product_id.id


@pytest.mark.parametrize(
    ['evaluation', 'total_count'],
    (
        (5, 1),
        (2, 0),
    )
)
@pytest.mark.django_db
def test_product_reviews_filter_evaluation(api_client, product_factory, product_review_factory, evaluation, total_count):
    user = User.objects.create_user('user', 'user@example.org', 'user12345', is_active=True)
    product = product_factory()
    product_review = product_review_factory(creator_id=user, product_id=product, evaluation=evaluation)
    url = reverse('product-review-list')

    response = api_client.get(url, {'evaluation_min': 3})

    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == total_count


@pytest.mark.parametrize(
    ['date', 'total_count'],
    (
        ('2025-03-10', 1),
        ('2018-03-10', 0),
    )
)
@pytest.mark.django_db
def test_product_reviews_filter_created_at(api_client, product_factory, product_review_factory, date, total_count):
    user = User.objects.create_user('user', 'user@example.org', 'user12345', is_active=True)
    product = product_factory()
    product_review = product_review_factory(creator_id=user, product_id=product)
    url = reverse('product-review-list')

    response = api_client.get(url, {'created_at_before': date})

    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == total_count


@pytest.mark.django_db
def test_product_reviews_create(api_client, product_factory):
    user = User.objects.create_user('user', 'user@example.org', 'user12345', is_active=True)
    token = Token.objects.create(user=user)
    product = product_factory()
    url = reverse('product-review-list')
    payload = {
        'creator_id': user,
        'product_id': product.id,
        'text': 'Very nice product',
        'evaluation': 5,
    }
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    response = api_client.post(url, payload)

    assert response.status_code == HTTP_201_CREATED
    response_json = response.json()
    assert response_json['creator_id']['id'] == user.id
    assert response_json['product_id'] == product.id


@pytest.mark.django_db
def test_product_reviews_delete(api_client, product_factory, product_review_factory):
    user1 = User.objects.create_user('user1', 'user1@example.org', 'user12345', is_active=True)
    user2 = User.objects.create_user('user2', 'user2@example.org', 'user12345', is_active=True)
    token2 = Token.objects.create(user=user2)

    product = product_factory()
    product_review = product_review_factory(creator_id=user1, product_id=product)

    url = reverse('product-review-detail', args=[product_review.id])
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token2.key)

    response = api_client.delete(url)

    assert response.status_code == HTTP_403_FORBIDDEN
