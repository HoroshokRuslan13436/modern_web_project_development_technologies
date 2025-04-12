import matplotlib
from flask import Flask, render_template, request, flash, session, url_for, redirect
import sympy
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import psycopg2

matplotlib.use('Agg')

app = Flask(__name__, template_folder=r'C:\Users\User\PycharmProjects\pythonProject8\templates')

DATABASE_URI = 'dbname=TaskWeb user=postgres password=новий_пароль host=localhost port=5432'
app.secret_key = '3131312'


def create_tables():
    connection = psycopg2.connect(DATABASE_URI)
    cursor = connection.cursor()
    try:
        # Create the user table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS "user" (
            id SERIAL PRIMARY KEY,
            username VARCHAR(80) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password VARCHAR(80) NOT NULL
        )
        """)

        # Create the solution table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS solution (
            id SERIAL PRIMARY KEY,
            equation VARCHAR(255) NOT NULL,
            user_id INTEGER REFERENCES "user" (id) NOT NULL
        )
        """)

        connection.commit()
        print("Tables created successfully.")
    except psycopg2.Error as e:
        print(f"Error creating tables: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()


def save_solution_to_database(equation, solution, method, username):
    connection = psycopg2.connect(DATABASE_URI)
    cursor = connection.cursor()

    try:
        # Get user ID based on email
        cursor.execute("SELECT id FROM \"user\" WHERE username = %s", (username,))
        user_id = cursor.fetchone()[0]

        cursor.execute("INSERT INTO solution (equation, solution, method, user_id) VALUES (%s, %s, %s, %s)",
                       (equation, solution, method, user_id))
        connection.commit()
        print("Solution saved to the database.")
    except psycopg2.Error as e:
        print(f"Error saving solution to the database: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()


def generate_graph(function):
    x_values = np.linspace(-10, 10, 100)
    y_values = function(x_values)

    plt.plot(x_values, y_values, label='Function')
    plt.title('Graph of the Function')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return graph_data


def newton_method(function, derivative, initial, tolerance, max_iterations):
    iterations = 0
    x_new = initial
    x_old = x_new + 2 * tolerance
    errors = []

    while abs(x_new - x_old) > tolerance and iterations < max_iterations:
        x_old = x_new
        x_new = x_old - function(x_old) / derivative(x_old)
        iterations += 1
        deviation = abs(x_new - x_old)
        errors.append((iterations, deviation))

    if iterations == max_iterations:
        solution = "Did not converge"
    else:
        solution = x_new

    return solution, iterations, errors


def bisection_method(function, a, b, tolerance, max_iterations):
    iterations = 0
    x_new = a
    x_old = b
    errors = []

    while abs(x_new - x_old) > tolerance and iterations < max_iterations:
        x_mid = (a + b) / 2.0
        f_mid = function(x_mid)
        if f_mid == 0:
            break
        elif function(a) * f_mid < 0:
            b = x_mid
        else:
            a = x_mid

        x_old = x_new
        x_new = x_mid
        iterations += 1
        deviation = abs(x_new - x_old)
        errors.append((iterations, deviation))

    if iterations == max_iterations:
        solution = "Did not converge"
    else:
        solution = x_new

    return solution, iterations, errors


def secant_method(function, x0, x1, tolerance, max_iterations):
    iterations = 0
    x_new = x1
    x_old = x0
    errors = []

    while abs(x_new - x_old) > tolerance and iterations < max_iterations:
        x_next = x_new - (function(x_new) * (x_new - x_old)) / (function(x_new) - function(x_old))
        x_old = x_new
        x_new = x_next
        iterations += 1
        deviation = abs(x_new - x_old)
        errors.append((iterations, deviation))

    if iterations == max_iterations:
        solution = "Did not converge"
    else:
        solution = x_new

    return solution, iterations, errors


@app.route('/Root_Finding_Methods', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        equation_str = request.form['equation']
        x = sympy.Symbol('x')

        try:
            equation = sympy.sympify(equation_str)
            initial_str = request.form.get('initial', '1')
            initial = float(initial_str)
            tolerance_str = request.form.get('tolerance', '1e-6')
            tolerance = float(tolerance_str)
            max_iterations_str = request.form.get('max_iterations', '100')
            max_iterations = int(max_iterations_str)
            function = sympy.lambdify(x, equation)
            derivative = sympy.lambdify(x, sympy.diff(equation, x))

            if tolerance <= 0:
                raise ValueError("Tolerance must be positive.")
            if max_iterations <= 0:
                raise ValueError("Max iterations must be positive.")

            method = request.form.get('method')

            if method == 'Newton':
                solution, num_iterations, errors = newton_method(function, derivative, initial, tolerance,
                                                                 max_iterations)
            elif method == 'Bisection':
                a = float(request.form.get('a', '-10'))
                b = float(request.form.get('b', '10'))
                solution, num_iterations, errors = bisection_method(function, a, b, tolerance, max_iterations)
            elif method == 'Secant':
                x0 = float(request.form.get('x0', '-10'))
                x1 = float(request.form.get('x1', '10'))
                solution, num_iterations, errors = secant_method(function, x0, x1, tolerance, max_iterations)
            else:
                raise ValueError("Invalid method selected.")

            graph_data = generate_graph(function)

            username = session.get('username')  # Retrieve email from the session
            if username:
                save_solution_to_database(equation_str, solution, method, username)

            return render_template('index.html', solution=solution, equation=equation_str, initial=initial_str,
                                   tolerance=tolerance_str, max_iterations=max_iterations_str,
                                   num_iterations=num_iterations, errors=errors, graph_data=graph_data)
        except (sympy.SympifyError, ValueError) as e:
            return render_template('error.html', error_message=str(e))

    else:
        return render_template('index.html')


@app.route('/error')
def error():
    return render_template('error.html', error_message='Invalid request.')


@app.route('/')
def home():
    return render_template('home.html', error_message='Invalid request.')


@app.route('/register', methods=['POST'])
def register():
    success_message = None
    error_message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        connection = psycopg2.connect(DATABASE_URI)
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM \"user\" WHERE username = %s OR email = %s", (username, email))
            existing_user = cursor.fetchone()

            if existing_user:
                error_message = 'User with the same username or email already exists. Please choose a different one.'
            else:
                cursor.execute("INSERT INTO \"user\" (username, password, email) VALUES (%s, %s, %s)",
                               (username, password, email))
                connection.commit()
                success_message = 'Registration successful!'
        except psycopg2.Error as e:
            print(f"Error registering user: {e}")
            error_message = 'Error registering user. Please try again.'
        finally:
            if connection:
                cursor.close()
                connection.close()

    if success_message:
        return render_template('home.html', message=success_message)
    else:
        return render_template('home.html', unmessage=error_message)


@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']

        connection = psycopg2.connect(DATABASE_URI)
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM \"user\" WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()

            if user:
                username = user[1]

                session['username'] = username

                script = f"<script>window.sessionStorage.setItem('username', '{username}');</script>"

                return render_template('index.html', username=username, script=script, )
            else:

                return render_template('home.html', login_message='Invalid username or password')
        except psycopg2.Error as e:
            print(f"Error logging in: {e}")
            # Provide an error message in the JSON response
            return render_template('home.html', login_message='Error logging in. Please try again.')
        finally:
            if connection:
                cursor.close()
                connection.close()

    except Exception as e:
        print(f"Unexpected error: {e}")
        # Provide an error message and redirect to the login page
        return render_template('home.html', login_message='An unexpected error occurred')


@app.route('/user_history')
def user_history():
    username = session.get('username')
    if username:
        # Fetch user-specific history from the database
        history = get_user_history(username)
        return render_template('history.html', username=username, history=history)
    else:
        # Handle the case where the user is not logged in
        flash('Please log in to view your history.')
        return redirect(url_for('home'))


def get_user_history(username):
    connection = psycopg2.connect(DATABASE_URI)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT equation, solution, method
            FROM solution
            JOIN "user" ON solution.user_id = "user".id
            WHERE "user".username = %s
        """, (username,))
        history = cursor.fetchall()
        return history

    except psycopg2.Error as e:
        print(f"Error fetching user history: {e}")
        return []
    finally:
        if connection:
            cursor.close()
            connection.close()


if __name__ == '__main__':
    create_tables()
    app.run(debug=True, port=8080)
