from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    user = {
        'username': 'Иван Иванов',
        'avatar': 'no-avatar.png',
        'style': 'style.css'
    }
    return render_template('index.html', user=user)

@app.route('/profile')
def profile():
    user = {
        'username': 'Иван Иванов',
        'style': 'style.css',
        'followers': 100,
        'subscribes': 150,
        'is_followed': False,  # Подставьте значение в зависимости от логики вашего приложения
        'avatar': 'no-avatar.png',
        'is_current_user': False,  # Добавлено для проверки текущего пользователя
        'email': 'ivan@example.com',  # Электронная почта пользователя
        'registration_date': '2024-05-21',  # Дата регистрации
        'tag': 'Programmer'  # Тег пользователя
    }
    return render_template('profile.html', user=user)

@app.route('/contacts')
def contacts():
    user = {   
        'username': 'Иван Иванов',
        'avatar': 'no-avatar.png',
        'style': 'style.css',
        'email': 'ivan@example.com',
        'phone': '+1234567890',
        'tg': '@ivan_kalinin'
        }
    return render_template('contacts.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
