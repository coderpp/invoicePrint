#!/usr/bin/env python3
"""
跨平台打包脚本
将 invoiceprint 打包成独立可执行文件
"""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def get_platform_info():
    """获取平台信息"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "darwin":
        platform_name = "macos"
    elif system == "windows":
        platform_name = "windows"
    elif system == "linux":
        platform_name = "linux"
    else:
        platform_name = system
    
    # 架构
    if machine in ("x86_64", "amd64"):
        arch = "x64"
    elif machine in ("arm64", "aarch64"):
        arch = "arm64"
    else:
        arch = machine
    
    return platform_name, arch


def clean_build():
    """清理构建目录"""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    files_to_clean = ["*.spec"]
    
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"清理目录: {dir_path}")
            shutil.rmtree(dir_path)
    
    for pattern in files_to_clean:
        for file_path in Path(".").glob(pattern):
            print(f"清理文件: {file_path}")
            file_path.unlink()


def build_executable():
    """构建可执行文件"""
    platform_name, arch = get_platform_info()
    
    print(f"平台: {platform_name}")
    print(f"架构: {arch}")
    print("-" * 40)
    
    # 输出文件名
    if platform_name == "windows":
        exe_name = "invoiceprint.exe"
    else:
        exe_name = "invoiceprint"
    
    output_name = f"invoiceprint-{platform_name}-{arch}"
    
    # PyInstaller 参数
    pyinstaller_args = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",           # 打包成单个文件
        "--clean",             # 清理临时文件
        "--noconfirm",         # 不确认覆盖
        "--name", output_name, # 输出文件名
        "main.py"              # 入口文件
    ]
    
    # Windows 特定选项：隐藏控制台窗口（如果需要的话可以取消注释）
    # if platform_name == "windows":
    #     pyinstaller_args.insert(-1, "--noconsole")
    
    print("开始打包...")
    print(f"命令: {' '.join(pyinstaller_args)}")
    print("-" * 40)
    
    # 执行打包
    result = subprocess.run(pyinstaller_args)
    
    if result.returncode != 0:
        print("打包失败!")
        return False
    
    # 检查输出文件
    if platform_name == "windows":
        output_file = Path("dist") / f"{output_name}.exe"
    else:
        output_file = Path("dist") / output_name
    
    if output_file.exists():
        file_size = output_file.stat().st_size / (1024 * 1024)  # MB
        print("-" * 40)
        print(f"打包成功!")
        print(f"输出文件: {output_file}")
        print(f"文件大小: {file_size:.2f} MB")
        return True
    else:
        print("打包失败: 输出文件不存在")
        return False


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="跨平台打包脚本")
    parser.add_argument(
        "--clean", "-c",
        action="store_true",
        help="仅清理构建目录"
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="打包前不清理"
    )
    
    args = parser.parse_args()
    
    # 切换到脚本所在目录
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    if args.clean:
        clean_build()
        print("清理完成!")
        return 0
    
    if not args.no_clean:
        clean_build()
    
    # 检查 PyInstaller 是否安装
    try:
        import PyInstaller
        print(f"PyInstaller 版本: {PyInstaller.__version__}")
    except ImportError:
        print("错误: PyInstaller 未安装")
        print("请运行: uv pip install pyinstaller")
        print("或者: uv sync --extra dev")
        return 1
    
    success = build_executable()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

