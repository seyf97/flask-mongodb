from app.models.article import Article
from app.models.user import User
import mongoengine as me
import pytest


def test_user_model_normal():
    user = {
        "email": "test@example.com",
        "password": "topSecret"
    }
    new_user = User(**user)
    new_user.validate()


def test_article_model_normal():
    article = {
        "title": "Test title",
        "content": "Test content",
        "category": "Test category"
    }
    new_article = Article(**article)
    new_article.validate()


def test_user_model_missing_field():
    user = {
        "email": "test@example.com",
    }
    new_user = User(**user)

    with pytest.raises(me.errors.ValidationError) as e:
        new_user.validate()


def test_article_model_missing_field():
    article = {
        "content": "Test content",
        "category": "Test category"
    }
    new_article = Article(**article)
    
    with pytest.raises(me.errors.ValidationError) as e:
        new_article.validate()