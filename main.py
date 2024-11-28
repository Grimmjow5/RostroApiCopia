from flask import Flask, render_template, request

from app.InterfaceApi import interfaceApi

app = Flask(__name__, template_folder='templates')
app.register_blueprint(interfaceApi)
#app.config['SECRET_KEY'] = 'tu_clave_secreta'
app.config['WTF_CSRF_ENABLED'] = False

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')