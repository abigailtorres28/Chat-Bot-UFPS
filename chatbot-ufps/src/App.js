// src/App.js
import React, { useState } from 'react';

function App() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: input }),
      });

      const data = await res.json();
      setResponse(data.response.response); // doble acceso por estructura del JSON
    } catch (error) {
      setResponse("Error al conectar con el servidor.");
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>Chatbot UFPS 🤖</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Escribe tu pregunta..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{ width: "300px", padding: "0.5rem" }}
          required
        />
        <button type="submit" style={{ marginLeft: "1rem", padding: "0.5rem" }}>
          {loading ? "Cargando..." : "Enviar"}
        </button>
      </form>
      <div style={{ marginTop: "2rem" }}>
        <strong>Respuesta del chatbot:</strong>
        <p>{response}</p>
      </div>
    </div>
  );
}

export default App;
