from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.services.chatbot import answer_question
from app.services.pdf_processor import load_vectorstore  # Modified import

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["GET", "POST"])
def chat():
    # Ensure vectorstore path exists in session
    if "vectorstore_path" not in session:
        flash("No PDF processed. Please upload one.")
        return redirect(url_for("upload.upload"))

    # Load vectorstore from disk
    try:
        vectorstore = load_vectorstore(session["vectorstore_path"])
    except Exception as e:
        flash(f"Error loading vectorstore: {e}")
        return redirect(url_for("upload.upload"))

    # Retrieve chat history
    messages = session.get("messages", [])

    if request.method == "POST":
        question = request.form["question"]
        try:
            # Get answer from chatbot
            answer = answer_question(vectorstore, question)

            # Save chat to session
            messages.append({"user": question, "bot": answer})
            session["messages"] = messages
        except Exception as e:
            flash(f"Error generating answer: {e}")

    return render_template("chat.html", messages=messages)
