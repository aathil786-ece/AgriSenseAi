import { useState } from 'react';

function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const farmerId = 1;  // Hardcoded for demo purposes

  const sendMessage = async () => {
    const userMessage = { sender: 'Farmer', text: input };
    setMessages([...messages, userMessage]);

    const response = await fetch('http://localhost:8000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ farmer_id: farmerId, message: input }),
    });

    const data = await response.json();
    const systemMessage = { sender: 'AgriSenseAI', text: data.reply };
    setMessages(prev => [...prev, systemMessage]);
    setInput('');
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>AgriSense AI Chat</h1>
      <div style={{ border: '1px solid #ccc', padding: '10px', height: '400px', overflowY: 'scroll' }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ margin: '10px 0' }}>
            <b>{msg.sender}:</b> {msg.text}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask about fertilizer, irrigation, pest control..."
        style={{ width: '80%', padding: '10px' }}
      />
      <button onClick={sendMessage} style={{ padding: '10px' }}>Send</button>
    </div>
  );
}

export default ChatInterface;