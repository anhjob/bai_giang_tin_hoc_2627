import os

# ⚙️ Cấu hình GitHub
USERNAME = "anhjob"      # 👉 Thay bằng tên tài khoản GitHub của bạn
REPO = "bai_giang_tin_hoc"             # 👉 Thay bằng tên repository của bạn
BRANCH = "main"              # 👉 Nếu dùng branch khác (vd: master) thì sửa lại

# 🗂️ Thư mục gốc chứa file PDF
ROOT_DIR = "."       # Có thể đổi thành "." nếu muốn quét toàn bộ dự án

# 📄 File xuất kết quả
OUTPUT_FILE = "list_pdf_links.md"

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
        grouped_links[class_name].append(f"- [{f}]({url})")

# 💾 Xuất ra file Markdown
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("# 📘 Danh sách bài giảng PDF theo lớp\n\n")
    for class_name in sorted(grouped_links.keys()):
        f.write(f"## 🏫 {class_name}\n\n")
        f.write("\n".join(grouped_links[class_name]))
        f.write("\n\n")

print(f"✅ Đã tạo file: {OUTPUT_FILE}")
