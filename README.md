# Lab 2: Login & To-Do Application

Introduction to Database Systems, Fall 2026, Alexandria National University

## 1. Team

| Name | ID | Contribution |
|------|----|--------------|
| YOUR NAME | YOUR ID | e.g. database schema, back end, README |
| PARTNER NAME (delete row if working alone) | PARTNER ID | e.g. front end, validation, testing |

## 2. Technology

- **Back end:** Python 3.12, Flask, PyMySQL (plain SQL, no ORM), bcrypt, python-dotenv
- **Front end:** HTML (Jinja templates), CSS, JavaScript (no framework)
- **Database:** MySQL, database `registration`, tables `users` and `todos`

## 3. How to run it (from an empty machine)

1. Install **Python 3.12** (tick "Add python.exe to PATH") and **MySQL Server**.
2. Clone the repository and open a terminal in its folder:
   ```
   git clone <repository-url>
   cd <repository-folder>
   ```
3. Create and activate a virtual environment, then install the packages:
   ```
   python -m venv venv
   venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```
   (If PowerShell blocks the script, run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` once.)
4. Build the database. This drops and recreates `registration`:
   ```
   mysql -u root -p -e "source database/schema.sql"
   ```
5. Copy `.env.example` to `.env` and fill in your MySQL user, password and a long random `SESSION_SECRET`:
   ```
   copy .env.example .env
   ```
6. Start the server:
   ```
   python app.py
   ```
7. Open http://127.0.0.1:5000 in a browser.

## 4. Features

| # | Feature | Done |
|---|---------|------|
| R1 | Register (name, email, password, confirm password), duplicate email shows `Email Already Exists`, user is logged in afterwards | yes |
| R2 | Login, same `Invalid email or password` message for unknown email and wrong password, logout | yes |
| R3 | Private list: visitors are redirected to the login page, each user sees only their own to-dos, newest first | yes |
| R4 | Add a to-do | yes |
| R5 | Edit a to-do title | yes |
| R6 | Mark a to-do done / not done | yes |
| R7 | Delete a to-do with an "are you sure?" confirmation | yes |
| R8 | Validation in the browser (JavaScript) and again on the server, with the exact messages | yes |
| R9 | bcrypt password hashes, only the given queries, always with parameters, `user_id` taken from the session | yes |
| R10 | Consistent, responsive interface (works at about 360 px) with feedback and an empty-list message | yes |
| Bonus | (list any you built, or delete this row) | |

## 5. Screenshots

Put four images in the `screenshots/` folder and keep these names (or change the links):

![Register page with error messages](screenshots/01-register-errors.png)
![Login page](screenshots/02-login.png)
![To-do list with one done item](screenshots/03-todo-list.png)
![Phone-sized window](screenshots/04-mobile.png)

## 6. Answers

Write each answer in your own words. Short notes on what to cover are in the comments.

**(a) Why do UPDATE and DELETE contain `AND user_id = ?`, and what changes if you remove it?**

<!-- Where does the to-do id come from? Who can change it? What could another user do?
     Which part of the session is used instead? What happens to the number of changed rows? -->

YOUR ANSWER

**(b) What happens if you insert a to-do for a `user_id` that does not exist, and which constraint of the lecture is that?**

<!-- Try it in MySQL yourself and copy the error number and message you get.
     Name the constraint from the lecture (hint: it is about references between two tables). -->

YOUR ANSWER

**(c) Why do you store a hash and not the password?**

<!-- Think about a leaked database. Why bcrypt and not MD5/SHA? What does "salted" mean here? -->

YOUR ANSWER

**(d) The `name` column is `NOT NULL`: why did you still need your own check for an empty name?**

<!-- What is the difference between NULL and an empty text ''? Which one does NOT NULL refuse? -->

YOUR ANSWER