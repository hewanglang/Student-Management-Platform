@echo off
echo 管理员日志查询自动化测试脚本
echo ==============================

:menu
echo.
echo 请选择要运行的测试：
echo 1. 运行所有测试
echo 2. 运行管理员获取日志列表测试
echo 3. 运行分页查询测试
echo 4. 运行筛选功能测试
echo 5. 运行日志详情测试
echo 6. 运行日志清空测试
echo 7. 运行日志初始化测试
echo 8. 生成HTML测试报告
echo 9. 退出
echo.

set /p choice=请输入选项（1-9）: 

if "%choice%"=="1" (
    echo 正在运行所有测试...
    python -m pytest tests/test_logs.py -v
    goto menu
)

if "%choice%"=="2" (
    echo 正在运行管理员获取日志列表测试...
    python -m pytest tests/test_logs.py::TestLogs::test_get_logs_list_admin -v
    goto menu
)

if "%choice%"=="3" (
    echo 正在运行分页查询测试...
    python -m pytest tests/test_logs.py::TestLogs::test_get_logs_with_pagination -v
    goto menu
)

if "%choice%"=="4" (
    echo 正在运行筛选功能测试...
    python -m pytest tests/test_logs.py::TestLogs::test_get_logs_with_filters -v
    goto menu
)

if "%choice%"=="5" (
    echo 正在运行日志详情测试...
    python -m pytest tests/test_logs.py::TestLogs::test_get_log_detail -v
    goto menu
)

if "%choice%"=="6" (
    echo 正在运行日志清空测试...
    python -m pytest tests/test_logs.py::TestLogs::test_clear_logs -v
    goto menu
)

if "%choice%"=="7" (
    echo 正在运行日志初始化测试...
    python -m pytest tests/test_logs.py::TestLogs::test_init_logs -v
    goto menu
)

if "%choice%"=="8" (
    echo 正在生成HTML测试报告...
    python -m pytest tests/test_logs.py -v --html=report.html
    echo 测试报告已生成：report.html
    goto menu
)

if "%choice%"=="9" (
    echo 感谢使用，再见！
    exit /b 0
)

echo 无效的选项，请重新选择
goto menu 