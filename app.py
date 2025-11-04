from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  amount REAL NOT NULL,
                  category TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/expenses', methods=['GET'])
def get_expenses():
    print("Fetching all expenses...")
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT * FROM expenses')
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (title, amount, category) VALUES (?, ?, ?)",
              (data['title'], data['amount'], data['category']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Expense added successfully'}), 201

@app.route('/expenses/<int:id>', methods=['PUT'])
def update_expense(id):
    data = request.get_json()
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("UPDATE expenses SET title=?, amount=?, category=? WHERE id=?",
              (data['title'], data['amount'], data['category'], id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Expense updated successfully'})

@app.route('/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Expense deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
