# /run.py
import os

from src.app import create_app

def main():
    env_name = os.getenv('FLASK_ENV')
    app = create_app(env_name)
    
    # run app
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()

