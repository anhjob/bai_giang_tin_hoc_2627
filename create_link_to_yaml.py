import requests
import yaml
from datetime import datetime

# ⚙️ Cấu hình GitHub
USERNAME = "anhjob"
REPO = "bai_giang_tin_hoc"
BRANCH = "main"

# 📄 File xuất kết quả
OUTPUT_FILE = "list_pdf_links.yaml"

# 🔗 API GitHub
base_api = f"https://api.github.com/repos/{USERNAME}/{REPO}"

# 🔧 Tạo URL raw GitHub
def make_github_url_download(filepath):
    filepath = filepath.replace("\\", "/")
    return f"https://raw.githubusercontent.com/{USERNAME}/{REPO}/{BRANCH}/{filepath}"

# Tạo URL xem trên GitHub
def make_github_url_view(filepath):
    filepath = filepath.replace("\\", "/")
    return f"https://github.com/{USERNAME}/{REPO}/blob/{BRANCH}/{filepath}"

# 📅 Lấy ngày cập nhật cuối
def get_last_update(path):
    url = f"{base_api}/commits?path={path}&per_page=1"
    res = requests.get(url)
    res.raise_for_status()
    commits = res.json()

    if not commits:
        return None

    date_str = commits[0]["commit"]["committer"]["date"]
    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    return dt.strftime("%Y-%m-%d")

# 🗂️ Quét toàn bộ repo (đệ quy)
def scan_folder(folder):
    url = f"{base_api}/contents/{folder}"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()

# 📌 Duyệt theo thư mục K6/K7/K8/K9
def scan_all_grades():
    url = f"{base_api}/contents"
    res = requests.get(url)
    res.raise_for_status()

    root_items = res.json()
    yaml_data = {}

    for item in root_items:
        if item["type"] == "dir" and item["name"].startswith("K"):  
            grade = item["name"]
            yaml_data[grade] = []

            # Quét thư mục con
            pdfs = scan_pdfs_in_folder(grade)
            yaml_data[grade].extend(pdfs)

    return yaml_data

# 📝 Lấy PDF trong một thư mục (đệ quy)
def scan_pdfs_in_folder(folder):
    items = scan_folder(folder)
    pdf_list = []

    for item in items:
        item_path = f"{folder}/{item['name']}"

        if item["type"] == "file" and item["name"].lower().endswith(".pdf"):
            updated = get_last_update(item_path)

            pdf_list.append({
                "ten": item["name"],
                "ngay_cap_nhat": updated,
                "xem": make_github_url_view(item_path),
                "tai": make_github_url_download(item_path)
            })

        elif item["type"] == "dir":
            pdf_list.extend(scan_pdfs_in_folder(item_path))

    return pdf_list


# ===== THỰC THI =====
yaml_output = scan_all_grades()

# ===== GHI FILE YAML =====
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    yaml.dump(yaml_output, f, allow_unicode=True, sort_keys=False)

print("✅ Đã tạo file", OUTPUT_FILE)