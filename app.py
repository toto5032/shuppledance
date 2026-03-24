"""
셔플댄스 영상 공유 웹 페이지
Google Drive 폴더의 댄스 영상을 공유하기 위한 웹 애플리케이션
"""
from flask import Flask, render_template
import os

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')
app.secret_key = os.environ.get("SECRET_KEY", "shuffledance-secret")

DRIVE_FOLDER_ID = "17E8j7ntUrXzzK8vWV7l9WSNJsJVGTC0Q"


@app.route("/")
def index():
    """메인 페이지 - 셔플댄스 영상 공유"""
    return render_template("index.html", folder_id=DRIVE_FOLDER_ID)


if __name__ == "__main__":
    app.run(debug=True, port=5010)
