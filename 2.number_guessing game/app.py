from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'number' not in session:
        session['number'] = random.randint(1, 100)
        session['attempts'] = 0
        session['message'] = ""

    if request.method == 'POST':
        guess = request.form.get('guess')
        if guess and guess.isdigit():
            guess = int(guess)
            session['attempts'] += 1
            number = session['number']

            if guess < number:
                session['message'] = "🔻 Too low!"
            elif guess > number:
                session['message'] = "🔺 Too high!"
            else:
                session['message'] = f"🎉 Correct! You guessed it in {session['attempts']} attempts!"
                session['won'] = True
        else:
            session['message'] = "⚠️ Enter a valid number."

    return render_template('index.html',
                           message=session.get('message', ''),
                           attempts=session.get('attempts', 0),
                           won=session.get('won', False))

@app.route('/restart')
def restart():
    session.pop('number', None)
    session.pop('attempts', None)
    session.pop('message', None)
    session.pop('won', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
