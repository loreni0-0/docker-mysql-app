import os
import time
from flask import Flask, render_template_string
import pymysql

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "usuario")
DB_PASSWORD = os.getenv("DB_PASSWORD", "clave123")
DB_NAME = os.getenv("DB_NAME", "pruebadb")
DB_PORT = int(os.getenv("DB_PORT", "3306"))

def get_db_connection():
    retries = 10
    while retries > 0:
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                port=DB_PORT,
                connect_timeout=5
            )
            return conn, None
        except pymysql.MySQLError as e:
            retries -= 1
            if retries == 0:
                return None, str(e)
            time.sleep(2)
    return None, "Tiempo de espera agotado"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hola Mundo - Docker Compose & MySQL</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #f4f6f9;
            color: #333;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        .card {
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            max-width: 500px;
            width: 100%;
            padding: 35px 30px;
            text-align: center;
        }
        h1 {
            color: #0b5ed7;
            font-size: 2rem;
            margin-bottom: 10px;
        }
        .badge {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
            margin: 15px 0;
        }
        .badge-success {
            background-color: #d1e7dd;
            color: #0f5132;
        }
        .badge-danger {
            background-color: #f8d7da;
            color: #842029;
        }
        .info-table {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
            text-align: left;
        }
        .info-table th, .info-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #edf2f7;
            font-size: 0.95rem;
        }
        .info-table th {
            color: #6c757d;
            font-weight: 500;
            width: 45%;
        }
        .info-table td {
            color: #212529;
            font-weight: 600;
        }
        .footer {
            margin-top: 25px;
            font-size: 0.85rem;
            color: #888;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>👋 ¡Hola Mundo!</h1>
        {% if success %}
            <span class="badge badge-success">✓ Conexión exitosa a MySQL</span>
            <table class="info-table">
                <tr>
                    <th>Base de Datos:</th>
                    <td>{{ db_name }}</td>
                </tr>
                <tr>
                    <th>Host del Servidor:</th>
                    <td>{{ db_host }}</td>
                </tr>
                <tr>
                    <th>Versión del Motor:</th>
                    <td>MySQL {{ db_version }}</td>
                </tr>
                <tr>
                    <th>Hora de la BD:</th>
                    <td>{{ db_time }}</td>
                </tr>
            </table>
        {% else %}
            <span class="badge badge-danger">✗ Error de Conexión</span>
            <p style="color: #842029; font-size: 0.9rem;">{{ error_msg }}</p>
        {% endif %}
        <div class="footer">
            Docker Compose &bull; Flask (Python 3.11) &bull; MySQL 8.0
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def hola_mundo():
    conn, error_msg = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT VERSION(), NOW();")
                version, current_time = cursor.fetchone()
            return render_template_string(
                HTML_TEMPLATE,
                success=True,
                db_name=DB_NAME,
                db_host=DB_HOST,
                db_version=version,
                db_time=str(current_time)
            )
        finally:
            conn.close()
    else:
        return render_template_string(
            HTML_TEMPLATE,
            success=False,
            error_msg=error_msg
        ), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
