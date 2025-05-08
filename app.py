from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)
ORDERS_FILE = "orders.xlsx"

@app.route("/api/order", methods=["POST"])
def receive_order():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Нет данных"}), 400

    df_new = pd.DataFrame([{
        "username": data.get("username"),
        "user_id": data.get("user_id"),
        "contractor": data.get("contractor"),
        "address": data.get("address"),
        "date": data.get("date"),
        "items": data.get("items"),
        "status": "Ожидает подтверждения"
    }])

    if os.path.exists(ORDERS_FILE):
        df = pd.read_excel(ORDERS_FILE)
        df = pd.concat([df, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_excel(ORDERS_FILE, index=False)
    return jsonify({"message": "Заказ получен"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)