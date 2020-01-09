from app import app
import os 

flask_host = os.getenv('FLASK_HOST', '127.0.0.1')
flask_port = os.getenv('FLASK_PORT', 8080)


app.run(host=flask_host, port=flask_port, threaded=True)