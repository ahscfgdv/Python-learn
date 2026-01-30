from pypdf import PdfReader, PdfWriter

def split_pdf_by_bookmarks(path):
    reader = PdfReader(path)
    # 获取大纲（书签）
    outline = reader.outline
    
    # 简单的遍历，仅处理一级目录
    for i in range(len(outline)):
        item = outline[i]
        
        # 确保是书签项而不是列表（处理嵌套情况需要递归，此处为简易版）
        if isinstance(item, list):
            continue
            
        title = item.title
        start_page = reader.get_destination_page_number(item)
        
        # 确定结束页码
        if i + 1 < len(outline) and not isinstance(outline[i+1], list):
            end_page = reader.get_destination_page_number(outline[i+1])
        else:
            # 如果是最后一个章节，或者是复杂嵌套结构，这里简化为取到文件末尾
            # 实际生产中需要更复杂的逻辑来判断下一章的起始页
            end_page = len(reader.pages)

        writer = PdfWriter()
        for page_num in range(start_page, end_page):
            writer.add_page(reader.pages[page_num])
            
        # 保存文件，文件名需过滤非法字符
        safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).strip()
        with open(f"{safe_title}.pdf", "wb") as output_pdf:
            writer.write(output_pdf)
        print(f"已生成: {safe_title}.pdf")

# 使用示例
split_pdf_by_bookmarks("C:\\Users\\ljx\\Desktop\\网吧及电竞酒店常见问题及处理方法.pdf")