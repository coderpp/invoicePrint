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

## 注意事项

- 每个PDF文件只使用第一页（如果PDF有多页）
- 发票会自动缩放以适应布局，保持原始宽高比
- 输出文件会覆盖同名文件（如果存在）

## 项目结构

```
invoicePrint/
├── main.py           # 主程序
├── pyproject.toml    # 项目配置和依赖
├── .gitignore        # Git忽略文件
└── README.md         # 说明文档
```

## 依赖库

- `pypdf`: PDF文件读取、合并和页面操作

## 许可证

MIT License
