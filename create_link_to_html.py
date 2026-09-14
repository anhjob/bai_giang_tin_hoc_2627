import os
from datetime import datetime

# ⚙️ Cấu hình GitHub
USERNAME = "anhjob"      # 👉 Thay bằng tên tài khoản GitHub của bạn
REPO = "bai_giang_tin_hoc"             # 👉 Thay bằng tên repository của bạn
BRANCH = "main"              # 👉 Nếu dùng branch khác (vd: master) thì sửa lại

# 🗂️ Thư mục gốc chứa bài giảng
ROOT_DIR = "."       # có thể đổi thành "." để quét toàn bộ dự án
OUTPUT_FILE = "list_pdf_links.html"

# 📘 Hàm tạo link trực tiếp đến GitHub
def make_github_url(filepath):
    filepath = filepath.replace("\\", "/")
    return f"https://raw.githubusercontent.com/{USERNAME}/{REPO}/{BRANCH}/{filepath}"

# 🧩 Gom nhóm file PDF theo thư mục lớp
grouped_links = {}

for root, _, files in os.walk(ROOT_DIR):
    pdf_files = [f for f in files if f.lower().endswith(".pdf")]
    if not pdf_files:
        continue

    # Lấy tên thư mục (ví dụ: K6, K7, K8)
    class_name = os.path.basename(root)
    if class_name not in grouped_links:
        grouped_links[class_name] = []

    for f in sorted(pdf_files):
        rel_path = os.path.join(root, f)
        url = make_github_url(rel_path)
        mtime = os.path.getmtime(rel_path)
        date_str = datetime.fromtimestamp(mtime).strftime("%d/%m/%Y")
        grouped_links[class_name].append((f, url, date_str))

# 🧱 Tạo HTML
html = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Danh sách bài giảng PDF</title>
<style>
    body { font-family: "Segoe UI", sans-serif; margin: 40px; background: #f9f9f9; }
    h1 { color: #0078D7; }
    h2 { margin-top: 30px; color: #444; }
    table { border-collapse: collapse; width: 100%; margin-top: 10px; background: white; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
    th { background: #0078D7; color: white; }
    a.button { text-decoration: none; background: #0078D7; color: white; padding: 6px 12px; border-radius: 6px; }
    a.button:hover { background: #005A9E; }
</style>
</head>
<body>
<h1>📘 Danh sách bài giảng PDF theo lớp</h1>
"""

for class_name in sorted(grouped_links.keys()):
    html += f"<h2>🏫 {class_name}</h2>\n"
    html += "<table>\n<tr><th>Tên bài giảng</th><th>Ngày cập nhật</th><th>Tải về</th></tr>\n"
    for name, url, date in grouped_links[class_name]:
        html += f"<tr><td>{name}</td><td>{date}</td><td><a class='button' href='{url}' target='_blank'>Download</a></td></tr>\n"
    html += "</table>\n"

html += """
</body>
</html>
"""

# 💾 Ghi ra file HTML
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Đã tạo file HTML: {OUTPUT_FILE}")
