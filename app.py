"""
셔플댄스 영상 공유 웹 페이지
Google Drive 폴더의 댄스 영상을 공유하기 위한 웹 애플리케이션
"""
from flask import Flask, render_template, jsonify
import urllib.request
import re
import os

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')
app.secret_key = os.environ.get("SECRET_KEY", "shuffledance-secret")

DRIVE_FOLDER_ID = "17E8j7ntUrXzzK8vWV7l9WSNJsJVGTC0Q"

# 캐시 (서버 재시작 시 초기화)
_cache = {"videos": None}


def fetch_drive_videos():
    """Google Drive 공개 폴더에서 영상 파일 목록을 가져온다."""
    if _cache["videos"] is not None:
        return _cache["videos"]

    url = f"https://drive.google.com/embeddedfolderview?id={DRIVE_FOLDER_ID}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="replace")

    # flip 엔트리에서 파일 ID와 제목 추출
    entries = re.findall(
        r'<div class="flip-entry"[^>]*id="entry-([^"]+)".*?'
        r'<div class="flip-entry-title">(.*?)</div>',
        html, re.DOTALL
    )

    videos = []
    for file_id, raw_title in entries:
        title = re.sub(r'<[^>]+>', '', raw_title).strip()
        if not title:
            continue
        # 확장자 제거하여 표시 이름 생성
        display = re.sub(r'\.(mp4|mov|avi|mkv|webm)$', '', title, flags=re.IGNORECASE)
        videos.append({
            "id": file_id,
            "title": title,
            "display": display,
            "preview": f"https://drive.google.com/thumbnail?id={file_id}&sz=w400",
            "play": f"https://drive.google.com/file/d/{file_id}/preview",
            "download": f"https://drive.google.com/uc?export=download&id={file_id}",
        })

    _cache["videos"] = videos
    return videos


@app.route("/")
def index():
    videos = fetch_drive_videos()
    return render_template("index.html", videos=videos)


@app.route("/api/refresh")
def refresh():
    _cache["videos"] = None
    videos = fetch_drive_videos()
    return jsonify({"count": len(videos)})


if __name__ == "__main__":
    app.run(debug=True, port=5010)
