import os
from datetime import timedelta
from flask import Flask, jsonify
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Import database and routes
from database import db
from routes.routes import api

def create_app(config_name=None):
    """
    Application factory function
    Allows creating different app configurations
    """
    # Create Flask app instance
    app = Flask(__name__)

    # Configure CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Configuration management
    if config_name == 'production':
        app.config.from_object('config.ProductionConfig')
    elif config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        # Default development configuration
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sredbtooluser:libPwdadmin%40512@localhost:3306/sredb'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ECHO'] = False  # SQL query logging
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-default-secret-key')
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    Marshmallow(app)
    jwt = JWTManager(app)

    # Register Blueprints
    app.register_blueprint(api, url_prefix="/api")

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify(error="Resource not found"), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify(error="Internal server error"), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        """
        Global exception handler
        Logs errors and returns a generic error response
        """
        app.logger.error(f"Unhandled Exception: {e}", exc_info=True)
        return jsonify(
            error="An unexpected error occurred",
            details=str(e)
        ), 500

    return app

# Application context
app = create_app()

# Optional: CLI commands
@app.cli.command("create-tables")
def create_tables():
    """Create database tables"""
    db.create_all()
    print("Tables created successfully.")

@app.cli.command("drop-tables")
def drop_tables():
    """Drop all database tables"""
    db.drop_all()
    print("All tables dropped successfully.")

if __name__ == '__main__':
    # Run the application
    app.run(
        host='0.0.0.0',  # Listen on all available interfaces
        port=5000,       # Specify port
        debug=True       # Enable debug mode for development
    )