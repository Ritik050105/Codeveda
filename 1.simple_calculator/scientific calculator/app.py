from flask import Flask, render_template, request, session, redirect, url_for
import math

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session

def calculate_expression(expr):
    try:
        # Allow safe eval for math functions
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        allowed_names['abs'] = abs
        result = eval(expr, {"__builtins__": None}, allowed_names)
        return result
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception:
        return "Invalid Expression"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        expression = request.form.get('expression', '')
        result = calculate_expression(expression)
        session['history'].append(f"{expression} = {result}")
        session.modified = True

    return render_template("index.html", result=result, history=session['history'])

@app.route('/clear')
def clear():
    session['history'] = []
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
