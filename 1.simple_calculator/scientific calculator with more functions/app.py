from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def calculate_expression(expr):
    try:
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        allowed_names.update({'abs': abs, 'pi': math.pi, 'e': math.e})
        allowed_names['factorial'] = math.factorial
        allowed_names['ln'] = math.log
        if 'x' in expr:
            return expr
        return eval(expr, {"__builtins__": None}, allowed_names)
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception:
        return "Invalid Expression"

def plot_expression(expr):
    x = np.linspace(-10, 10, 400)
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    allowed_names.update({'abs': abs, 'pi': math.pi, 'e': math.e, 'x': x})
    allowed_names['factorial'] = np.vectorize(math.factorial)
    allowed_names['ln'] = np.log
    try:
        y = eval(expr, {"__builtins__": None}, allowed_names)
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_title(f"y = {expr}")
        filename = f"{uuid.uuid4().hex}.png"
        filepath = os.path.join("plots", filename)
        fig.savefig(filepath)
        plt.close(fig)
        return filename
    except Exception:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    plot_filename = None
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        expression = request.form.get('expression', '')
        result = calculate_expression(expression)
        if isinstance(result, str) and result == expression and 'x' in expression:
            plot_filename = plot_expression(expression)
            session['history'].append(f"Plot: y = {expression}")
        else:
            session['history'].append(f"{expression} = {result}")
        session.modified = True

    return render_template("index.html", result=result, history=session['history'], plot=plot_filename)

@app.route('/clear')
def clear():
    session['history'] = []
    return redirect(url_for('index'))

@app.route('/plots/<filename>')
def get_plot(filename):
    return send_from_directory('plots', filename)

if __name__ == '__main__':
    app.run(debug=True)
