from flask import Flask, render_template, jsonify
import psycopg2
import subprocess

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="covid",
        user="user",
        password="password"
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/covid')
def covid():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM covid_data')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route('/api/predict')
def predict():
    result = subprocess.run(['python3', 'data_analysis/covid_prediction.py'], capture_output=True, text=True)
    return jsonify({"result": result.stdout})

if __name__ == '__main__':
    app.run(debug=True)
