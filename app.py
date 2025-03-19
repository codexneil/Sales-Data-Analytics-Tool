import os
import logging
from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
import pandas as pd
from models import db, SalesRecord  # Import db and SalesRecord from models.py
from config import Config  # Import configuration from config.py
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # No default for production!

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Ensure uploads folder exists
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def process_and_store_csv(filepath):
    try:
        df = pd.read_csv(filepath)
        required_columns = {"Date", "Product", "Quantity Sold", "Unit Price (INR)",
                            "Total Sales (INR)", "Customer Type", "Location"}

        if not required_columns.issubset(df.columns):
            return "Invalid CSV format! Missing required columns."

        # In process_and_store_csv():
        # Rename ALL columns consistently
        df = df.rename(columns={
            "Date": "date",  # Add this line
            "Unit Price (INR)": "unit_price",
            "Total Sales (INR)": "total_sales",
            "Quantity Sold": "quantity_sold",
            "Customer Type": "customer_type",
            "Location": "location"  # Ensure this is included
        })

        # Convert data types
        df["date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["quantity_sold"] = pd.to_numeric(df["quantity_sold"], errors="coerce")
        df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
        df["total_sales"] = pd.to_numeric(df["total_sales"], errors="coerce")
        df.dropna(inplace=True)

        # Bulk insert
        records = df.to_dict('records')
        db.session.bulk_insert_mappings(SalesRecord, records)
        db.session.commit()

        # Cleanup uploaded file
        os.remove(filepath)

        return f"Inserted {len(records)} rows successfully!"

    except Exception as e:
        db.session.rollback()
        logging.error("Error during CSV processing: %s", str(e))
        return f"Error: {str(e)}"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file uploaded", "error")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("No file selected", "error")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            message = process_and_store_csv(filepath)
            flash(message, "success")

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)