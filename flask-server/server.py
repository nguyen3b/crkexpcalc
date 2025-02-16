from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cookie.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cookie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    exp = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "level": self.level,
            "exp": self.exp,
        }

@app.route("/api/cookies", methods=["POST"])
def add_cookies():
    print("Received POST request to /api/cookies")
    data = request.get_json()

    if not data or 'level' not in data or 'exp' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    new_cookie = Cookie(level=data['level'], exp=data['exp'])
    db.session.add(new_cookie)
    db.session.commit()

    return jsonify(new_cookie.to_dict()), 201

@app.route("/api/cookies", methods=["GET"])
def get_cookies():
    print("Received GET request to /api/cookies")
    cookies = Cookie.query.all()
    cookies_list = [cookie.to_dict() for cookie in cookies]
    return jsonify(cookies_list), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
