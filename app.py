from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from chatbot import predict_class, get_response
from db import create_user, check_user
from db import create_user, check_user, save_chat, get_chat_history

app = Flask(__name__)
app.secret_key = "shopsmart_secret_key"


@app.route("/")
def home():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("index.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    create_user(username, email, password)

    return "Account created successfully!"


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    user = check_user(username, password)

    if user:
        session["username"] = username
        return redirect(url_for("home"))
    else:
        return "Invalid Username or Password"


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/chat", methods=["POST"])
def chat():

    message = request.json.get("message")

    intents = predict_class(message)
    response = get_response(message, intents)

    username = session["username"]

    save_chat(username, message, response)

    return jsonify({"response": response})
@app.route("/history")
def history():

    if "username" not in session:
        return redirect(url_for("login"))

    chats = get_chat_history(session["username"])

    return render_template(
        "history.html",
        chats=chats
    )


if __name__ == "__main__":
    app.run(debug=True, port=8000)