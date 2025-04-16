from flask import Flask, render_template
from database import db
from routes.routes import api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sredbtooluser:libPwdadmin%40512@localhost:3306/sredb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # <== Initialize db here

app.register_blueprint(api, url_prefix="/api")

# Route for the UI
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)