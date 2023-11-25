from flask import Flask
import os

app = Flask(__name__)

@app.route('/bye')
def bye_world():
    return 'Bye, World!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))  # Use port provided by Heroku or default to 5000
    app.run(host='0.0.0.0', port=port)
