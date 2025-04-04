# backend/main.py
import json
from quart import Quart, request, jsonify
from agent import chatbot_agent

app = Quart(__name__)

@app.route("/chat", methods=["POST"])
async def chat():
    """Endpoint para recibir preguntas y devolver respuestas del chatbot."""
    """Endpoint para recibir preguntas y devolver respuestas del chatbot."""
    data = await request.get_data()  # Obtén los datos crudos de la solicitud
    try:
        data = data.decode('utf-8')  # Decodifica el contenido en UTF-8
        data_json = json.loads(data)  # Convierte los datos en JSON
    except UnicodeDecodeError:
        return jsonify({"error": "No se pudo decodificar el mensaje, asegúrate de que el contenido esté en UTF-8"}), 400
    except json.JSONDecodeError:
        return jsonify({"error": "No se pudo procesar el formato JSON del mensaje"}), 400

    user_message = data_json.get("message")  # Ahora obtenemos el mensaje de manera segura
    
    if not user_message:
        return jsonify({"error": "No se recibió mensaje"}), 400

    response = await chatbot_agent(user_message)
    return jsonify({"response": response})
if __name__ == "__main__":
    app.run(port=5000, debug=True)
