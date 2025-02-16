import React, { useState } from 'react';

function App() {
  const [message, setMessage] = useState('');

  const addCookie = async () => {
    console.log("addCookie function triggered");

    const newCookie = { level: 1, exp: 100 };

    try {
      console.log("Sending POST request to /api/cookies...");
      const response = await fetch("http://127.0.0.1:5000/api/cookies", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newCookie),
      });
      console.log("Response received:", response);

      if (!response.ok) {
        throw new Error(`Failed to add cookie: ${response.statusText}`);
      }

      const data = await response.json();
      setMessage(`Cookie added with ID: ${data.id}`);
    } catch (error) {
      console.error("Error:", error);
      setMessage("Error adding cookie");
    }
  };

  return (
    <div>
      <h1>Cookie App</h1>
      <button onClick={addCookie}>Add Cookie</button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default App;
