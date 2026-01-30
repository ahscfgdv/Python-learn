import os
import fitz  # PyMuPDF

def sanitize_filename(name):
    """清理文件名非法字符"""
    # 替换掉换行符，只保留常见字符
    name = name.replace("\n", "").replace("\r", "")
    return "".join([c for c in name if c.isalnum() or c in (' ', '-', '_', '.', '(', ')')]).strip()

def analyze_and_split(pdf_path, toc_page_index):
    doc = fitz.open(pdf_path)
    
    # 1. 验证页码范围
    if toc_page_index >= len(doc):
        print(f"❌ 错误：你输入的页码 {toc_page_index} 超出了文件总页数 ({len(doc)})。")
        print("⚠️ 记住：程序里 0 代表第1页，1 代表第2页。")
        return

    page = doc[toc_page_index]
    print(f"🔍 正在分析第 {toc_page_index + 1} 页 (程序索引: {toc_page_index})...")
    
    # 获取页面所有文本供参考
    text_sample = page.get_text("text")[:50].replace("\n", " ")
    print(f"   该页开头文字: \"{text_sample}...\" (请确认这是你的目录页)")

    # 2. 提取所有链接
    links = page.get_links()
    print(f"   ---> 共检测到 {len(links)} 个链接对象。")

    chapters = []
    
    for i, link in enumerate(links):
        # 尝试解析目标页码
        dest_page = -1
        
        # 情况A: 直接指向页码 (GOTO)
        if 'page' in link and link['page'] > -1:
            dest_page = link['page']
        
        # 情况B: 命名目的地 (Named Destination)
        elif 'dest' in link:
            try:
                # 尝试解析命名目的地
                dest_info = doc.resolve_names(link['dest'])
                # resolve_names 返回格式通常是 { 'destination_name': (page_num, x, y, ...) }
                # 这里 PyMuPDF 不同版本行为可能略有不同，通常直接取 page
                if dest_info:
                    # 某些版本返回的是页码，某些是复杂对象，这里做个简单处理
                    # 如果 resolve 失败通常不需要处理，fitz 在 get_links 往往已经尽力解析了 page
                    pass 
            except:
                pass
        
        # 如果 fitz 已经智能解析出了 page (通常它会自动把 named 转为 page)，直接用
        if dest_page == -1:
            print(f"      [跳过] 链接 #{i} 无法解析出目标页码 (类型: {link.get('kind')})")
            continue

        # 提取文字标题
        rect = link['from']
        title = page.get_text("text", clip=rect).strip()
        if not title:
            title = f"Chapter_{dest_page+1}"
        
        print(f"      [有效] 链接 #{i}: 指向第 {dest_page+1} 页 -> 标题: {title}")
        chapters.append((dest_page, title))

    # 3. 整理章节
    # 去重并排序
    unique_chapters = sorted(list(set(chapters)), key=lambda x: x[0])
    
    if not unique_chapters:
        print("\n❌ 依然未检测到有效章节。可能原因：")
        print("1. 页码填错了（请看上面的‘该页开头文字’是否对的上）。")
        print("2. 那些蓝字根本不是链接，只是带颜色的文字（有些扫描件或设计图是这样的）。")
        return

    print(f"\n✅ 最终识别出 {len(unique_chapters)} 个可拆分章节，开始拆分...")
    
    output_dir = "./test"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, (start, title) in enumerate(unique_chapters):
        # 确定结束页
        if i + 1 < len(unique_chapters):
            end_page = unique_chapters[i+1][0]
        else:
            end_page = len(doc)
            
        if end_page <= start:
            continue

        # 保存
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=start, to_page=end_page-1)
        
        safe_title = sanitize_filename(title)
        out_name = f"{i+1:02d}_{safe_title}.pdf"
        new_doc.save(os.path.join(output_dir, out_name))
        print(f"   已生成: {out_name}")

    print("\n🎉 完成！")

# ================= 配置区 =================
pdf_file = "C:\\Users\\ljx\\Desktop\\网吧及电竞酒店常见问题及处理方法.pdf"   # <--- 修改文件名
toc_page_num = 3           # <--- 修改这里！(0=封面, 1=第二页, 2=第三页...)

if __name__ == "__main__":
    if os.path.exists(pdf_file):
        analyze_and_split(pdf_file, toc_page_num)
    else:
        print("❌ 找不到文件")