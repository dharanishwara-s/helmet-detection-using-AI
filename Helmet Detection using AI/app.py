from flask import Flask, render_template, request
import cv2, os
from detector import detect
from db import get_db_connection

app = Flask(__name__)

UPLOAD = "static/uploads"
RESULT = "static/results"
os.makedirs(UPLOAD, exist_ok=True)
os.makedirs(RESULT, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    helmet = 0
    violation = ""
    result = None

    if request.method == "POST":
        file = request.files["image"]
        img_path = os.path.join(UPLOAD, file.filename)
        file.save(img_path)

        img = cv2.imread(img_path)
        img, helmet, violation = detect(img)

        result = os.path.join(RESULT, file.filename)
        cv2.imwrite(result, img)

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO detection_history (image_name, helmet_count, violation_status) VALUES (%s,%s,%s)",
            (file.filename, helmet, violation)
        )
        conn.commit()
        cur.close()
        conn.close()

    return render_template(
        "index.html",
        result=result,
        helmet=helmet,
        violation=violation
    )

@app.route("/history")
def history():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM detection_history ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("history.html", rows=rows)

@app.route("/analytics")
def analytics():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM detection_history WHERE violation_status='NO HELMET'")
    violations = cur.fetchone()[0]
    cur.close()
    conn.close()
    return render_template("analytics.html", violations=violations)

if __name__ == "__main__":
    app.run(debug=True)
