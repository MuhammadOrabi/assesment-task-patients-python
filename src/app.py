#src/app.py

from flask import Flask

from .config import app_config

from .models import db, bcrypt

from .views.PatientView import patient_api as patient_blueprint

from flask_cors import CORS

def create_app(env_name):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(app_config[env_name])


    # initializing bcrypt
    bcrypt.init_app(app)

    db.init_app(app)

    app.register_blueprint(patient_blueprint, url_prefix='/api/patients')
    

    @app.route('/', methods=['GET'])
    def index():
        """
        example endpoint
        """
        return 'Congratulations! Your first endpoint is workin'

    return app