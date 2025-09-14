import React, { useState } from "react";
import axios from "axios";
import "./TaskList.css";

const API = "http://localhost:5000/api";

function TaskList({ tasks, onUpdated }) {
  const [comments, setComments] = useState({}); // store comments per task
  const [editId, setEditId] = useState(null);
  const [editTitle, setEditTitle] = useState("");

  // --- TASK CRUD ---
  const updateTask = async (id, newTitle) => {
    await axios.put(`${API}/tasks/${id}`, { title: newTitle });
    setEditId(null);
    onUpdated();
  };

  const deleteTask = async (id) => {
    await axios.delete(`${API}/tasks/${id}`);
    onUpdated();
  };

  // --- COMMENT CRUD ---
  const addComment = async (taskId) => {
    const text = comments[taskId];
    if (!text?.trim()) return;
    await axios.post(`${API}/tasks/${taskId}/comments`, { content: text });
    setComments({ ...comments, [taskId]: "" }); // reset input
    onUpdated();
  };

  return (
    <div className="task-list">
      {tasks.map((task) => (
        <div key={task.id} className="task-card">
          {/* --- Task Title + Edit --- */}
          {editId === task.id ? (
            <div>
              <input
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
              />
              <button onClick={() => updateTask(task.id, editTitle)}>
                Save
              </button>
              <button onClick={() => setEditId(null)}>Cancel</button>
            </div>
          ) : (
            <h3>
              {task.title}{" "}
              <button onClick={() => { setEditId(task.id); setEditTitle(task.title); }}>
                Edit
              </button>
              <button onClick={() => deleteTask(task.id)}>Delete</button>
            </h3>
          )}

          {/* --- Add Comment --- */}
          <div className="comment-section">
            <input
              className="comment-input"
              value={comments[task.id] || ""}
              onChange={(e) =>
                setComments({ ...comments, [task.id]: e.target.value })
              }
              placeholder="Add a comment..."
            />
            <button
              className="comment-btn"
              onClick={() => addComment(task.id)}
            >
              Comment
            </button>
          </div>

          {/* --- Show existing comments (if API sends them) --- */}
          {task.comments?.length > 0 && (
            <ul>
              {task.comments.map((c) => (
                <li key={c.id}>{c.content}</li>
              ))}
            </ul>
          )}
        </div>
      ))}
    </div>
  );
}

export default TaskList;

