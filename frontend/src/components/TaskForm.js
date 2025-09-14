import React, { useState } from "react";
import axios from "axios";
import "./TaskForm.css";

const API = "http://localhost:5000/api";

function TaskForm({ onTaskCreated }) {
  const [title, setTitle] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    await axios.post(`${API}/tasks`, { title });
    setTitle("");
    onTaskCreated();
  };

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <input
        className="task-input"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Enter task title..."
      />
      <button className="add-btn" type="submit">
        + Add Task
      </button>
    </form>
  );
}

export default TaskForm;
