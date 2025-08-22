from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = ''
    if request.method == 'POST':
        try:
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            operation = request.form['operation']
            
            if operation == 'add':
                result = num1 + num2
            elif operation == 'sub':
                result = num1 - num2
            elif operation == 'mul':
                result = num1 * num2
            elif operation == 'div':
                result = "Error: Division by zero" if num2 == 0 else num1 / num2
            else:
                result = "Invalid operation"
        except ValueError:
            result = "Invalid input. Please enter numeric values."
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
