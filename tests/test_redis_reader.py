
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


def test_store_and_retrieve_structured_test_data(redis):

    test_data = {
        "username": "standard_user",
        "password": "secret_sauce",
        "expected": "success"
    }

    result = redis.store_test_data("login_test", test_data)

    assert result is True

    retrieved_data = redis.get_test_data("login_test")

    assert retrieved_data == test_data


def test_get_all_test_data(redis):

    first_record = {
        "username": "standard_user",
        "expected": "success"
    }

    second_record = {
        "username": "locked_out_user",
        "expected": "failure"
    }

    redis.store_test_data("login_1", first_record)
    redis.store_test_data("login_2", second_record)

    result = redis.get_all_test_data()

    assert "login_1" in result
    assert "login_2" in result

    assert result["login_1"] == first_record
    assert result["login_2"] == second_record


def test_get_nonexistent_test_data(redis):

    result = redis.get_test_data("nonexistent_test_data")

    assert result is None


def test_delete_test_data(redis):

    test_data = {
        "username": "standard_user",
        "expected": "success"
    }

    redis.store_test_data("delete_test", test_data)

    result = redis.delete_test_data("delete_test")

    assert result == 1

    assert redis.get_test_data("delete_test") is None

def test_delete_all_test_data(redis):

    redis.store_test_data(
        "cleanup_1",
        {"username": "standard_user"}
    )

    redis.store_test_data(
        "cleanup_2",
        {"username": "locked_out_user"}
    )

    client = redis.get_connection()

    client.set("unrelated_key", "keep_me")

    result = redis.delete_all_test_data()

    assert result >= 2

    assert redis.get_test_data("cleanup_1") is None
    assert redis.get_test_data("cleanup_2") is None

    assert client.get("unrelated_key") == "keep_me"

    client.delete("unrelated_key")