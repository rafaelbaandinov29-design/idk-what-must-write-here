import sqlite3  # sqlite3 будет работать с тем же файлом БД, что и в консольном этапе.
from flask import Flask, render_template, request, redirect, url_for  # Базовые функции Flask: шаблоны, формы, редирект, сборка URL.

app = Flask(__name__, static_folder="static")  # Создаём Flask-приложение; __name__ помогает Flask найти templates и другие ресурсы.

DB_NAME = "todo.db"  # Файл БД (он уже создан скриптом db_setup.py).

def get_connection():  # Простая функция, чтобы не копировать connect() в каждой строке.
    return sqlite3.connect(DB_NAME)  # Возвращаем новое соединение с БД.

@app.route("/")  # Главная страница: покажем список задач.
def index():
    conn = get_connection()  # Открываем соединение с базой.
    cursor = conn.cursor()  # Создаём курсор для выполнения SQL.
    cursor.execute("SELECT id, title FROM tasks ORDER BY id DESC")  # Читаем задачи и сортируем так, чтобы новые были сверху.
    tasks = cursor.fetchall()  # Получаем список задач (список кортежей).
    conn.close()  # Закрываем соединение, чтобы не держать файл заблокированным.

    return render_template("index.html", tasks=tasks)  # Передаём tasks в шаблон Jinja2.

@app.route("/add", methods=["POST"])  # Этот роут принимает данные формы (POST) и добавляет задачу.
def add_task():
    title = request.form.get("title", "").strip()  # Берём поле title из формы; get безопаснее, чем form[«title»].
    if title == "":  # Простая проверка: если пусто - ничего не добавляем.
        return redirect(url_for("index"))  # Возвращаем пользователя на главную.

    conn = get_connection()  # Открываем соединение с БД.
    cursor = conn.cursor()  # Создаём курсор.
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))  # Добавляем задачу; (title,) - кортеж из 1 элемента.
    conn.commit()  # Сохраняем изменения, иначе новая строка может не записаться в файл.
    conn.close()  # Закрываем соединение.

    return redirect(url_for("index"))

@app.route("/delete/<int:id>", methods=["POST"])  # Этот роут принимает данные формы (POST) и добавляет задачу.
def delete_task(id):

    conn = get_connection()  # Открываем соединение с БД.
    cursor = conn.cursor()  # Создаём курсор.
    cursor.execute("DELETE FROM tasks WHERE id=?",
                   (id,))  # Добавляем задачу; (title,) - кортеж из 1 элемента.
    conn.commit()  # Сохраняем изменения, иначе новая строка может не записаться в файл.
    conn.close()  # Закрываем соединение.

    return redirect(url_for("index"))

#for task in tasks: #Выполнено/невыполнено
    #task_id, title, description, created_date, is_done = task
    #status = "Выполнено" if is_done == 1 else "Не выполнено"
    #short_title = title[:17] + "..." if len(title) > 20 else title
    #print(f"{task_id:<4} {status:<12} {short_title:<20} {created_date[:16]:<20}")

#def add_task(self, title, description=''): #Защита от пустых задач
    #if not title or not title.strip():
        #print("Ошибка: Введите название задачи")
        #return False
        
    #title = title.strip()
    #created_date = datetime.now().strftime("")
    #self.cursor.execute()
    #self.conn.commit()
    #print(f"Задача '{title}' добавлена")
    #return True

# После добавления возвращаемся на главную страницу.

if __name__ == "__main__":  # Стандартная проверка: код ниже выполнится только при запуске файла напрямую.
    app.run(debug=True)  # Запускаем сервер разработки; debug=True удобен на практике (показывает ошибки).
