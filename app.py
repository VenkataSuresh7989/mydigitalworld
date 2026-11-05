import json
import os
from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

# Initialize Flask with template_folder set to current directory (".")
app = Flask(__name__, template_folder=".")

DATA_FILE = "data.json"
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def load_data():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        default_data = {"categories": []}
        save_data(default_data)
        return default_data
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"categories": []}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def save_uploaded_files(files):
    saved_paths = []
    for file in files:
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(filepath):
                filename = f"{base}_{counter}{ext}"
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                counter += 1
            file.save(filepath)
            saved_paths.append(f"/static/uploads/{filename}")
    return saved_paths


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify(load_data())


# --- RESET ALL DATA ENDPOINT ---
@app.route("/api/reset", methods=["POST"])
def reset_data():
    default_data = {"categories": []}
    save_data(default_data)
    return jsonify({"success": True, "message": "All data has been reset."})


# --- CATEGORIES (TABS) ---
@app.route("/api/category", methods=["POST"])
def add_category():
    name = request.json.get("name", "").strip()
    if not name:
        return jsonify({"error": "Category name required"}), 400

    data = load_data()
    cat_id = name.lower().replace(" ", "-") + "-" + os.urandom(2).hex()
    new_cat = {"id": cat_id, "name": name, "items": []}
    data["categories"].append(new_cat)
    save_data(data)
    return jsonify(new_cat)


@app.route("/api/category/<cat_id>", methods=["PUT"])
def edit_category(cat_id):
    name = request.json.get("name", "").strip()
    if not name:
        return jsonify({"error": "Name required"}), 400

    data = load_data()
    for cat in data["categories"]:
        if cat["id"] == cat_id:
            cat["name"] = name
            save_data(data)
            return jsonify(cat)
    return jsonify({"error": "Category not found"}), 404


@app.route("/api/category/<cat_id>", methods=["DELETE"])
def delete_category(cat_id):
    data = load_data()
    data["categories"] = [c for c in data["categories"] if c["id"] != cat_id]
    save_data(data)
    return jsonify({"success": True})


# --- ITEMS ---
@app.route("/api/item", methods=["POST"])
def add_item():
    cat_id = request.form.get("cat_id")
    item_type = request.form.get("type")

    data = load_data()
    target_cat = next((c for c in data["categories"] if c["id"] == cat_id), None)
    if not target_cat:
        return jsonify({"error": "Category not found"}), 404

    new_item = {"type": item_type}

    if item_type == "direct_text":
        new_item["text"] = request.form.get("text", "")
    elif item_type == "key_value":
        new_item["key"] = request.form.get("key", "")
        new_item["value"] = request.form.get("value", "")
    elif item_type == "image_text":
        new_item["text"] = request.form.get("text", "")
        files = request.files.getlist("images")
        new_item["images"] = save_uploaded_files(files)

    target_cat["items"].append(new_item)
    save_data(data)
    return jsonify(target_cat)


@app.route("/api/item/<cat_id>/<int:index>", methods=["POST"])
def update_item(cat_id, index):
    data = load_data()
    target_cat = next((c for c in data["categories"] if c["id"] == cat_id), None)

    if not target_cat or index < 0 or index >= len(target_cat["items"]):
        return jsonify({"error": "Item not found"}), 404

    item = target_cat["items"][index]
    item_type = item.get("type")

    if item_type == "direct_text":
        item["text"] = request.form.get("text", item.get("text", ""))
    elif item_type == "key_value":
        item["key"] = request.form.get("key", item.get("key", ""))
        item["value"] = request.form.get("value", item.get("value", ""))
    elif item_type == "image_text":
        item["text"] = request.form.get("text", item.get("text", ""))
        
        removed_images_json = request.form.get("removed_images", "[]")
        try:
            removed_images = json.loads(removed_images_json)
        except:
            removed_images = []

        current_images = item.get("images", [])
        current_images = [img for img in current_images if img not in removed_images]

        new_files = request.files.getlist("images")
        newly_saved = save_uploaded_files(new_files)
        
        item["images"] = current_images + newly_saved

    save_data(data)
    return jsonify(target_cat)


@app.route("/api/item/<cat_id>/<int:index>", methods=["DELETE"])
def delete_item(cat_id, index):
    data = load_data()
    for cat in data["categories"]:
        if cat["id"] == cat_id:
            if 0 <= index < len(cat["items"]):
                cat["items"].pop(index)
                save_data(data)
                return jsonify(cat)
    return jsonify({"error": "Item not found"}), 404


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)