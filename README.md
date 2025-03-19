# Sales Data Analytics Tool

The Sales Data Analytics Tool is a web-based platform that enables businesses to upload, process, and analyze sales data efficiently. It leverages Flask for the backend, Pandas for data processing, SQLAlchemy for database interactions, and MySQL as the storage engine.

## Features

- CSV Upload: Easily upload sales data in CSV format.
- Data Processing: Validate and clean data using Pandas.
- Database Storage: Store processed records in a MySQL database using SQLAlchemy.
- Interactive Reporting: Visualize key metrics and trends (future enhancements include data visualization tools).

## Getting Started

### Prerequisites

- Python 3.8 or higher
- MySQL Server installed and running
- Git

### Installation

1. Clone the Repository
   git clone <repository-url>
   cd <repository-directory>

2. Create and Activate a Virtual Environment
   python -m venv venv
   venv\Scripts\activate

3. Install Dependencies
   pip install -r requirements.txt

4. Configure Environment Variables
   Create a .env file in the project root and add:
   SECRET_KEY=your_generated_secret_key

5. Database Setup
   Update config.py with your MySQL credentials.
   Initialize the database:
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade

6. Run the Application
   flask run

The application should now be running at http://127.0.0.1:5000/.

Usage
Upload CSV: Navigate to the home page and use the upload form to submit your sales data CSV file.
Data Processing: The system validates and processes the CSV, then stores the records in the MySQL database.
Reports: View flash messages confirming successful data insertion. (Enhancements can include interactive dashboards for detailed analytics.)




   

