from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

DB = "familia_peluche"


class Peluches:
    def __init__(self, data):
        self.id_peluche = data["id_peluche"]
        self.nombre = data["nombre"]
        self.descripcion = data["descripcion"]
        self.visitas = data.get("visitas", 0)
        self.donador_id = data.get("donador_id")
        self.adoptador_id = data.get("adoptador_id")
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        # Datos de JOINs
        self.donador_nombre = data.get("donador_nombre")
        self.donador_apellido = data.get("donador_apellido")
        self.adoptador_nombre = data.get("adoptador_nombre")
        self.adoptador_apellido = data.get("adoptador_apellido")

    # ------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------
    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO peluches (
                nombre, 
                descripcion, 
                donador_id, 
                adoptador_id,
                created_at, 
                updated_at
            ) VALUES (
                %(nombre)s, 
                %(descripcion)s, 
                %(donador_id)s, 
                %(adoptador_id)s,
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
                p.id_peluche,
                p.nombre,
                p.descripcion,
                p.visitas,
                p.donador_id,
                p.adoptador_id,
                p.created_at,
                p.updated_at,
                d.nombre AS donador_nombre,
                d.apellido AS donador_apellido,
                a.nombre AS adoptador_nombre,
                a.apellido AS adoptador_apellido
            FROM peluches p
            LEFT JOIN usuarios d ON p.donador_id = d.id_usuario
            LEFT JOIN usuarios a ON p.adoptador_id = a.id_usuario
            ORDER BY p.id_peluche;
        """
        resultados = connectToMySQL(DB).query_db(query)
        peluches = []
        for peluche in resultados:
            peluches.append(cls(peluche))
        return peluches

    @classmethod
    def buscar_id(cls, id):
        query = """
            SELECT 
                p.id_peluche,
                p.nombre,
                p.descripcion,
                p.visitas,
                p.donador_id,
                p.adoptador_id,
                p.created_at,
                p.updated_at,
                d.nombre AS donador_nombre,
                d.apellido AS donador_apellido,
                a.nombre AS adoptador_nombre,
                a.apellido AS adoptador_apellido
            FROM peluches p
            LEFT JOIN usuarios d ON p.donador_id = d.id_usuario
            LEFT JOIN usuarios a ON p.adoptador_id = a.id_usuario
            WHERE p.id_peluche = %(id_peluche)s;
        """
        data = {"id_peluche": id}
        resultado = connectToMySQL(DB).query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    @classmethod
    def buscar_donador(cls, donador_id):
        query = """
            SELECT 
                p.id_peluche,
                p.nombre,
                p.descripcion,
                p.visitas,
                p.donador_id,
                p.adoptador_id,
                p.created_at,
                p.updated_at,
                d.nombre AS donador_nombre,
                d.apellido AS donador_apellido,
                a.nombre AS adoptador_nombre,
                a.apellido AS adoptador_apellido
            FROM peluches p
            LEFT JOIN usuarios d ON p.donador_id = d.id_usuario
            LEFT JOIN usuarios a ON p.adoptador_id = a.id_usuario
            WHERE p.donador_id = %(donador_id)s
            ORDER BY p.id_peluche;
        """
        data = {"donador_id": donador_id}
        resultados = connectToMySQL(DB).query_db(query, data)
        peluches = []
        for peluche in resultados:
            peluches.append(cls(peluche))
        return peluches

    @classmethod
    def buscar_adoptante(cls, adoptador_id):
        query = """
            SELECT 
                p.id_peluche,
                p.nombre,
                p.descripcion,
                p.visitas,
                p.donador_id,
                p.adoptador_id,
                p.created_at,
                p.updated_at,
                d.nombre AS donador_nombre,
                d.apellido AS donador_apellido,
                a.nombre AS adoptador_nombre,
                a.apellido AS adoptador_apellido
            FROM peluches p
            LEFT JOIN usuarios d ON p.donador_id = d.id_usuario
            LEFT JOIN usuarios a ON p.adoptador_id = a.id_usuario
            WHERE p.adoptador_id = %(adoptador_id)s
            ORDER BY p.id_peluche;
        """
        data = {"adoptador_id": adoptador_id}
        resultados = connectToMySQL(DB).query_db(query, data)
        peluches = []
        for peluche in resultados:
            peluches.append(cls(peluche))
        return peluches

    @classmethod
    def buscar_por_nombre_y_donador(cls, nombre, donador_id, excluir_id=None):
        if excluir_id:
            query = """
                SELECT 
                    p.id_peluche,
                    p.nombre,
                    p.descripcion,
                    p.visitas,
                    p.donador_id,
                    p.adoptador_id,
                    p.created_at,
                    p.updated_at
                FROM peluches p
                WHERE p.nombre = %(nombre)s 
                  AND p.donador_id = %(donador_id)s
                  AND p.id_peluche != %(id_peluche)s;
            """
            data = {
                "nombre": nombre,
                "donador_id": donador_id,
                "id_peluche": excluir_id
            }
        else:
            query = """
                SELECT 
                    p.id_peluche,
                    p.nombre,
                    p.descripcion,
                    p.visitas,
                    p.donador_id,
                    p.adoptador_id,
                    p.created_at,
                    p.updated_at
                FROM peluches p
                WHERE p.nombre = %(nombre)s 
                  AND p.donador_id = %(donador_id)s;
            """
            data = {
                "nombre": nombre,
                "donador_id": donador_id
            }

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
            UPDATE peluches
            SET 
                nombre = %(nombre)s,
                descripcion = %(descripcion)s,
                updated_at = NOW()
            WHERE id_peluche = %(id_peluche)s;
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def adoptar(cls, data):
        query = """
            UPDATE peluches
            SET 
                adoptador_id = %(adoptador_id)s,
                updated_at = NOW()
            WHERE id_peluche = %(id_peluche)s;
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def sumar_visita(cls, id):
        query = """
            UPDATE peluches
            SET 
                visitas = visitas + 1
            WHERE id_peluche = %(id_peluche)s;
        """
        data = {"id_peluche": id}
        return connectToMySQL(DB).query_db(query, data)

    # ------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------
    @classmethod
    def eliminar(cls, id):
        query = """
            DELETE FROM peluches
            WHERE id_peluche = %(id_peluche)s;
        """
        data = {"id_peluche": id}
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

        donador_id = datos.get("donador_id")
        excluir_id = datos.get("id_peluche")
        if donador_id and datos["nombre"].strip():
            existente = Peluches.buscar_por_nombre_y_donador(
                datos["nombre"].strip(),
                donador_id,
                excluir_id
            )
            if existente:
                flash("Ya tienes un peluche registrado con ese nombre.", "danger")
                es_valido = False

        return es_valido