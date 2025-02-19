import React, { useState, useEffect } from 'react';

function App() {
  const [message, setMessage] = useState('');
  const [cookies, setCookies] = useState([]);

  // Function to fetch cookies from the backend
  const fetchCookies = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/cookies");
      if (!response.ok) {
        throw new Error(`Error fetching cookies: ${response.statusText}`);
      }
      const data = await response.json();
      setCookies(data);
    } catch (error) {
      console.error("Error fetching cookies:", error);
      setMessage("Error fetching cookies.");
    }
  };

  // Fetch cookies on component mount
  useEffect(() => {
    fetchCookies();
  }, []);

  // Function to add a cookie
  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
    const jsonData = Object.fromEntries(formData.entries());

    console.log("Submitting cookie data:", jsonData);

    const level = Number(jsonData.level);
    if (level < 1 || level > 90) {
      setMessage("Error: Level must be between 1 and 90.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/api/cookies", {
        method: "POST",
        body: JSON.stringify(jsonData),
        headers: { "Content-Type": "application/json" }
      });

      if (!response.ok) {
        throw new Error(`Failed to add cookie: ${response.statusText}`);
      }

      const data = await response.json();
      setMessage(`Cookie added with ID: ${data.id}`);
      // Refresh the list of cookies
      fetchCookies();
    } catch (error) {
      console.error("Error:", error);
      setMessage("Error adding cookie.");
    }
  };

  // Function to delete all cookies
  const clearAllCookies = async () => {
    if (!window.confirm("Are you sure you want to clear all cookies?")) {
      return;
    }
    try {
      const response = await fetch("http://127.0.0.1:5000/api/cookies", {
        method: "DELETE",
      });
      if (!response.ok) {
        throw new Error(`Failed to delete cookies: ${response.statusText}`);
      }
      const data = await response.json();
      setMessage(data.message);
      // Refresh the list of cookies
      fetchCookies();
    } catch (error) {
      console.error("Error:", error);
      setMessage("Error deleting cookies.");
    }
  };

  // Function to calculate the max achievable cookie level using FormData
  const handleCalcSubmit = async (event) => {
    event.preventDefault();

    // Create a FormData object from the calculation form
    const formData = new FormData(event.target);
    const dataObject = Object.fromEntries(formData.entries());
    
    // Build a "jellies" object from the form data. The input names correspond to the outer level.
    const jellies = {
      "Lv.1": Number(dataObject["Lv.1"] || 0),
      "Lv.2": Number(dataObject["Lv.2"] || 0),
      "Lv.3": Number(dataObject["Lv.3"] || 0),
      "Lv.4": Number(dataObject["Lv.4"] || 0),
      "Lv.5": Number(dataObject["Lv.5"] || 0),
      "Lv.6": Number(dataObject["Lv.6"] || 0),
      "Lv.7": Number(dataObject["Lv.7"] || 0),
      "Lv.8": Number(dataObject["Lv.8"] || 0),
    };

    const jelly_upgrade = Number(dataObject.jelly_upgrade || 0);
    if (jelly_upgrade < 0 || jelly_upgrade > 5) {
      setMessage("Invalid jelly upgrade level. Must be between 0 and 5.");
      return;
    }

    const dataToSend = { jellies, jelly_upgrade };

    try {
      const response = await fetch("http://127.0.0.1:5000/api/calc", {
        method: "POST",
        body: JSON.stringify(dataToSend),
        headers: { "Content-Type": "application/json" }
      });
      if (!response.ok) {
        throw new Error(`Failed to calculate: ${response.statusText}`);
      }
      const data = await response.json();
      setMessage(`Max achievable cookie level: ${data.max_level}`);
    } catch (error) {
      console.error("Error:", error);
      setMessage("Error calculating max level.");
    }
  };

  return (
    <div>
      <h1>Cookie App</h1>
      
      {/* Add Cookie Form */}
      <form onSubmit={handleSubmit}>
        <h2>Add Cookie</h2>
        <label>
          Level:
          <input type="number" name="level" min="1" max="90" required />
        </label>
        <br />
        <label>
          Experience:
          <input type="number" name="exp" required />
        </label>
        <br />
        <button type="submit">Add Cookie</button>
      </form>

      <button onClick={clearAllCookies}>Clear All Cookies</button>

      {/* Calculate Max Level Form */}
      <form onSubmit={handleCalcSubmit}>
        <h2>Calculate Max Level</h2>
        <label>
          Jelly Upgrade Level (0 for Base, 1-5 for Lv.1 to Lv.5):
          <input type="number" name="jelly_upgrade" min="0" max="5" required />
        </label>
        <br />
        <p>Enter the quantity of EXP jellies for each outer level:</p>
        <label>
          Lv.1:
          <input type="number" name="Lv.1" min="0" defaultValue="0" />
        </label>
        <br />
        <label>
          Lv.2:
          <input type="number" name="Lv.2" min="0" defaultValue="0" />
        </label>
        <br />
        <label>
          Lv.3:
          <input type="number" name="Lv.3" min="0" defaultValue="0" />
        </label>
        <br />
        <label>
          Lv.4:
          <input type="number" name="Lv.4" min="0" defaultValue="0" />
        </label>
        <br />
        <label>
          Lv.5:
          <input type="number" name="Lv.5" min="0" defaultValue="0" />
        </label>
        <br />
        <label>
          Lv.6:
          <input type="number" name="Lv.6" min="0" defaultValue="0" />
        </label>
        <br />
        <label>
          Lv.7:
          <input type="number" name="Lv.7" min="0" defaultValue="0" />
        </label>
        <br />
        <label>
          Lv.8:
          <input type="number" name="Lv.8" min="0" defaultValue="0" />
        </label>
        <br />
        <button type="submit">Calculate Max Level</button>
      </form>

      {/* Display Cookies */}
      <h2>Cookies</h2>
      {cookies.length === 0 ? (
        <p>No cookies available.</p>
      ) : (
        <ul>
          {cookies.map((cookie) => (
            <li key={cookie.id}>
              <strong>ID:</strong> {cookie.id} | <strong>Level:</strong> {cookie.level} | <strong>EXP:</strong> {cookie.exp}
            </li>
          ))}
        </ul>
      )}

      {message && <p>{message}</p>}
    </div>
  );
}

export default App;
