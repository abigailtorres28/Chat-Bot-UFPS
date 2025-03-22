# backend/main.py
from quart import Quart, request, jsonify
from agent import chatbot_agent

app = Quart(__name__)

@app.route("/chat", methods=["POST"])
async def chat():
    """Endpoint para recibir preguntas y devolver respuestas del chatbot."""
    data = await request.json
    user_message = data.get("message")
    
    if not user_message:
        return jsonify({"error": "No se recibió mensaje"}), 400

    response = await chatbot_agent(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
