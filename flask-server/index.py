# api/index.py

import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Create Flask app and enable CORS for API routes.
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Use an environment variable for the database URL if provided,
# otherwise default to a local SQLite file.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///cookie.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# EXP Jelly values dictionary
exp_jellies = {
    "Lv.1": {"Base": 14, "Lv.1": 14, "Lv.2": 14, "Lv.3": 15, "Lv.4": 15, "Lv.5": 15},
    "Lv.2": {"Base": 60, "Lv.1": 61, "Lv.2": 62, "Lv.3": 63, "Lv.4": 64, "Lv.5": 66},
    "Lv.3": {"Base": 150, "Lv.1": 152, "Lv.2": 155, "Lv.3": 158, "Lv.4": 161, "Lv.5": 165},
    "Lv.4": {"Base": 400, "Lv.1": 404, "Lv.2": 412, "Lv.3": 420, "Lv.4": 428, "Lv.5": 440},
    "Lv.5": {"Base": 800, "Lv.1": 808, "Lv.2": 824, "Lv.3": 840, "Lv.4": 856, "Lv.5": 880},
    "Lv.6": {"Base": 1600, "Lv.1": 1616, "Lv.2": 1648, "Lv.3": 1680, "Lv.4": 1712, "Lv.5": 1760},
    "Lv.7": {"Base": 3000, "Lv.1": 3030, "Lv.2": 3090, "Lv.3": 3150, "Lv.4": 3210, "Lv.5": 3300},
    "Lv.8": {"Base": 8000, "Lv.1": 8080, "Lv.2": 8240, "Lv.3": 8400, "Lv.4": 8560, "Lv.5": 8800},
}

# Database model for a Cookie
class Cookie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    exp = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, "level": self.level, "exp": self.exp}

# ----------------------------
# API Endpoints
# ----------------------------

# Add a new cookie (POST /api/cookies)
@app.route("/api/cookies", methods=["POST"])
def add_cookie():
    data = request.get_json()
    if not data or 'level' not in data or 'exp' not in data:
        return jsonify({"error": "Invalid request"}), 400

    try:
        level = int(data['level'])
        exp = int(data['exp'])
    except Exception:
        return jsonify({"error": "Level and EXP must be numbers"}), 400

    new_cookie = Cookie(level=level, exp=exp)
    db.session.add(new_cookie)
    db.session.commit()
    return jsonify(new_cookie.to_dict()), 201

# Retrieve all cookies (GET /api/cookies)
@app.route("/api/cookies", methods=["GET"])
def get_cookies():
    cookies = Cookie.query.all()
    return jsonify([cookie.to_dict() for cookie in cookies]), 200

# Delete all cookies (DELETE /api/cookies)
@app.route("/api/cookies", methods=["DELETE"])
def delete_cookies():
    try:
        db.session.query(Cookie).delete()
        db.session.commit()
        return jsonify({"message": "All cookies have been deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Calculate max achievable level for all cookies (POST /api/calc)
@app.route("/api/calc", methods=["POST"])
def calc_max():
    # EXP required per level for levels 2 to 50+ (sample values)
    exp_per_level = {
        2: 60, 3: 80, 4: 100, 5: 120, 6: 150, 7: 180, 8: 220, 9: 270, 10: 330,
        11: 400, 12: 480, 13: 570, 14: 680, 15: 810, 16: 970, 17: 1160, 18: 1380,
        19: 1640, 20: 1950, 21: 2320, 22: 2760, 23: 3280, 24: 3900, 25: 4630,
        26: 5500, 27: 6530, 28: 7750, 29: 9200, 30: 10920, 31: 12960, 32: 15380,
        33: 18250, 34: 21650, 35: 25680, 36: 30460, 37: 36130, 38: 42860,
        39: 50840, 40: 60300, 41: 71520, 42: 84830, 43: 100610, 44: 119330,
        45: 141530, 46: 167860, 47: 199090, 48: 236130, 49: 280160, 50: 332160,
    }
    # Levels 51-60
    for level in range(51, 61):
        exp_per_level[level] = 332160
    # Levels 61-65
    for level in range(61, 66):
        exp_per_level[level] = 342124
    # Levels 66-70
    for level in range(66, 71):
        exp_per_level[level] = 362054
    # Levels 71-80
    for level in range(71, 81):
        exp_per_level[level] = 383777
    # Levels 81-90
    for level in range(81, 91):
        exp_per_level[level] = 405500

    # Build cumulative EXP table; level 1 starts at 0 EXP.
    cumulative_exp = {1: 0}
    for level in range(2, 91):
        cumulative_exp[level] = cumulative_exp[level - 1] + exp_per_level[level]

    # Expected JSON structure:
    # {
    #   "jellies": {
    #       "Lv.1": <quantity>,
    #       "Lv.2": <quantity>,
    #       ...,
    #       "Lv.8": <quantity>
    #   },
    #   "jelly_upgrade": <number between 0 and 5>
    # }
    data = request.get_json()
    if not data or "jellies" not in data or "jelly_upgrade" not in data:
        return jsonify({"error": "Missing jelly data"}), 400

    jellies_input = data["jellies"]
    try:
        jelly_upgrade = int(data["jelly_upgrade"])
    except Exception:
        return jsonify({"error": "Invalid jelly upgrade level"}), 400

    if jelly_upgrade < 0 or jelly_upgrade > 5:
        return jsonify({"error": "Jelly upgrade level must be between 0 and 5"}), 400

    # Map 0 to "Base", 1-5 to "Lv.1" ... "Lv.5"
    upgrade_key = "Base" if jelly_upgrade == 0 else f"Lv.{jelly_upgrade}"

    # Calculate total EXP from all provided jellies
    total_jelly_exp = 0
    for outer in exp_jellies:
        try:
            qty = int(jellies_input.get(outer, 0))
        except Exception:
            qty = 0
        total_jelly_exp += exp_jellies[outer][upgrade_key] * qty

    # Retrieve cookies from the database and calculate each cookie's total EXP.
    cookies = Cookie.query.all()
    if not cookies:
        return jsonify({"max_level": 1, "message": "No cookies in database"}), 200

    cookie_total_exps = []
    for cookie in cookies:
        current_total = cumulative_exp.get(cookie.level, 0) + cookie.exp
        cookie_total_exps.append(current_total)

    current_max_level = max(cookie.level for cookie in cookies)
    achievable_level = current_max_level

    # For each target level (from the highest current level up to 90),
    # check if the pooled jelly EXP can bring all cookies to that level.
    for target_level in range(current_max_level, 91):
        total_needed = sum(
            max(0, cumulative_exp[target_level] - current_exp)
            for current_exp in cookie_total_exps
        )
        if total_needed <= total_jelly_exp:
            achievable_level = target_level
        else:
            break

    return jsonify({"max_level": achievable_level, "jelly_total_exp": total_jelly_exp}), 200

# ----------------------------
# Initialize the database (for local testing)
# ----------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    # Use host="0.0.0.0" for external access and port 5000 (or any available port)
    app.run(host="0.0.0.0", port=5000)
