🧪 Pharmacy System

A simple Python-based desktop application to manage pharmacy inventory and customer data using Excel and CSV files. Built with a Tkinter GUI, this tool allows for registering customers, managing drug stock, and handling prescription entries.

🚀 Features

Customer registration, editing, and deletion

Drug management: add/remove medications with or without prescription

Prescription tracking per customer

Excel-based drug database (drugs.xlsx)

CSV-based customer and address databases

Individual customer logs stored as text files

Functional Tkinter GUI (login, admin, and user panels)

Google-style documentation for core modules and GUIs

Modular and extensible architecture

🧠 Tech Stack

Python 3.x

pandas for data handling

openpyxl for Excel integration

tkinter for GUI components

csv, os, datetime for file and date handling

📚 Installation

1. Clone the repository

git clone https://github.com/your-username/pharmacy-system.git
cd pharmacy-system

2. Create a virtual environment (recommended)

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

3. Install dependencies

pip install -r requirements.txt

4. Run the application

python main.py

📂 Project Structure

.
├── main.py           # Entry point & GUI controller
├── customers.py      # Customer CRUD logic
├── drugs.py          # Drug CRUD and prescription logic
├── globals.py        # File path constants
├── login.py          # Login screen logic (modular GUI)
├── registration.py   # Registration screen logic (modular GUI)
├── Gui.py            # Combined interface with admin/user workflows
├── customer.csv      # Customer data (CSV)
├── address.csv       # Address data (CSV)
├── drugs.xlsx        # Drug database (Excel)
├── database/         # Per-customer purchase history logs
├── README.md         # Project overview
└── requirements.txt  # Package dependencies

📄 Module Descriptions

login.py

Minimal Tkinter-based login window with placeholder logic for user entry. Includes transition to registration window.

login_window(window) — renders login GUI

set_placeholder(...) — handles entry field UX

Depends on registration.py

registration.py

Simple registration window with email and password fields. Uses similar UX logic to login window.

registration_window(window, back_function) — displays registration panel

set_placeholder(...) — reused for placeholder handling

Gui.py

All-in-one interface with:

login

registration

admin dashboard

user panel

drug shop with add/edit/remove drug options

Functions are grouped logically and leverage shared placeholder/input helpers. Built for later expansion.

👥 Team Roles

You: Documentation, GitHub setup, backend support

Dev 1: Backend logic (customers, drugs)

Dev 2: Frontend GUI (Tkinter interface)

📝 Notes

All data is stored locally—no server required.

GUI modules (Gui.py, login.py, registration.py) can be merged or swapped as needed.

Planned improvements:

Real authentication

More detailed logs and reporting

Centralized GUI with routing

Exception handling polish

📌 License

This project is intended for academic and educational use.