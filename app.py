from flask import Flask, render_template, redirect, session, request
from flask import url_for, abort
from models_data import db, Todo, User
import re
from datetime import datetime


app = Flask(__name__)
app.secret_key = "some password"

# configure the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)


@app.route("/")
def index():
    return render_template ("index.html")

@app.route("/register")
def register():
    return render_template ("form_register.html")

@app.route("/register-success")
def register_success():
    return render_template("register_success.html")    

@app.route("/login")
def login():
    return render_template("form_connection.html")


@app.route("/connection", methods=['POST'])
def connection():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    #if username and password are valid
    if(user and user.check_password(password)):
        
        #create a new session
        session['user_id'] = user.id
        return redirect (url_for('dashboard'))

    return render_template ("form_connection.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        user = User.query.get(session['user_id'])
        list_todo = Todo.query.filter_by(id_user=user.id).all()
        return render_template ("dashboard.html", username = user.username, 
        list_todo = list_todo)
    
    return redirect(url_for('login'))


@app.route("/add-new-todo")
def add_new_todo():
    return render_template('form_new_todo.html')    


@app.route("/new-user", methods=["POST"])
def new_user():

    #store form in data
    data = request.form

    first_name = data.get('first_name', "").strip()
    last_name = data.get('last_name', "").strip()
    email = data.get('email', "").strip()
    username = data.get('username', "").strip()
    password = data.get('password', "")

    #model email
    regex_email = r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$"

    errors = []

    if not first_name:
        errors.append("Prénom requis")
    elif len(first_name) > 30:
        errors.append("Votre prénom ne doit pas dépasser de 30 caractères")

    if not last_name:
        errors.append("Nom famille requis")
    elif len(last_name) > 30:
        errors.append("Votre nom famille ne doit pas dépasser de 30 caractères")

    if not email:
        errors.append("Courriel requis")
    #if email doesn't match with regex_email
    elif not re.fullmatch(regex_email, email):
        errors.append("Courriel non valide")

    if not username:
        errors.append("Nom utilisateur requis")
    elif len(username) > 30:
        errors.append("Votre nom utilisateur ne doit pas dépasser de 30 caractères")

    if not password:
        errors.append("Mot de passe requis")
    elif len(password) < 8 or len(password) > 30:
        errors.append("Votre mot de passe doit contenir entre 8 et 30 caractères")       

    user = User.query.filter_by(username=username).first()
    #if an user is already in db
    if user:
        errors.append("Le nom d'utilisateur existe déjà!")

    #Return form with errors
    if errors:
        return render_template ("form_register.html", errors=errors)
    
    new_user = User(username=username, first_name=first_name, 
    last_name=last_name, email=email)
    new_user.set_password(password)

    # Add a new user to the db
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("register_success"))


@app.route("/todo-new", methods=['POST'])
def todo_new():
    if 'user_id' not in session:
        return render_template('index')

    data = request.form

    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    date = data.get('date', '').strip()
    time = data.get('time','')
    status = data.get('status','').strip()

    errors = []

    if not title:
        errors.append('Titre requis')
    elif len(title) > 50:
        errors.append('Le titre de la tâche ne dois pas dépasser'
         ' de 50 caractères')
    
    if errors:
        return render_template ('dashboard.html', errors=errors)

    #Convert date and time in Objet datetime
    if date:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    else :
        date = None

    if time :
        time = datetime.strptime(time, '%H:%M').time()
    else:
        time = None
          

    new_todo = Todo(id_user=session["user_id"], title=title, description=description, 
                    due_date=date, due_time=time, status=status)
    
    db.session.add(new_todo)
    db.session.commit()
    return render_template('new_todo_success.html')

#Delete a Todo
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id:int):
    if "user_id" not in session:
        return redirect(url_for('login'))
    
    delete_todo = Todo.query.get_or_404(id)

    if delete_todo.id_user != session["user_id"]:
        abort(403)
    try:
        db.session.delete(delete_todo)
        db.session.commit()
        return redirect (url_for('dashboard'))
    except Exception as e:
        return f"ERROR{e}"
    
#Update a Todo
@app.route ("/update/<int:id>" , methods = ["POST", "GET"])
def update(id:int):

    if "user_id" not in session:
        return redirect(url_for('login'))
    
    update_todo = Todo.query.get_or_404(id)

    # id verification
    if update_todo.id_user != session["user_id"]:
        abort(403)

    if request.method == "POST":
        update_todo.title = request.form.get('title', '').strip()
        update_todo.description = request.form.get('description', '').strip()

        date = request.form.get('date')
        time = request.form.get('time')
        
        #Convert date and time in Objet datetime
        if date:
            update_todo.due_date = datetime.strptime(date, '%Y-%m-%d').date()
        else :
            update_todo.due_date = None

        if time:
            update_todo.due_time = datetime.strptime(time, '%H:%M').time()
        else :
            update_todo.due_time = None

        update_todo.status = request.form.get('status', '').strip()

        try :
            db.session.commit()
            return redirect(url_for('dashboard'))
        except Exception as e:
            return f"Error {e}"
        
    else :
        return render_template ('update_todo.html', todo=update_todo)    

            

@app.route("/logout")
def logout():
    # remove the username from the session
    session.pop('user_id', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)