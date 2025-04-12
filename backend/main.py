# backend/main.py
from quart import Quart, request, jsonify
from quart_cors import cors
from agent import chatbot_agent
import json

app = Quart(__name__)
app = cors(app, allow_origin="http://localhost:3000")

@app.route("/chat", methods=["POST"])
async def chat():
    data = await request.get_data()
    try:
        data = data.decode('utf-8')
        data_json = json.loads(data)
    except UnicodeDecodeError:
        return jsonify({"error": "No se pudo decodificar el mensaje"}), 400
    except json.JSONDecodeError:
        return jsonify({"error": "Formato JSON inválido"}), 400

    user_message = data_json.get("message")
    print(f"📨 Mensaje recibido desde frontend: '{user_message}'")
    if not user_message:
        return jsonify({"error": "No se recibió mensaje"}), 400

    response = await chatbot_agent(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
