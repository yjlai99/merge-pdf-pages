import fitz  # PyMuPDF
import sys
import requests
import math
import os

def download_pdf(url):
    response = requests.get(url)
    local_filename = url.split('/')[-1]
    with open(local_filename, 'wb') as f:
        f.write(response.content)
    return local_filename

def calculate_best_m_n(page_count, original_height, original_width, target_height, target_width):
    best_m = 1
    best_n = page_count
    max_rect_height = 0
    max_rect_width = 0
    for m in range(1, page_count + 1):
        for n in range(1, page_count + 1):
            if m * n < page_count:
                continue
            allowed_rect_height = target_height / m
            allowed_rect_width = target_width / n
            if allowed_rect_height/allowed_rect_width > original_height/original_width:
                rect_height = original_height / original_width * allowed_rect_width
                rect_width = allowed_rect_width
            else:
                rect_height = allowed_rect_height
                rect_width = original_width / original_height * allowed_rect_height
            if rect_height > max_rect_height:
                max_rect_height = rect_height
                max_rect_width = rect_width
                best_m = m
                best_n = n
    target_height, target_width = target_width, target_height
    for m in range(1, page_count + 1):
        for n in range(1, page_count + 1):
            if m * n < page_count:
                continue
            allowed_rect_height = target_height / m
            allowed_rect_width = target_width / n
            if allowed_rect_height/allowed_rect_width > original_height/original_width:
                rect_height = original_height / original_width * allowed_rect_width
                rect_width = allowed_rect_width
            else:
                rect_height = allowed_rect_height
                rect_width = original_width / original_height * allowed_rect_height
            if rect_height > max_rect_height:
                max_rect_height = rect_height
                max_rect_width = rect_width
                best_m = m
                best_n = n
    return best_m, best_n

def calculate_m_n(page_count, origin_ratio, target_ratio):
    closest_diff = float('inf')
    best_m = 1
    best_n = page_count

    for n in range(1, page_count + 1):
        m = max(1, int(page_count / n))
        if m * n < page_count:  # make sure there are enough cells to fit all pages
            m += 1
        # calculate the aspect ratio of the current layout
        layout_ratio = (origin_ratio * n) / m
        # compare the aspect ratio difference
        diff = abs(layout_ratio - target_ratio)
        if diff < closest_diff:
            closest_diff = diff
            best_m = m
            best_n = n

    # try the other way around
    for m in range(1, page_count + 1):
        n = max(1, int(page_count / m))
        if m * n < page_count:  # make sure there are enough cells to fit all pages
            n += 1
        # calculate the aspect ratio of the current layout
        layout_ratio = (origin_ratio * m) / n
        # compare the aspect ratio difference
        diff = abs(1/layout_ratio - 1/target_ratio)
        if diff < closest_diff:
            closest_diff = diff
            best_m = n  # swap m and n
            best_n = m

    return best_m, best_n

def merge_pdf_pages(input_path, output_path=None, m=None, n=None, d1=0, d2=0):
    if input_path.startswith('http'):
        input_pdf_path = download_pdf(input_path)
    else:
        input_pdf_path = input_path

    doc = fitz.open(input_pdf_path)
    new_doc = fitz.open()

    if not output_path:
        base_name = os.path.basename(input_pdf_path)
        output_pdf_path = f"merged_{os.path.splitext(base_name)[0]}.pdf"
    else:
        output_pdf_path = output_path

    original_width = doc[0].rect.width
    original_height = doc[0].rect.height
    if not m or not n:
        # m, n = calculate_m_n(page_count=len(doc), origin_ratio=(original_height/original_width), target_ratio=8.5/11)
        m, n = calculate_best_m_n(len(doc), original_height, original_width, 8.5, 11)
        print(f"Optimal m: {m}, n: {n}")
    rect_width = original_width
    rect_height = original_height
    
    new_page_width = rect_width * n + d2 * (n - 1)
    new_page_height = rect_height * m + d1 * (m - 1)

    page_count = 0
    while page_count < len(doc):
        new_page = new_doc.new_page(-1, width=new_page_width, height=new_page_height)
        for col in range(n):
            for row in range(m):
                if page_count >= len(doc):
                    break
                x0 = col * (rect_width + d2)
                y0 = row * (rect_height + d1)
                x1 = x0 + rect_width
                y1 = y0 + rect_height
                target_rect = fitz.Rect(x0, y0, x1, y1)
                new_page.show_pdf_page(target_rect, doc, page_count)
                page_count += 1
            if page_count >= len(doc):
                break

    new_doc.save(output_pdf_path)
    print(f"Output saved to {output_pdf_path}")

if __name__ == "__main__":
    args = sys.argv[1:]
    input_path = args[0] if len(args) > 0 else None
    output_path = args[1] if len(args) > 1 else None
    m = int(args[2]) if len(args) > 2 else None
    n = int(args[3]) if len(args) > 3 else None
    d1 = float(args[4]) if len(args) > 4 else 0
    d2 = float(args[5]) if len(args) > 5 else 0
    
    if not input_path:
        print("Usage: python merge_pdf_pages.py [input.pdf | input_url] [output.pdf] [m] [n] [d1] [d2]")
    else:
        merge_pdf_pages(input_path, output_path, m, n, d1, d2)
