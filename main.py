from flask import Flask, render_template, request

from app.InterfaceApi import interfaceApi
from app.Api import api

app = Flask(__name__, template_folder='templates', static_folder='./muestras')
app.register_blueprint(interfaceApi)
app.register_blueprint(api)
#app.config['SECRET_KEY'] = 'tu_clave_secreta'
app.config['WTF_CSRF_ENABLED'] = False

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run( host='0.0.0.0')