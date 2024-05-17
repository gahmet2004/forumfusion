from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    user = {
        'username': 'Иван Иванов',
        'avatar': 'no-avatar.png'
    }
    return render_template('index.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
