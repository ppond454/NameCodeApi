import json
from flask import Flask, after_this_request, jsonify, request, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import random
import string
from pathlib import Path
from function import convertFunc


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "file"
app.config["MAX_CONTENT_LENGHT"] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(["csv"])

CORS(app)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "msg": "hello"
    }), 200


@app.route("/upload", methods=["POST"])
def upload():

    if request.method == "POST":

        if "file" not in request.files:
            return jsonify({
                "massage": "file is required"
            }), 400

        file = request.files['file']
        if file.filename == "":
            return jsonify({
                "massage": "No file selected for uploading"
            }), 400
        if file and allowed_file(file.filename):
            randomStr = ''.join(random.SystemRandom().choice(
                string.ascii_letters + string.digits) for _ in range(5))
            filename = secure_filename(randomStr)
            file.save(os.path.join(
                app.config["UPLOAD_FOLDER"], filename+".csv"))

            return jsonify({
                "massage": "File uploaded successfully",
                "id": filename
            }), 201
        else:
            return jsonify({'massage': 'Allowed file types is csv'}), 400


@app.route("/download/<path:filename>", methods=["GET"])
def download(filename):
    if request.method == "GET":
        my_file = Path(app.config["UPLOAD_FOLDER"], filename+".csv")
        if my_file.is_file():
            convertFunc(filename)

            @after_this_request
            def delete(res):
                os.remove(my_file)
                return res
            return send_file(my_file, as_attachment=True), 200
        return jsonify({
            "message": "not found"
        }), 404


if __name__ == "__main__":
    app.run(port=4000, debug=True)
