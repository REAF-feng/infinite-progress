"""
Python 学习环境快速验证

运行方式：
  - 终端: .\\.venv\\Scripts\\Activate.ps1; python python-course/检查环境.py
  - 或在 VS Code 中右键此文件 → "Run Python File"

本脚本检查所有学习工具是否已正确安装。
"""

import sys
import os

# 确保 Windows 下输出不乱码
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def check_python():
    """检查 Python 版本"""
    version = sys.version_info
    print(f"[OK] Python {version.major}.{version.minor}.{version.micro}")
    print(f"     路径: {sys.executable}")
    return version >= (3, 10)


def check_package(name, import_name=None):
    """检查某个包是否可导入"""
    if import_name is None:
        import_name = name
    try:
        __import__(import_name)
        print(f"[OK] {name}")
        return True
    except ImportError:
        print(f"[MISSING] {name} -- 未安装")
        return False


def main():
    print("=" * 50)
    print("  Python 学习环境检查")
    print("=" * 50)

    results = []

    # 基础检查
    print("\n[基础环境]")
    results.append(check_python())

    # 工具包检查
    print("\n[工具包]")
    results.append(check_package("IPython", "IPython"))
    results.append(check_package("JupyterLab", "jupyterlab"))
    results.append(check_package("pytest"))
    results.append(check_package("black"))
    results.append(check_package("pylint"))

    # 常用标准库（无需安装）
    print("\n[常用标准库 -- 内置]")
    for lib in ["json", "csv", "random", "datetime", "math", "os", "pathlib", "re"]:
        check_package(lib)

    print("\n" + "=" * 50)
    if all(results):
        print("  全部就绪! 开始你的 Python 学习之旅吧!")
    else:
        print("  部分工具未安装，请运行:")
        print("  pip install ipython jupyterlab black pylint pytest")
    print("=" * 50)


if __name__ == "__main__":
    main()
