# PDF发票合并打印工具

一个Python工具，用于将指定目录下的PDF发票文件合并，并在一张A4纸上排列多张发票（默认6张，可配置）。

## 功能特性

- 📄 自动扫描指定目录下的所有PDF文件
- 🖨️ 将多个PDF发票合并到一个PDF文件中
- 📐 在一张A4纸上排列多张发票（可配置：2、4、6、9张）
- 🎯 自动缩放和居中，保持发票原始宽高比
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
# 合并指定目录下的所有PDF发票，默认每页6张
uv run python main.py /path/to/invoices

# 指定输出文件
uv run python main.py /path/to/invoices -o output.pdf

# 每页排列4张发票（2x2布局）
uv run python main.py /path/to/invoices -n 4

# 每页排列9张发票（3x3布局）
uv run python main.py /path/to/invoices -n 9
```

### 命令行参数

- `directory`: 包含PDF发票文件的目录路径（必需）
- `-o, --output`: 输出PDF文件路径（默认: `merged_invoices.pdf`）
- `-n, --number`: 每页A4纸排列的发票数量（可选: 2, 4, 6, 9，默认: 6）

### 布局选项

- `-n 2`: 1行 x 2列
- `-n 4`: 2行 x 2列
- `-n 6`: 2行 x 3列（默认）
- `-n 9`: 3行 x 3列

## 示例

```bash
# 合并当前目录下的所有PDF发票
uv run python main.py . -o invoices.pdf

# 合并指定目录，每页4张发票
uv run python main.py ~/Documents/invoices -n 4 -o merged.pdf
```

## 注意事项

- 每个PDF文件只使用第一页（如果PDF有多页）
- 发票会自动缩放以适应布局，保持原始宽高比
- 输出文件会覆盖同名文件（如果存在）

## 项目结构

```
invoicePrint/
├── main.py           # 主程序
├── pyproject.toml    # 项目配置和依赖
└── README.md         # 说明文档
```

## 依赖库

- `pypdf`: PDF文件读取、合并和页面操作

## 许可证

MIT License

