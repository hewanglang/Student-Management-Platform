import pytest
import requests
from datetime import datetime
import json
import os
from typing import Dict, Any

# 测试配置
BASE_URL = "http://localhost:3000"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "123456"
NORMAL_USER_EMAIL = "student@example.com"
NORMAL_USER_PASSWORD = "123456"

class TestLogs:
    @pytest.fixture(scope="class")
    def admin_token(self) -> str:
        """获取管理员token"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
        )
        assert response.status_code == 200
        return response.cookies.get("user_session")

    @pytest.fixture(scope="class")
    def normal_user_token(self) -> str:
        """获取普通用户token"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": NORMAL_USER_EMAIL, "password": NORMAL_USER_PASSWORD}
        )
        assert response.status_code == 200
        return response.cookies.get("user_session")

    def test_get_logs_list_admin(self, admin_token: str):
        """测试管理员获取日志列表"""
        response = requests.get(
            f"{BASE_URL}/api/logs",
            cookies={"user_session": admin_token}
        )
        assert response.status_code == 200
        data = response.json()
        assert "logs" in data
        assert "pagination" in data

    def test_get_logs_list_normal_user(self, normal_user_token: str):
        """测试普通用户获取日志列表（应该被拒绝）"""
        response = requests.get(
            f"{BASE_URL}/api/logs",
            cookies={"user_session": normal_user_token}
        )
        assert response.status_code == 403

    def test_get_logs_with_pagination(self, admin_token: str):
        """测试分页查询"""
        response = requests.get(
            f"{BASE_URL}/api/logs?page=1&limit=10",
            cookies={"user_session": admin_token}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["pagination"]["page"] == 1
        assert data["pagination"]["limit"] == 10

    def test_get_logs_with_filters(self, admin_token: str):
        """测试带筛选条件的查询"""
        # 获取当前日期
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 测试日期范围筛选
        response = requests.get(
            f"{BASE_URL}/api/logs?startDate={today}&endDate={today}",
            cookies={"user_session": admin_token}
        )
        assert response.status_code == 200
        data = response.json()
        assert "logs" in data

        # 测试操作类型筛选
        response = requests.get(
            f"{BASE_URL}/api/logs?action=用户登录",
            cookies={"user_session": admin_token}
        )
        assert response.status_code == 200
        data = response.json()
        assert "logs" in data

    def test_get_log_detail(self, admin_token: str, normal_user_token: str):
        """测试获取日志详情"""
        # 首先获取一条日志的ID
        response = requests.get(
            f"{BASE_URL}/api/logs",
            cookies={"user_session": admin_token}
        )
        assert response.status_code == 200
        data = response.json()
        if data["logs"]:
            log_id = data["logs"][0]["id"]
            
            # 测试管理员查看日志详情
            response = requests.get(
                f"{BASE_URL}/api/logs/{log_id}",
                cookies={"user_session": admin_token}
            )
            assert response.status_code == 200
            assert response.json()["log"]["id"] == log_id

            # 测试普通用户查看日志详情（应该被拒绝）
            response = requests.get(
                f"{BASE_URL}/api/logs/{log_id}",
                cookies={"user_session": normal_user_token}
            )
            assert response.status_code == 403

    def test_clear_logs(self, admin_token: str, normal_user_token: str):
        """测试清空日志"""
        # 测试管理员清空日志
        response = requests.delete(
            f"{BASE_URL}/api/logs/clear",
            cookies={"user_session": admin_token}
        )
        assert response.status_code == 200
        assert response.json()["message"] == "系统日志已清空"

        # 测试普通用户清空日志（应该被拒绝）
        response = requests.delete(
            f"{BASE_URL}/api/logs/clear",
            cookies={"user_session": normal_user_token}
        )
        assert response.status_code == 403

    def test_init_logs(self, admin_token: str, normal_user_token: str):
        """测试初始化日志"""
        # 测试管理员初始化日志
        response = requests.post(
            f"{BASE_URL}/api/logs/init",
            cookies={"user_session": admin_token}
        )
        assert response.status_code == 200
        assert "message" in response.json()

        # 测试普通用户初始化日志（应该被拒绝）
        response = requests.post(
            f"{BASE_URL}/api/logs/init",
            cookies={"user_session": normal_user_token}
        )
        assert response.status_code == 403

if __name__ == "__main__":
    pytest.main(["-v", "test_logs.py"]) 