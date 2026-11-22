
import pytest

from src.data.redis_reader import RedisReader


def test_redis_connection(redis):

    client = redis.get_connection()

    assert client.ping() is True


def test_redis_connection_reuse(redis):

    first_connection = redis.get_connection()

    second_connection = redis.get_connection()

    assert first_connection is second_connection


def test_redis_close_connection(redis):

    client = redis.get_connection()

    redis.close_connection()

    assert redis.client is None


def test_redis_reconnect_after_close(redis):

    first_connection = redis.get_connection()

    redis.close_connection()

    second_connection = redis.get_connection()

    assert second_connection is not first_connection

    assert second_connection.ping() is True


def test_redis_store_and_retrieve_data(redis):

    client = redis.get_connection()

    client.set("test_username", "standard_user")

    result = client.get("test_username")

    assert result == "standard_user"


def test_redis_delete_data(redis):

    client = redis.get_connection()

    client.set("test_key", "test_value")

    result = client.delete("test_key")

    assert result == 1

    assert client.get("test_key") is None


def test_redis_nonexistent_key(redis):

    client = redis.get_connection()

    result = client.get("nonexistent_key")

    assert result is None
