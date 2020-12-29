import os
from datetime import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    # Request can be used only in some function that curently responds to some request.
    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"))

    app.db = client.microblog  # Microblog is a database I created earlier

    @app.route("/", methods=["GET","POST"])
    def home():
        if request.method == "POST":
            # Content is the name of textarea
            entry_content = request.form.get("content")
            formatted_date = datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert({
                "content": entry_content,
                "date": formatted_date
            })

        entries_with_date = [(entry["content"], entry["date"],datetime.strptime(entry["date"],"%Y-%m-%d").strftime("%b-%d")) 
        for entry in app.db.entries.find({})]

        return render_template("home.html", entries=entries_with_date)

    return app


