from flask import Flask, render_template, request, send_file
import io

app = Flask(__name__)

def is_safe(board, row, col, n):
    for i in range(row):
        if board[i][col]:
            return False
    for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
        if board[i][j]:
            return False
    for i, j in zip(range(row-1, -1, -1), range(col+1, n)):
        if board[i][j]:
            return False
    return True

def solve_n_queens(board, row, n, solutions):
    if row == n:
        solutions.append([r[:] for r in board])
        return
    for col in range(n):
        if is_safe(board, row, col, n):
            board[row][col] = 1
            solve_n_queens(board, row + 1, n, solutions)
            board[row][col] = 0

def get_solutions(n):
    board = [[0 for _ in range(n)] for _ in range(n)]
    solutions = []
    solve_n_queens(board, 0, n, solutions)
    return solutions

@app.route('/', methods=['GET', 'POST'])
def index():
    solutions = []
    n = 4
    if request.method == 'POST':
        try:
            n = int(request.form.get('n'))
            if 1 <= n <= 12:
                solutions = get_solutions(n)
        except ValueError:
            pass
    return render_template('index.html', solutions=solutions, n=n)

@app.route('/download')
def download():
    n = int(request.args.get("n", 4))
    solutions = get_solutions(n)
    output = io.StringIO()
    output.write(f"{len(solutions)} solutions for {n}-Queens:\n\n")
    for idx, board in enumerate(solutions, 1):
        output.write(f"Solution {idx}:\n")
        for row in board:
            output.write(''.join('Q' if cell else '.' for cell in row) + '\n')
        output.write('\n')
    output.seek(0)
    return send_file(io.BytesIO(output.read().encode()), mimetype='text/plain',
                     download_name=f'{n}_queens_solutions.txt', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
