from flask import Flask, request, redirect, render_template, flash
import psycopg2

app = Flask(__name__)
app.secret_key = "todo-secret-key"

def get_conn():
    return psycopg2.connect(
        host="localhost",
        database="tododb",
        user="guest",
        password="password",
        port=5433
    )

@app.route("/", methods=["GET"])
def index():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM categories ORDER BY id;")
    categories = cur.fetchall()

    cur.execute("""
        SELECT t.id, t.title, c.name, t.is_done, t.created_at
        FROM tasks t
        JOIN categories c ON t.category_id = c.id
        ORDER BY t.created_at DESC, t.id DESC;
    """)
    tasks = cur.fetchall()

    cur.close()
    conn.close()
    return render_template("index.html", tasks=tasks, categories=categories)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    category_id = request.form.get("category_id", "").strip()

    # ★ タスク名が空白
    if not title:
        flash("タスク名を入力してください。")
        return redirect("/")

    if not category_id:
        return redirect("/")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title, category_id) VALUES (%s, %s);",
        (title, int(category_id))
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

@app.route("/add_category", methods=["POST"])
def add_category():
    name = request.form.get("category_name", "").strip()

    # ★ カテゴリ名が空白
    if not name:
        flash("カテゴリ名を入力してください。")
        return redirect("/")

    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO categories (name) VALUES (%s);", (name,))
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        flash("このカテゴリ名はすでに存在しています。")
    finally:
        cur.close()
        conn.close()

    return redirect("/")

@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET is_done = NOT is_done WHERE id = %s;", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

@app.route("/delete_category/<int:category_id>", methods=["POST"])
def delete_category(category_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks WHERE category_id = %s;", (category_id,))
    cur.execute("DELETE FROM categories WHERE id = %s;", (category_id,))

    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
