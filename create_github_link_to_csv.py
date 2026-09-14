import os
from datetime import datetime

# ⚙️ Cấu hình GitHub
USERNAME = "anhjob"      # 👉 Thay bằng tên tài khoản GitHub của bạn
REPO = "bai_giang_tin_hoc"             # 👉 Thay bằng tên repository của bạn
BRANCH = "main"              # 👉 Nếu dùng branch khác (vd: master) thì sửa lại

# 🗂️ Thư mục gốc chứa bài giảng
ROOT_DIR = "."       # có thể đổi thành "." để quét toàn bộ dự án
OUTPUT_FILE = "list_pdf_links.csv"