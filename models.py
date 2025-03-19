# models.py
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class SalesRecord(db.Model):
    __tablename__ = 'sales_record'  # Explicit table name (optional)

    # models.py
    class SalesRecord(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        date = db.Column(db.Date)  # Must match CSV's renamed "date" column
        product = db.Column(db.String(255))
        quantity_sold = db.Column(db.Integer)  # Matches "quantity_sold"
        unit_price = db.Column(db.Float)  # Matches "unit_price"
        total_sales = db.Column(db.Float)  # Matches "total_sales"
        customer_type = db.Column(db.String(50))  # Matches "customer_type"
        location = db.Column(db.String(100))  # Matches "location"


    # Optional: Add a string representation
    def __repr__(self):
        return f"<SalesRecord(product='{self.product}', date='{self.date}')>"