from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.services.chatbot import answer_question
from app.services.pdf_processor import process_pdf # Import your PDF processing utility

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["GET", "POST"])
def chat():
    # Ensure the file has been uploaded and processed
    if "filepath" not in session:
        flash("No PDF processed. Please upload one.")
        return redirect(url_for("upload.upload"))

    # Retrieve the filepath of the uploaded PDF
    filepath = session["filepath"]

    # Rebuild the vectorstore from the saved PDF path
    try:
        vectorstore = process_pdf(filepath)
    except Exception as e:
        flash(f"Error processing the PDF: {e}")
        return redirect(url_for("upload.upload"))
    
    # Retrieve chat history (messages)
    messages = session.get("messages", [])

    if request.method == "POST":
        question = request.form["question"]
        try:
            # Get the answer from the chatbot
            answer = answer_question(vectorstore, question)
            
            # Store user query and bot response in the session
            messages.append({"user": question, "bot": answer})
            session["messages"] = messages
        except Exception as e:
            flash(f"Error generating answer: {e}")
    
    # Render the chat page with messages
    return render_template("chat.html", messages=messages)
