from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Пример данных пользователя
current_user = {
    'username': 'Иван Иванов',
    'avatar': 'no-avatar.png',
    'style': 'style.css',
    'is_authenticated': True  # Добавляем для проверки авторизации пользователя
}

# Пример списка топиков
topics = [
    {'id': 1, 'title': 'Топик 1', 'author': 'Автор 1', 'last_update': '2024-05-17'},
    {'id': 2, 'title': 'Топик 2', 'author': 'Автор 2', 'last_update': '2024-05-16'},
    {'id': 3, 'title': 'Топик 3', 'author': 'Автор 3', 'last_update': '2024-05-15'},
]

@app.route('/')
def index():
    user = current_user
    return render_template('forum.html', user=user)

@app.route('/profile')
def profile():
    user = current_user
    return render_template('profile.html', user=user)

@app.route('/contacts')
def contacts():
    user = current_user
    return render_template('contacts.html', user=user)

@app.route('/topics')
def topics_view():
    user = current_user
    return render_template('topics.html', user=user, topics=topics)

@app.route('/topic/<int:topic_id>')
def topic(topic_id):
    topic = next((t for t in topics if t['id'] == topic_id), None)
    user = current_user
    return render_template('topic.html', user=user, topic=topic)

@app.route('/add_topic', methods=['POST'])
def add_topic():
    if current_user['is_authenticated']:
        title = request.form.get('title')
        new_topic = {
            'id': len(topics) + 1,
            'title': title,
            'author': current_user['username'],
            'last_update': '2024-05-17'
        }
        topics.append(new_topic)
    return redirect(url_for('topics_view'))

if __name__ == '__main__':
    app.run(debug=True)
