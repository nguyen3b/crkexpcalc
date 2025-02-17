import React, { useState } from 'react';

function App() {
  const [message, setMessage] = useState('');

  // Function to handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent page reload

    // Create a FormData object and append input values
    const formData = new FormData(event.target);
    // Convert FormData to a JSON object
    const jsonData = Object.fromEntries(formData.entries());

    console.log("Submitting data:", jsonData);

    const level = Number(jsonData.level);
    // level range
    if (level < 0 || level > 90) {
      setMessage("Error: Level must be between 1 to 90")
      return
    }
    try {
      const response = await fetch("http://127.0.0.1:5000/api/cookies", {
        method: "POST",
        body: JSON.stringify(jsonData), // Send JSON data
        headers: {
          "Content-Type": "application/json"
        }
      });

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
      <form onSubmit={handleSubmit}>
        <label>
          Level:
          <input type="number" name="level" min = "1" max = "89" required />
        </label>
        <label>
          Experience:
          <input type="number" name="exp" required />
        </label>
        <button type="submit">Add Cookie</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default App;
