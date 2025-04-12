import React, { useState } from 'react';

function App() {
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!message.trim()) return;

    setLoading(true);
    setChat([...chat, { sender: 'user', text: message }]);

    try {
      const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      });
    
      const data = await response.json();
      console.log("📦 Respuesta del backend:", data);
    
      const botMessage = data.response || 'Error en la respuesta';
    
      setChat(prev => [...prev, { sender: 'bot', text: botMessage }]);
    } catch (error) {
      setChat(prev => [...prev, { sender: 'bot', text: 'Error de conexión con el backend.' }]);
    }
    

    setMessage('');
    setLoading(false);
  };

  return (
    <div style={{
      maxWidth: '600px',
      margin: '40px auto',
      padding: '20px',
      border: '1px solid #ccc',
      borderRadius: '10px',
      fontFamily: 'Arial, sans-serif',
      backgroundColor: '#f9f9f9'
    }}>
      <h1 style={{ textAlign: 'center' }}>Chatbot UFPS 🤖</h1>
  
      <div style={{
        maxHeight: '400px',
        overflowY: 'auto',
        marginBottom: '15px',
        display: 'flex',
        flexDirection: 'column',
        gap: '10px'
      }}>
        {chat.map((msg, i) => (
          <div
            key={i}
            style={{
              alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
              backgroundColor: msg.sender === 'user' ? '#DCF8C6' : '#FFFFFF',
              padding: '10px',
              borderRadius: '10px',
              maxWidth: '80%',
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
            }}
          >
            <strong>{msg.sender === 'user' ? 'Tú' : 'Chatbot'}:</strong>
            <div style={{ marginTop: '5px', whiteSpace: 'pre-line' }}>{msg.text}</div>
          </div>
        ))}
      </div>
  
      <div style={{ display: 'flex' }}>
        <input
          type="text"
          placeholder="Escribe tu pregunta..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          style={{
            flex: 1,
            padding: 10,
            border: '1px solid #ccc',
            borderRadius: '5px'
          }}
        />
        <button
          onClick={handleSend}
          disabled={loading}
          style={{
            marginLeft: '10px',
            padding: '10px 15px',
            border: 'none',
            backgroundColor: '#007bff',
            color: '#fff',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          {loading ? 'Enviando...' : 'Enviar'}
        </button>
      </div>
    </div>
  );
  
}

export default App;
