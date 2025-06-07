# FUO Alumni System - Installation Guide

## 1. Prerequisites

Before installing the FUO Alumni System, ensure you have the following prerequisites installed on your system:

- Python 3.8 or higher
- MySQL (via XAMPP or standalone MySQL server)
- Git (optional, for cloning the repository)

## 2. Setting Up Python Environment

### 2.1. Install Python

If you don't have Python installed, download and install it from [python.org](https://www.python.org/downloads/).

> **Note:** Make sure to check "Add Python to PATH" during installation.

### 2.2. Verify Python Installation


Open a command prompt or terminal and run:

```bash
python --version
```

You should see the Python version number. If not, ensure Python is properly installed and added to your PATH.

## 3. Setting Up the Database

### 3.1. Install MySQL

You can install MySQL using one of the following methods:

#### Option 1: Using XAMPP

1. Download and install XAMPP from [apachefriends.org](https://www.apachefriends.org/download.html)
2. Start the XAMPP Control Panel
3. Start the Apache and MySQL services
4. Access phpMyAdmin by clicking the "Admin" button next to MySQL or navigating to [http://localhost/phpmyadmin](http://localhost/phpmyadmin)

#### Option 2: Using MySQL Installer

1. Download and install MySQL from [dev.mysql.com](https://dev.mysql.com/downloads/installer/)
2. Follow the installation wizard instructions
3. Remember the root password you set during installation

### 3.2. Create the Database

#### Using phpMyAdmin (XAMPP):

1. Open phpMyAdmin at [http://localhost/phpmyadmin](http://localhost/phpmyadmin)
2. Click on "New" in the left sidebar
3. Enter "fuo_alumni" as the database name
4. Select "utf8mb4_general_ci" as the collation
5. Click "Create"

#### Using MySQL Command Line:

```sql
mysql -u root -p
CREATE DATABASE fuo_alumni CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
EXIT;
```

## 4. Installing the Application

### 4.1. Download the ZIP file

Download and extract the ZIP file of the project to your desired location.

### 4.2. Create a Virtual Environment (Recommended)

Navigate to the project directory and create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### 4.3. Install Dependencies

With your virtual environment activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

### 4.4. Configure the Application

Create a `.env` file in the root directory of the project with the following content:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URI=mysql://root:your_mysql_password@localhost/fuo_alumni
```

> **Note:** Replace `your_mysql_password` with your actual MySQL password. If you're using XAMPP with default settings, the password might be empty. If no password, the `DATABASE_URI` should look like:
> ```env
> DATABASE_URI=mysql://root@localhost/fuo_alumni
> ```

## 5. Database Setup and Seeding

### 5.1. Import the Database Schema and Seed Data

#### Using phpMyAdmin (XAMPP):

1. Open phpMyAdmin and select the "fuo_alumni" database
2. Click on the "Import" tab
3. Click "Choose File" and select the "seed_alumni_database.sql" file from the project root
4. Click "Go" to import the database structure and seed data

#### Using MySQL Command Line (skip if not using MySQL CLI):

```bash
mysql -u root -p fuo_alumni < seed_alumni_database.sql
```

## 6. Running the Application

### 6.1. Start the Flask Development Server

With your virtual environment activated, run:

```bash
flask run
```

The application should now be running at [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 6.2. Access the Application

Open your web browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 7. Default Login Credentials

### Admin Account:
| Field    | Value                   |
|----------|-------------------------|
| Email    | admin@alumni.com        |
| Password | password123             |

### User Account:
| Field    | Value                   |
|----------|-------------------------|
| Email    | john.doe@example.com    |
| Password | password123             |

## 8. Application Structure

```
fuo-alumni-system/
├── app.py                   # Main application entry point
├── models.py                # Database models
├── requirements.txt         # Python dependencies
├── seed_alumni_database.sql # Database seed file
├── static/                  # Static files (CSS, JS, images)
├── templates/               # HTML templates
├── blueprints/              # Flask blueprints for routes
│   ├── admin.py             # Admin routes
│   ├── alumni.py            # Alumni routes
│   ├── auth.py              # Authentication routes
│   ├── contributions.py     # Contributions routes
│   ├── events.py            # Events routes
│   └── main.py              # Main routes
├── forms/                   # Form definitions
│   ├── admin.py             # Admin forms
│   ├── alumni.py            # Alumni forms
│   ├── auth.py              # Authentication forms
│   ├── contributions.py     # Contributions forms
│   └── events.py            # Events forms
└── utils/                   # Utility functions and helpers
    └── decorators.py        # Custom decorators
```

## 9. Troubleshooting

### Common Issues

#### Database Connection Issues

If you encounter database connection issues:
- Verify that MySQL is running
- Check that the database credentials in the .env file are correct
- Ensure the "fuo_alumni" database exists
- Try connecting to the database using a different client to verify credentials

#### Missing Dependencies

If you encounter errors about missing modules:
```bash
pip install -r requirements.txt
```
Make sure your virtual environment is activated when installing dependencies and running the application.

#### File Upload Issues

If file uploads aren't working:
- Ensure the UPLOAD_FOLDER path exists and is writable
- Check that the folder permissions allow the web server to write to it

#### Port Already in Use

If port 5000 is already in use, you can specify a different port:

```bash
flask run --port=5001
```

## 10. Additional Configuration

### 10.1. Email Configuration

To enable email notifications, add the following to your `.env` file:

```env
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_DEFAULT_SENDER=your_email@example.com
```

**FUO Alumni System Documentation - Created for educational purposes**