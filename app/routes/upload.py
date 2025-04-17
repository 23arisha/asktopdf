import os
import uuid
from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from werkzeug.utils import secure_filename

upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = "app/static/uploads"

@upload_bp.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "pdf_file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        
        file = request.files["pdf_file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        
        if file and file.filename.lower().endswith(".pdf"):
            # Ensure upload directory exists
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            try:
                session["filepath"] = filepath
                return redirect(url_for("chat.chat"))
            except Exception as e:
                flash(f"Error processing PDF: {e}")
                return redirect(request.url)
        else:
            flash("Unsupported file type. Please upload a PDF.")
            return redirect(request.url)
    
    return render_template("upload.html")
