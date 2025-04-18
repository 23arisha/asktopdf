import os
import uuid
import hashlib
from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from werkzeug.utils import secure_filename
from app.services.pdf_processor import process_pdf

upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = "app/static/uploads"
VECTORSTORE_FOLDER = "app/static/vectorstores"

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
            # Ensure upload directories exist
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            os.makedirs(VECTORSTORE_FOLDER, exist_ok=True)

            # Save PDF to upload folder
            filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            try:
                # Create a unique vectorstore path (e.g. based on hash of filename)
                vectorstore_id = hashlib.md5(filename.encode()).hexdigest()
                vectorstore_path = os.path.join(VECTORSTORE_FOLDER, vectorstore_id)

                # Process PDF and save vectorstore
                process_pdf(filepath, persist_dir=vectorstore_path)

                # Clear the session to start fresh for a new upload
                session.clear()

                # Save paths to session
                session["filepath"] = filepath
                session["vectorstore_path"] = vectorstore_path
                session["messages"] = []

                return redirect(url_for("chat.chat"))
            except Exception as e:
                flash(f"Error processing PDF: {e}")
                return redirect(request.url)
        else:
            flash("Unsupported file type. Please upload a PDF.")
            return redirect(request.url)
    
    return render_template("upload.html")
