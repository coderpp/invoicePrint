#!/usr/bin/env python3
"""
PDF发票合并打印工具
将指定目录下的PDF发票文件合并，并在一张A4纸上排列多张发票（默认6张）
"""

import argparse
from pathlib import Path
from typing import List
from io import BytesIO
from pypdf import PdfReader, PdfWriter, PageObject, Transformation


class InvoiceMerger:
    """PDF发票合并器"""
    
    # A4纸张尺寸（点，1点=1/72英寸）
    A4_WIDTH_PORTRAIT = 595.27   # 纵向宽度
    A4_HEIGHT_PORTRAIT = 841.89  # 纵向高度
    
    def __init__(self, invoices_per_page: int = 4):
        """
        初始化合并器
        
        Args:
            invoices_per_page: 每页A4纸排列的发票数量，默认6张（3行2列）
        """
        self.invoices_per_page = invoices_per_page
        self._calculate_layout()
    
    def _calculate_layout(self):
        """计算布局参数"""
        # 根据每页发票数量计算行列数和页面方向
        if self.invoices_per_page == 6:
            self.rows = 3
            self.cols = 2
            self.landscape = False  # 纵向
        elif self.invoices_per_page == 4:
            self.rows = 2
            self.cols = 2
            self.landscape = True   # 横向
        elif self.invoices_per_page == 8:
            self.rows = 4
            self.cols = 2
            self.landscape = False  # 纵向
        elif self.invoices_per_page == 2:
            self.rows = 2
            self.cols = 1
            self.landscape = False  # 纵向
        else:
            # 默认尝试自动计算
            import math
            self.cols = int(math.sqrt(self.invoices_per_page))
            self.rows = (self.invoices_per_page + self.cols - 1) // self.cols
            self.landscape = False
        
        # 设置页面尺寸
        if self.landscape:
            self.page_width = self.A4_HEIGHT_PORTRAIT   # 横向：宽度=纵向高度
            self.page_height = self.A4_WIDTH_PORTRAIT   # 横向：高度=纵向宽度
        else:
            self.page_width = self.A4_WIDTH_PORTRAIT    # 纵向
            self.page_height = self.A4_HEIGHT_PORTRAIT
        
        # 计算每个发票的尺寸（留出边距）
        margin = 10  # 边距（点）
        self.invoice_width = (self.page_width - margin * (self.cols + 1)) / self.cols
        self.invoice_height = (self.page_height - margin * (self.rows + 1)) / self.rows
        self.margin = margin
    
    def merge_pdfs(self, pdf_files: List[Path], output_path: Path):
        """
        合并PDF文件
        
        Args:
            pdf_files: PDF文件路径列表
            output_path: 输出文件路径
        """
        if not pdf_files:
            raise ValueError("没有找到PDF文件")
        
        print(f"找到 {len(pdf_files)} 个PDF文件")
        orientation = "横向" if self.landscape else "纵向"
        print(f"每页排列 {self.invoices_per_page} 张发票 ({self.rows}行 x {self.cols}列, {orientation}A4)")
        
        # 收集所有PDF页面
        all_pages = []
        for pdf_file in pdf_files:
            try:
                reader = PdfReader(str(pdf_file))
                num_pages = len(reader.pages)
                
                if num_pages == 0:
                    print(f"警告: PDF文件 {pdf_file} 没有页面，跳过")
                    continue
                
                # 如果PDF有多页，只取第一页
                if num_pages > 1:
                    print(f"提示: PDF文件 {pdf_file} 有 {num_pages} 页，只使用第一页")
                
                page = reader.pages[0]
                all_pages.append(page)
                
            except Exception as e:
                print(f"警告: 无法处理PDF文件 {pdf_file}: {e}")
                continue
        
        if not all_pages:
            raise ValueError("没有有效的PDF页面")
        
        print(f"总共 {len(all_pages)} 张发票")
        
        # 创建输出PDF
        output_writer = PdfWriter()
        
        # 按每页发票数量分组
        for page_idx in range(0, len(all_pages), self.invoices_per_page):
            page_group = all_pages[page_idx:page_idx + self.invoices_per_page]
            
            # 创建新的A4页面
            merged_page = self._create_merged_page(page_group)
            output_writer.add_page(merged_page)
            print(f"处理第 {page_idx // self.invoices_per_page + 1} 页，包含 {len(page_group)} 张发票...")
        
        # 保存输出文件
        with open(output_path, 'wb') as f:
            output_writer.write(f)
        
        print(f"合并完成！输出文件: {output_path}")
    
    def _create_merged_page(self, pages: List[PageObject]) -> PageObject:
        """
        创建合并后的页面，将多个PDF页面排列在一张A4纸上
        
        Args:
            pages: 要合并的页面列表
            
        Returns:
            合并后的页面对象
        """
        if not pages:
            raise ValueError("页面列表为空")
        
        # 创建空白页面（根据布局选择纵向或横向）
        temp_writer = PdfWriter()
        temp_writer.add_blank_page(width=self.page_width, height=self.page_height)
        temp_pdf = BytesIO()
        temp_writer.write(temp_pdf)
        temp_pdf.seek(0)
        
        temp_reader = PdfReader(temp_pdf)
        merged_page = temp_reader.pages[0]
        
        # 将每个页面叠加到合并页面上
        for idx, page in enumerate(pages):
            # 创建页面的临时PDF，避免修改原始页面
            temp_page_writer = PdfWriter()
            temp_page_writer.add_page(page)
            temp_page_pdf = BytesIO()
            temp_page_writer.write(temp_page_pdf)
            temp_page_pdf.seek(0)
            temp_page_reader = PdfReader(temp_page_pdf)
            page_copy = temp_page_reader.pages[0]
            
            row = idx // self.cols
            col = idx % self.cols
            
            # 计算每个发票区域的位置（PDF坐标系：左下角为原点）
            # 区域左下角的x坐标
            x_left = self.margin + col * (self.invoice_width + self.margin)
            # 区域左下角的y坐标
            # row=0在最上方，row越大y越小
            y_bottom = self.page_height - self.margin - (row + 1) * self.invoice_height - row * self.margin
            
            # 获取原始页面尺寸
            page_width = float(page_copy.mediabox.width)
            page_height = float(page_copy.mediabox.height)
            
            # 计算缩放比例（保持宽高比）
            scale_x = self.invoice_width / page_width
            scale_y = self.invoice_height / page_height
            scale = min(scale_x, scale_y)
            
            scaled_width = page_width * scale
            scaled_height = page_height * scale
            
            # 居中偏移（在区域内居中）
            x_offset = (self.invoice_width - scaled_width) / 2
            y_offset = (self.invoice_height - scaled_height) / 2
            
            # 计算目标位置（页面左下角的目标位置）
            target_x = x_left + x_offset
            target_y = y_bottom + y_offset
            
            # 获取页面当前左下角位置
            page_left = float(page_copy.mediabox.left)
            page_bottom = float(page_copy.mediabox.bottom)
            
            # 计算平移量
            # 我们需要将内容缩放后移动到目标位置
            # 原始内容的原点在 (page_left, page_bottom)
            # 缩放后，原点仍在 (page_left, page_bottom)，但内容尺寸变为原来的 scale 倍
            # 我们需要将缩放后的内容移动，使得左下角在 (target_x, target_y)
            translate_x = target_x - page_left * scale
            translate_y = target_y - page_bottom * scale
            
            # 使用 Transformation 的链式调用方法
            # 注意：先平移到原点，再缩放，最后平移到目标位置
            # 或者：先缩放，再平移
            # Transformation().scale(sx, sy).translate(tx, ty) 相当于：
            # 变换矩阵 = 缩放矩阵 * 平移矩阵
            # 最终效果：先应用缩放，再应用平移
            transform = Transformation().scale(sx=scale, sy=scale).translate(tx=translate_x, ty=translate_y)
            
            # 使用 merge_transformed_page 方法合并页面
            merged_page.merge_transformed_page(page_copy, transform)
        
        return merged_page


