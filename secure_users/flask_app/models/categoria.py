from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

DB = "esquema"


class Categorias:
    def __init__(self, data):
        self.id_categoria = data["id_categoria"]
        self.nombre = data["nombre"]
        self.descripcion = data["descripcion"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # ------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------
    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO categorias (
                nombre, 
                descripcion, 
                created_at, 
                updated_at
            ) VALUES (
                %(nombre)s, 
                %(descripcion)s, 
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
                id_categoria,
                nombre,
                descripcion,
                created_at,
                updated_at
            FROM categorias
            ORDER BY id_categoria;
        """
        resultados = connectToMySQL(DB).query_db(query)
        categorias = []
        for categoria in resultados:
            categorias.append(cls(categoria))
        return categorias

    @classmethod
    def buscar_id(cls, id):
        query = """
            SELECT 
                id_categoria,
                nombre,
                descripcion,
                created_at,
                updated_at
            FROM categorias
            WHERE id_categoria = %(id_categoria)s;
        """
        data = {"id_categoria": id}
        resultado = connectToMySQL(DB).query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    @classmethod
    def buscar_nombre(cls, nombre):
        query = """
            SELECT 
                id_categoria,
                nombre,
                descripcion,
                created_at,
                updated_at
            FROM categorias
            WHERE nombre = %(nombre)s;
        """
        data = {"nombre": nombre}
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
            UPDATE categorias
            SET 
                nombre = %(nombre)s,
                descripcion = %(descripcion)s,
                updated_at = NOW()
            WHERE id_categoria = %(id_categoria)s;
        """
        return connectToMySQL(DB).query_db(query, data)

    # ------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------
    @classmethod
    def eliminar(cls, id):
        query = """
            DELETE FROM categorias
            WHERE id_categoria = %(id_categoria)s;
        """
        data = {"id_categoria": id}
        return connectToMySQL(DB).query_db(query, data)

    # ------------------------------------------------------------
    # VALIDACIONES
    # ------------------------------------------------------------
    @staticmethod
    def validar(datos):
        es_valido = True

        if not datos["nombre"].strip():
            flash("El nombre es obligatorio.", "danger"); es_valido = False
        elif len(datos["nombre"].strip()) < 3:
            flash("El nombre debe tener al menos 3 caracteres.", "danger"); es_valido = False
        elif Categorias.buscar_nombre(datos["nombre"].strip()):
            flash("Esta categoría ya existe.", "danger"); es_valido = False

        if not datos.get("descripcion", "").strip():
            flash("La descripción es obligatoria.", "danger"); es_valido = False

        return es_valido