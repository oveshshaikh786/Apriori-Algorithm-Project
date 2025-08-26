from flask import Flask, request, render_template, redirect, url_for, session
import os, time, math
from werkzeug.utils import secure_filename
from apriori_123456 import apriori, load_transactions, get_maximal_frequent_itemsets

# Explicit folders (your repo already has /templates and /static)
app = Flask(__name__, template_folder="templates", static_folder="static")

# ---- Config ----
app.secret_key = os.environ.get("SECRET_KEY", "dev_only_change_me")

# Detect if running on Render (or similar cloud)
IS_RENDER = os.environ.get("RENDER", "false").lower() == "true"

# Use /tmp on Render, local "uploads/" otherwise
UPLOAD_DIR = "/tmp/uploads" if IS_RENDER else os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_DIR
app.config["ALLOWED_EXTENSIONS"] = {"csv"}
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB file cap

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        support_raw = (request.form.get("min_support") or "").strip()

        if not file or file.filename == "":
            return "No file selected.", 400
        if not allowed_file(file.filename):
            return "Invalid file type. Please upload a CSV.", 400
        if not support_raw:
            return "Please enter a minimum support value.", 400

        # Save upload
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        try:
            # Load transactions first (so we can accept fractional support)
            transactions = load_transactions(filepath)

            # Parse min_support: allow integer OR fraction (0 < s < 1)
            try:
                s_val = float(support_raw)
            except ValueError:
                return "min_support must be a number (e.g., 2 or 0.02).", 400

            if 0 < s_val < 1:
                min_support = math.ceil(s_val * len(transactions))  # convert fraction to count
            else:
                min_support = int(round(s_val))

            # Run Apriori
            start_time = time.time()
            frequent_itemsets = apriori(transactions, min_support)
            maximal_itemsets = get_maximal_frequent_itemsets(frequent_itemsets)
            elapsed_time = time.time() - start_time

            # Pretty-print itemsets (sorted by length)
            sorted_itemsets = sorted(maximal_itemsets, key=lambda x: len(x))
            formatted_itemsets = []
            for itemset in sorted_itemsets:
                # itemset may be set/tuple/list; ensure strings and no empty entries
                items = [str(x) for x in itemset if x is not None and str(x) != ""]
                formatted_itemsets.append("{" + ", ".join(items) + "}")
            formatted_output = "{ " + " ".join(formatted_itemsets) + " }"

            # Store for output page
            session["output"] = formatted_output
            session["total_itemsets"] = len(maximal_itemsets)
            session["elapsed_time"] = elapsed_time
            session["input_file"] = filename
            session["min_support"] = min_support

            return redirect(url_for("output"))

        except Exception as e:
            # Surface the error but keep 500 status for clarity
            return f"Error processing the file: {e}", 500

    return render_template("index.html")

@app.route("/output")
def output():
    output = session.pop("output", None)
    total_itemsets = session.pop("total_itemsets", None)
    elapsed_time = session.pop("elapsed_time", None)
    input_file = session.pop("input_file", None)
    min_support = session.pop("min_support", None)

    if output is None:
        return redirect(url_for("index"))

    return render_template(
        "output.html",
        output=output,
        total_itemsets=total_itemsets,
        elapsed_time=elapsed_time,
        input_file=input_file,
        min_support=min_support,
    )

# Health / favicon helpers (nice for platforms & clean logs)
@app.get("/health")
def health():
    return "ok", 200

@app.get("/favicon.ico")
def favicon():
    return ("", 204)

if __name__ == "__main__":
    # Uses PORT from the environment if present (Render/Railway/Fly/Heroku)
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