def find_pdf_files(directory: Path, reverse: bool = False) -> List[Path]:
    """
    查找目录下的所有PDF文件
    
    Args:
        directory: 目录路径
        reverse: 是否倒序排列
        
    Returns:
        PDF文件路径列表
    """
    pdf_files = list(directory.glob("*.pdf"))
    pdf_files.extend(directory.glob("*.PDF"))
    pdf_files = sorted(pdf_files, reverse=reverse)
    return pdf_files


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="PDF发票合并打印工具 - 将多个PDF发票合并并排列在一张A4纸上"
    )
    parser.add_argument(
        "directory",
        type=str,
        help="包含PDF发票文件的目录路径"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="merged_invoices.pdf",
        help="输出PDF文件路径（默认: merged_invoices.pdf）"
    )
    parser.add_argument(
        "-n", "--number",
        type=int,
        default=4,
        choices=[2, 4, 6, 8],
        help="每页A4纸排列的发票数量（默认: 4，可选: 2, 4, 6, 8）"
    )
    parser.add_argument(
        "-r", "--reverse",
        action="store_true",
        help="倒序排列文件（默认: 正序）"
    )
    
    args = parser.parse_args()
    
    # 检查目录是否存在
    directory = Path(args.directory)
    if not directory.exists():
        print(f"错误: 目录不存在: {directory}")
        return 1
    
    if not directory.is_dir():
        print(f"错误: 不是目录: {directory}")
        return 1
    
    # 查找PDF文件
    pdf_files = find_pdf_files(directory, reverse=args.reverse)
    if not pdf_files:
        print(f"错误: 在目录 {directory} 中没有找到PDF文件")
        return 1
    
    # 显示排序方式
    sort_order = "倒序" if args.reverse else "正序"
    print(f"文件排序: {sort_order}")
    
    # 创建合并器并合并
    try:
        merger = InvoiceMerger(invoices_per_page=args.number)
        output_path = Path(args.output)
        merger.merge_pdfs(pdf_files, output_path)
        return 0
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
