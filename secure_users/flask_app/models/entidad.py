from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

DB = "esquema"


class Entidades:   # ← RENOMBRAR según escenario: Tareas, Libros, Peliculas...
    def __init__(self, data):
        self.id_entidad = data["id_entidad"]
        self.nombre = data["nombre"]
        self.descripcion = data["descripcion"]
        # ↓↓↓ CAMPOS ESPECÍFICOS (ajustar según escenario) ↓↓↓
        self.fecha = data.get("fecha")
        self.precio = data.get("precio")
        self.stock = data.get("stock")
        # ↑↑↑ ↑↑↑
        self.categoria_id = data["categoria_id"]
        self.usuario_id = data["usuario_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        # Datos de JOINs
        self.categoria_nombre = data.get("categoria_nombre")
        self.creador_nombre = data.get("creador_nombre")
        self.creador_apellido = data.get("creador_apellido")

    # ------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------
    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO entidades (
                nombre, 
                descripcion, 
                fecha, 
                precio, 
                stock,
                categoria_id, 
                usuario_id, 
                created_at, 
                updated_at
            ) VALUES (
                %(nombre)s, 
                %(descripcion)s, 
                %(fecha)s, 
                %(precio)s, 
                %(stock)s,
                %(categoria_id)s, 
                %(usuario_id)s, 
                NOW(), 
                NOW()
            );
        """
        return connectToMySQL(DB).query_db(query, data)

    # ------------------------------------------------------------
    # READ
    # ------------------------------------------------------------
    @classmethod
    def ver_todas(cls):
        query = """
            SELECT 
                e.id_entidad,
                e.nombre,
                e.descripcion,
                e.fecha,
                e.precio,
                e.stock,
                e.categoria_id,
                e.usuario_id,
                e.created_at,
                e.updated_at,
                c.nombre AS categoria_nombre,
                u.nombre AS creador_nombre,
                u.apellido AS creador_apellido
            FROM entidades e
            JOIN categorias c ON e.categoria_id = c.id_categoria
            JOIN usuarios u ON e.usuario_id = u.id_usuario
            ORDER BY e.id_entidad;
        """
        resultados = connectToMySQL(DB).query_db(query)
        entidades = []
        for entidad in resultados:
            entidades.append(cls(entidad))
        return entidades

    @classmethod
    def buscar_id(cls, id):
        query = """
            SELECT 
                e.id_entidad,
                e.nombre,
                e.descripcion,
                e.fecha,
                e.precio,
                e.stock,
                e.categoria_id,
                e.usuario_id,
                e.created_at,
                e.updated_at,
                c.nombre AS categoria_nombre,
                u.nombre AS creador_nombre,
                u.apellido AS creador_apellido
            FROM entidades e
            JOIN categorias c ON e.categoria_id = c.id_categoria
            JOIN usuarios u ON e.usuario_id = u.id_usuario
            WHERE e.id_entidad = %(id_entidad)s;
        """
        data = {"id_entidad": id}
        resultado = connectToMySQL(DB).query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    # ------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------
    @classmethod
    def modificar(cls, data):
        query = """
            UPDATE entidades
            SET 
                nombre = %(nombre)s,
                descripcion = %(descripcion)s,
                fecha = %(fecha)s,
                precio = %(precio)s,
                stock = %(stock)s,
                categoria_id = %(categoria_id)s,
                updated_at = NOW()
            WHERE id_entidad = %(id_entidad)s;
        """
        return connectToMySQL(DB).query_db(query, data)

    # ------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------
    @classmethod
    def eliminar(cls, id):
        query = """
            DELETE FROM entidades
            WHERE id_entidad = %(id_entidad)s;
        """
        data = {"id_entidad": id}
        return connectToMySQL(DB).query_db(query, data)

    # ------------------------------------------------------------
    # VALIDACIONES
    # ------------------------------------------------------------
    @staticmethod
    def validar(datos):
        es_valido = True

        if not datos["nombre"].strip():
            flash("El nombre es obligatorio.", "danger"); es_valido = False
        elif len(datos["nombre"].strip()) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "danger"); es_valido = False

        if not datos["descripcion"].strip():
            flash("La descripción es obligatoria.", "danger"); es_valido = False
        elif len(datos["descripcion"].strip()) < 10:
            flash("La descripción debe tener al menos 10 caracteres.", "danger"); es_valido = False

        if not datos["categoria_id"]:
            flash("Debes seleccionar una categoría.", "danger"); es_valido = False

        return es_valido