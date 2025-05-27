# 🧪 Pharmacy System

A simple Python-based desktop application to manage pharmacy inventory and customer data using Excel and CSV files. Built with a Tkinter GUI, this tool allows for registering customers, managing drug stock, and handling prescription entries.

---

## 🚀 Features

* Customer registration, editing, and deletion
* Drug management: add/remove medications with or without prescription
* Prescription tracking per customer
* Excel-based drug database (`drugs.xlsx`)
* CSV-based customer and address databases
* Individual customer logs stored as text files
* Functional Tkinter GUI (login, admin, and user panels)
* Google-style documentation for core modules
* Modular and extensible architecture

---

## 🧠 Tech Stack

* **Python 3.x**
* `pandas` for data handling
* `openpyxl` for Excel integration
* `tkinter` for GUI components
* `csv`, `os`, `datetime` for file and date handling

---

## 🗂 Project Structure

```
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
```

---

## 🧪 Getting Started

### ✅ Prerequisites

Install dependencies:

```bash
pip install -r requirements.txt
```

### ▶️ Run the app

```bash
python main.py
```

Alternative GUI entry points:

```bash
python login.py
# or
python Gui.py
```

You’ll start at the login screen. Current login logic is placeholder-based.

---

## 👥 Team Roles

* **You**: Documentation, GitHub setup, backend support
* Dev 1: Backend logic (customers, drugs)
* Dev 2: Frontend GUI (Tkinter interface)

---

## 📝 Notes

* All data is stored locally—no server required.
* GUI modules (`Gui.py`, `login.py`, `registration.py`) can be merged or swapped as needed.
* Planned improvements:

  * Real authentication
  * More detailed logs and reporting
  * Centralized GUI with routing
  * Exception handling polish

---

## 📌 License

This project is intended for academic and educational use.
