from flask import Flask, render_template
from config import config
from db import db

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config['development'])

    # Initialize the database
    db.init_app(app)

    # Import Blueprints
    from controllers.pages_controller import pages_bp
    from controllers.conversation_controller import conversation_bp
    from controllers.referral_controller import referral_bp
    from controllers.workplan_controller import workplan_bp
    from controllers.user_controller import user_bp
    from controllers.mood_controller import mood_bp
    from controllers.journal_controller import journal_bp
    from controllers.resources_controller import resources_bp
    from controllers.community_controller import community_bp
    from controllers.professional_controller import professional_bp

    # Register Blueprints
    app.register_blueprint(pages_bp)
    app.register_blueprint(conversation_bp, url_prefix="/api")
    app.register_blueprint(referral_bp,    url_prefix="/api")
    app.register_blueprint(workplan_bp,    url_prefix="/api")
    app.register_blueprint(user_bp,        url_prefix="/user")
    app.register_blueprint(mood_bp,        url_prefix="/api")
    app.register_blueprint(journal_bp,     url_prefix="/user")
    app.register_blueprint(resources_bp,   url_prefix="/user")
    app.register_blueprint(community_bp,   url_prefix="/community")
    app.register_blueprint(professional_bp, url_prefix="/professionals")

    # Create database tables
    with app.app_context():
        db.create_all() 

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
