from flask import Blueprint, request, jsonify
from database import db
from models import Task, Comment

api = Blueprint("api", __name__)

# Create Task
@api.route("/tasks", methods=["POST"])
def create_task():
    data = request.json or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error":"title required"}), 400
    task = Task(title=title, description=data.get("description"))
    db.session.add(task)
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title}), 201

# Get all tasks
@api.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title, "description": t.description} for t in tasks])

# Add Comment
@api.route("/tasks/<int:task_id>/comments", methods=["POST"])
def add_comment(task_id):
    # ensure task exists
    task = Task.query.get_or_404(task_id)
    data = request.json or {}
    content = data.get("content", "").strip()
    if not content:
        return jsonify({"error": "Content required"}), 400
    comment = Comment(content=content, task_id=task_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify({"id": comment.id, "content": comment.content}), 201

# Edit Comment
@api.route("/comments/<int:comment_id>", methods=["PUT"])
def edit_comment(comment_id):
    data = request.json
    comment = Comment.query.get_or_404(comment_id)
    comment.content = data["content"]
    db.session.commit()
    return jsonify({"id": comment.id, "content": comment.content})

# Delete Comment
@api.route("/comments/<int:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted"})

@api.route("/", methods=["GET"])
def index():
    return jsonify({"message": "API is working!"})

# Get all comments for a task
@api.route("/tasks/<int:task_id>/comments", methods=["GET"])
def get_comments(task_id):
    # Ensure task exists
    task = Task.query.get_or_404(task_id)
    comments = Comment.query.filter_by(task_id=task_id).order_by(Comment.created_at.asc()).all()
    return jsonify([{"id": c.id, "content": c.content, "created_at": c.created_at.isoformat()} for c in comments])

# Delete Task
@api.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200

# Edit Task
@api.route("/tasks/<int:task_id>", methods=["PUT"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "title required"}), 400
    task.title = title
    task.description = data.get("description", task.description)
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title, "description": task.description})





