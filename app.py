
from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy			# instead of mysqlconnection
from sqlalchemy.sql import func                         # ADDED THIS LINE FOR DEFAULT TIMESTAMP
from flask_migrate import Migrate			# this is new
app = Flask(__name__)
# configurations to tell our app about the database we'll be connecting to
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///$Duber.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# an instance of the ORM
db = SQLAlchemy(app)
# a tool for allowing migrations/creation of tables
migrate = Migrate(app, db)

app.secret_key = "secretstuff"


#### ADDING THIS CLASS ####
# the db.Model in parentheses tells SQLAlchemy that this class represents a table in our database



class User(db.Model):	
    # __tablename__ = "users"    # optional		
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password = db.Column(db.String(255))
    rides = db.relationship("Ride", backref="User")
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())



class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_point = db.Column(db.String(255))
    end_point = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

# routes go here...





@app.route('/')
def index():

    return render_template('index.html')

@app.route('/create_user', methods=['POST'])
def create_user():
    # Do Validation Here

    fname = request.form['first_name']
    lname = request.form['last_name']
    email = request.form['email']
    password = request.form['password']

    # If Valid, add to DB
    new_user = User(first_name = fname, last_name = lname, email = email, password = password)
    db.session.add(new_user)
    db.session.commit()
    
    this_user = User.query.filter_by(email = email).all()
    session['user_id'] = this_user[0].id
    return redirect('/dashboard')


@app.route('/login')
def login():

    # DO validation here
    email = request.form['email']
    password = request.form['password']

    this_user = User.query.filter_by(email = email).all()

    if this_user:
        if this_user.password == password:
            session['user_id'] = this_user[0].id
            return redirect('/dashboard')
        else:
            flash('Incorrect Password')
    else:
        return redirect('/')


    

@app.route('/dashboard')
def dashboard():
    rides = Ride.query.all()
    return render_template('dashboard.html', rides = rides)


@app.route('/create_ride', methods=["POST"])
def create_ride():
    rto = request.form['ride_to']
    rfrom = request.form['ride_from']
    if session['user_id']:
        uid = session['user_id']
    else:
        uid = 0
    new_ride = Ride(start_point = rfrom, end_point= rto, user_id = uid)
    db.session.add(new_ride)
    db.session.commit()
    return redirect('/dashboard')




if __name__ == "__main__":
    app.run(debug=True)










































