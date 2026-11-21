"""Thu thap metadata (giay phep, so sao, ngon ngu) cua 3 du an tu GitHub API.

Cach chay:
    python src/fetch_repo_metadata.py
Ket qua: results/repo_stats.csv
Luu y: GitHub API khong can dang nhap nhung bi gioi han so luot goi.
"""
import csv
import json
import os
import urllib.request
from datetime import date

REPOS = {
    "React": "facebook/react",
    "TensorFlow": "tensorflow/tensorflow",
    "GIMP": "GNOME/gimp",
}
OUT = os.path.join(os.path.dirname(__file__), "..", "results", "repo_stats.csv")


def fetch(full_name):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{full_name}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "license-study"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def main():
    rows = []
    for name, full in REPOS.items():
        try:
            d = fetch(full)
            lic = (d.get("license") or {}).get("spdx_id", "N/A")
            rows.append([name, full, lic, d.get("stargazers_count"), d.get("forks_count"),
                         d.get("language"), date.today().isoformat()])
        except Exception as e:  # noqa: BLE001
            print(f"Loi khi lay {full}: {e}")
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["project", "repo", "license_spdx", "stars", "forks", "language", "accessed"])
        wr.writerows(rows)
    print(f"Da ghi {len(rows)} dong vao {os.path.abspath(OUT)}")


if __name__ == "__main__":
    main()
