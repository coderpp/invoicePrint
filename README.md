# PDF发票合并打印工具

一个Python工具，用于将指定目录下的PDF发票文件合并，并在一张A4纸上排列多张发票（默认4张，可配置）。

## 功能特性

- 📄 自动扫描指定目录下的所有PDF文件
- 🖨️ 将多个PDF发票合并到一个PDF文件中
- 📐 在一张A4纸上排列多张发票（可配置：2、4、6、8张）
- 🎯 自动缩放和居中，保持发票原始宽高比
- 🔄 支持文件正序/倒序排列
- ⚙️ 使用UV管理Python环境

## 安装

### 前置要求

- Python 3.12+
- [UV](https://github.com/astral-sh/uv) - Python包管理器

### 系统依赖

无需额外系统依赖！本工具使用纯Python库实现，不依赖poppler或其他外部工具。

### 安装项目依赖

```bash
# 使用UV安装依赖
uv sync
```

## 使用方法

### 基本用法

```bash
# 合并指定目录下的所有PDF发票，默认每页4张（横向A4）
uv run python main.py /path/to/invoices

# 指定输出文件
uv run python main.py /path/to/invoices -o output.pdf

# 每页排列6张发票（3x2布局，纵向A4）
uv run python main.py /path/to/invoices -n 6

# 倒序排列文件
uv run python main.py /path/to/invoices -r
```

### 命令行参数

| 参数 | 说明 |
|------|------|
| `directory` | 包含PDF发票文件的目录路径（必需） |
| `-o, --output` | 输出PDF文件路径（默认: `merged_invoices.pdf`） |
| `-n, --number` | 每页A4纸排列的发票数量（可选: 2, 4, 6, 8，默认: 4） |
| `-r, --reverse` | 倒序排列文件（默认: 正序） |

### 布局选项

| 选项 | 布局 | 页面方向 |
|------|------|----------|
| `-n 2` | 2行 x 1列 | 纵向A4 |
| `-n 4` | 2行 x 2列 | **横向A4**（默认） |
| `-n 6` | 3行 x 2列 | 纵向A4 |
| `-n 8` | 4行 x 2列 | 纵向A4 |

## 示例

```bash
# 合并当前目录下的所有PDF发票（默认每页4张，横向A4）
uv run python main.py . -o invoices.pdf

# 合并指定目录，每页6张发票，倒序排列
uv run python main.py ~/Documents/invoices -n 6 -r -o merged.pdf
```

## 打包成可执行文件

支持将程序打包成独立可执行文件，无需 Python 环境即可运行。

### 安装打包依赖

```bash
uv sync --extra dev
```

### 执行打包

```bash
# 打包（自动检测平台和架构）
uv run python build.py

# 仅清理构建目录
uv run python build.py --clean
```

打包后的文件位于 `dist/` 目录，文件名格式为：
- macOS: `invoiceprint-macos-arm64` 或 `invoiceprint-macos-x64`
- Windows: `invoiceprint-windows-x64.exe`
- Linux: `invoiceprint-linux-x64` 或 `invoiceprint-linux-arm64`

### 使用打包后的程序

```bash
# macOS/Linux
./dist/invoiceprint-macos-arm64 /path/to/invoices -o output.pdf

# Windows
dist\invoiceprint-windows-x64.exe C:\path\to\invoices -o output.pdf
```

### 多平台自动打包（GitHub Actions）

项目包含 GitHub Actions 工作流，支持自动打包多平台程序：

**触发方式：**
1. **推送标签**：推送 `v*` 格式的标签（如 `v1.0.0`）
2. **手动触发**：在 GitHub 仓库的 Actions 页面手动运行

**支持的平台：**
- macOS ARM64 (Apple Silicon)
- macOS x64 (Intel)
- Linux x64
- Windows x64

**使用方法：**

```bash
# 创建并推送标签，触发自动打包和发布
git tag v1.0.0
git push origin v1.0.0
```

打包完成后，可在 GitHub Releases 页面下载各平台的可执行文件。

## 注意事项

- 每个PDF文件只使用第一页（如果PDF有多页）
- 发票会自动缩放以适应布局，保持原始宽高比
- 输出文件会覆盖同名文件（如果存在）

## 项目结构

```
invoicePrint/
├── main.py                       # 主程序
├── build.py                      # 跨平台打包脚本
├── pyproject.toml                # 项目配置和依赖
├── .gitignore                    # Git忽略文件
├── .github/workflows/build.yml   # GitHub Actions 多平台打包
└── README.md                     # 说明文档
```

## 依赖库

- `pypdf`: PDF文件读取、合并和页面操作

## 许可证

MIT License
