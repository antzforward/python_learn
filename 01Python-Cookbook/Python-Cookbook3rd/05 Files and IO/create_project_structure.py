import os
import sys
from pathlib import Path


def create_directory_structure(root_dir):
    """生成支持多语言对比的目录结构"""

    # 定义完整的目录结构（包含示例文件）
    structure = {
        ".devcontainer": {
            "devcontainer.json": None,  # 容器配置文件
            "docker-compose.yml": None
        },
        ".vscode": {
            "settings.json": None,  # 编辑器配置
            "launch.json": None,  # 调试配置
            "tasks.json": None  # 任务配置
        },
        "bin": [],  # 编译输出目录（空目录）
        "docs": {
            "sorting_example.md": None  # 对比文档示例
        },
        "src": {
            "algorithms": {  # 算法实现模块
                "cpp": {
                    "quicksort.cpp": None,
                    "CMakeLists.txt": None
                },
                "go": {
                    "quicksort.go": None,
                    "go.mod": None
                },
                "python": {
                    "quicksort.py": None
                },
                "rust": {
                    "quicksort.rs": None,
                    "Cargo.toml": None
                }
            },
            "web_api": {  # Web API模块
                "csharp": {
                    "WebApi.csproj": None,
                    "Controllers": {
                        "ValuesController.cs": None  # 添加示例文件
                    }
                },
                "typescript": {
                    "src": {
                        "index.ts": None
                    },
                    "package.json": None,
                    "tsconfig.json": None
                },
                "go": {
                    "main.go": None
                }
            }
        },
        "scripts": {  # 构建脚本目录
            "build_all.sh": None,
            "run_tests.sh": None
        },
        "Makefile": None,  # 顶层构建文件
        "README.md": None  # 项目说明
    }

    def create_node(current_path, node):
        """递归创建目录和文件"""
        if isinstance(node, dict):
            # 创建目录并处理子节点
            Path(current_path).mkdir(exist_ok=True)
            for key, value in node.items():
                create_node(os.path.join(current_path, key), value)
        elif node is None:
            # 创建空文件
            Path(current_path).touch(exist_ok=True)
            parent_dir = os.path.dirname(current_path)
            if not Path(parent_dir).exists():
                Path(parent_dir).mkdir(parents=True, exist_ok=True)
        elif isinstance(node, list):
            # 处理空目录（创建占位文件）
            Path(current_path).mkdir(exist_ok=True)
            (Path(current_path) / ".gitkeep").touch(exist_ok=True)

    # 从根目录开始创建
    create_node(root_dir, structure)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法：python create_project.py <目标目录>")
        sys.exit(1)

    target_dir = sys.argv[1]
    if not Path(target_dir).parent.exists():
        print(f"错误：父目录 {Path(target_dir).parent} 不存在")
        sys.exit(1)

    try:
        create_directory_structure(target_dir)
        print(f"多语言项目结构已生成在 {target_dir}")
        print("包含以下核心目录：")
        print("├── .devcontainer/  # 容器开发环境配置")
        print("├── src/algorithms/ # 多语言算法实现")
        print("└── src/web_api/    # 多语言Web API实现")
    except Exception as e:
        print(f"生成失败：{str(e)}")
        sys.exit(1)