import sqlite3
from werkzeug.security import generate_password_hash
from config import Config

def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Crea las tablas de la base de datos y un usuario admin por defecto."""
    try:
        with sqlite3.connect(Config.DATABASE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Tabla estudiantes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS estudiantes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellidos TEXT NOT NULL,
                    fecha_nacimiento TEXT NOT NULL
                )
            ''')

            # Tabla cursos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cursos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descripcion TEXT NOT NULL,
                    horas INTEGER NOT NULL
                )
            ''')

            # Tabla inscripcion
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inscripcion (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    estudiante_id INTEGER NOT NULL,
                    curso_id INTEGER NOT NULL,
                    FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id),
                    FOREIGN KEY (curso_id) REFERENCES cursos (id)
                )
            ''')

            # Tabla usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT NOT NULL UNIQUE,
                    correo TEXT NOT NULL UNIQUE,
                    celular TEXT NOT NULL,
                    contraseña TEXT NOT NULL
                )
            ''')

            # Insertar usuario admin por defecto si no existe
            cursor.execute('SELECT 1 FROM usuarios WHERE usuario = ?', ('admin',))
            if not cursor.fetchone():
                hashed = generate_password_hash('admin742##')
                cursor.execute('''
                    INSERT INTO usuarios (usuario, correo, celular, contrasena)
                    VALUES (?, ?, ?, ?)
                ''', ('admin', 'admin@admin.com', '77712345', hashed))

            conn.commit()
            print("Tablas creadas correctamente y usuario admin asegurado.")

    except sqlite3.Error as e:
        print(f"Error en la base de datos: {e}")
