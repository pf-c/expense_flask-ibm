# Import libraries
from flask import Flask, jsonify, request, render_template, redirect, url_for

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions=[
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]
# Read operation
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)
# Create operation
@app.route("/add", methods=["GET","POST"])
def add_transaction():
    if request.method == "POST":
        transation = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        transactions.append(transation)
        return redirect(url_for("get_transactions"))
    return render_template("form.html")
# Update operation
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    transaction = next((t for t in transactions if t['id'] == transaction_id), None)
    if request.method == "POST":
        date = request.form['date']
        amount = float(request.form['amount'])
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break
        return redirect(url_for("get_transactions"))
    for  transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)

    return {"message": "Transaction not found"}, 404
# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break
    return redirect(url_for("get_transactions"))

# Search Transactions
@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    if request.method == "POST":
        # Retrieve the input values from the form
        try:
            min_amount = float(request.form.get("min_amount"))
            max_amount = float(request.form.get("max_amount"))
        except (ValueError, TypeError):
            # Handle invalid input gracefully
            min_amount = None
            max_amount = None

        # Filter transactions based on the input range
        if min_amount is not None and max_amount is not None:
            filtered_transactions = [
                t for t in transactions if min_amount <= t['amount'] <= max_amount
            ]
        else:
            filtered_transactions = transactions  # Show all if inputs are invalid

        # Render the filtered transactions
        return render_template("transactions.html", transactions=filtered_transactions)

    # Render the search form if the request is GET
    return render_template("search.html")

# Total Balance
@app.route("/total")
def total_balance():
    total = sum(t['amount'] for t in transactions)
    return f"<p>Total amount is ${total}</p>"

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)