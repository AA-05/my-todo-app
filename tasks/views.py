import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .db import get_connection

# Render main page
def index(request):
    return render(request, 'tasks/index.html')

# GET all tasks
def get_tasks(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, due_date, status FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    tasks = [{"id": r[0], "title": r[1], "description": r[2], "due_date": r[3], "status": r[4]} for r in rows]
    return JsonResponse(tasks, safe=False)

# POST create task
@csrf_exempt
def create_task(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        data = json.loads(request.body)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description, due_date, status) VALUES (?, ?, ?, ?)",
            (data['title'], data.get('description', ''), data.get('due_date', ''), data.get('status', 'pending'))
        )
        conn.commit()
        conn.close()
        return JsonResponse({"message": "Task created successfully"}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

# PUT update task
@csrf_exempt
def update_task(request, task_id):
    if request.method != "PUT":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        data = json.loads(request.body)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET title=?, description=?, due_date=?, status=? WHERE id=?",
            (data['title'], data.get('description', ''), data.get('due_date', ''), data.get('status', 'pending'), task_id)
        )
        conn.commit()
        conn.close()
        return JsonResponse({"message": "Task updated successfully"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

# DELETE task
@csrf_exempt
def delete_task(request, task_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()
        return JsonResponse({"message": "Task deleted successfully"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
