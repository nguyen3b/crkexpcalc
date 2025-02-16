from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql  import text

db = SQLAlchemy() # db will be the name for all SQLAlchemy commmands

app = Flask(__name__)

db_name = 'cookie.db' #change string to name of the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQKALCHEMY_TACK_MODIFICATIONS'] = True

#intitalize the app with flask-sqlalchemy
db.init_app(app)


@app.route("/")
def cookie():
    try: 
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1> it works </h1>'
    except Exception as e:
        error_text = "<p> the error:<br>" + str(e) + "</p>"
        had = '<h1> SOmeing is broken </h1>'
        return had + error_text

if __name__ == "__main__":
    app.run(debug=True)

