# TODO App - Flask

A simple web application for managing daily tasks built
with **Python** and **Flask**.
Users can create, update, and delete tasks while managing
their personal todo silt through an autehnticated dashboard.

## Features

- User authentication (login / logout)
- Create new tasks
- Update existing tasks
- Delete tasks
- Assign a due date and time to tasks
- Task status management (PENDING / Done)
- Server-side form validation
- Route protection (users can only manage theri own tasks)

## Technologies Used

### Backend
- Python
- Flask
- SQLAlchemy
- SQLite

### Frontend

- HTML
- JavaScript
- Jinja2 Templates
- Bootstrap

### Tools
- Git
- GitHub

## Project Structure

```
.
├── app.py
├── create_db.py
├── models_data.py
├── README.md
├── requirements.txt
├── static
│   └── js
│       ├── script_add_modif_todo.js
│       └── script_register.js
└── templates
    ├── base.html
    ├── dashboard.html
    ├── form_connection.html
    ├── form_new_todo.html
    ├── form_register.html
    ├── index.html
    ├── new_todo_success.html
    ├── partials
    │   └── _error_form.html
    ├── register_success.html
    ├── todo_details.html
    └── update_todo.html
```

## Installation

1. ### Clone the repository
git clone https://github.com/oscarsilvam/Todo-app.git
cd todo-app

2. ### Create a virtual environment
python -m venv venv

3. ### Activate the virtual environment
source venv/bin/activate

4. ### Install dependencies
pip install -r requirements.txt

5. ### Create the database
python create_db.py

6. ### Run the application
python app.py

## Security
This application includes several basic security mechanisms:

- Session verification for protected routes
- Authorization checks to ensure users can only modify their own tasks.
- Server-side validation for form inputs

## Author

Oscar Silva

