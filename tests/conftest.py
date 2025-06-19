import pytest
import requests
from typing import Generator
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 测试配置
BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:3000")
ADMIN_EMAIL = os.getenv("TEST_ADMIN_EMAIL", "admin@test.com")
ADMIN_PASSWORD = os.getenv("TEST_ADMIN_PASSWORD", "test123")
NORMAL_USER_EMAIL = os.getenv("TEST_NORMAL_USER_EMAIL", "user@test.com")
NORMAL_USER_PASSWORD = os.getenv("TEST_NORMAL_USER_PASSWORD", "test123")

@pytest.fixture(scope="session")
def admin_token() -> Generator[str, None, None]:
    """获取管理员token的fixture"""
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    )
    assert response.status_code == 200
    token = response.cookies.get("user_session")
    if not token:
        pytest.fail("Failed to get admin token")
    yield token

@pytest.fixture(scope="session")
def normal_user_token() -> Generator[str, None, None]:
    """获取普通用户token的fixture"""
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": NORMAL_USER_EMAIL, "password": NORMAL_USER_PASSWORD}
    )
    assert response.status_code == 200
    token = response.cookies.get("user_session")
    if not token:
        pytest.fail("Failed to get normal user token")
    yield token

@pytest.fixture(scope="session")
def test_log_id(admin_token: str) -> Generator[str, None, None]:
    """获取测试日志ID的fixture"""
    response = requests.get(
        f"{BASE_URL}/api/logs",
        cookies={"user_session": admin_token}
    )
    assert response.status_code == 200
    data = response.json()
    if not data["logs"]:
        pytest.skip("No logs available for testing")
    yield data["logs"][0]["id"] 