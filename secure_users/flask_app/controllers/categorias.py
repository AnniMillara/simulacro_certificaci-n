from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.categoria import Categorias
from flask_app.models.entidad import Entidades

@app.route("/categorias")
def lista_categorias():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))
    categorias = Categorias.ver_todas()
    return render_template("categoria_lista.html", categorias=categorias)

@app.route("/categorias/nueva")
def nueva_categoria():
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))
    return render_template("categoria_form.html", categoria=None)

@app.route("/categorias/crear", methods=["POST"])
def crear_categoria():
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))
    datos = {
        "nombre": request.form.get("nombre", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
    }
    if not Categorias.validar(datos):
        return redirect(url_for("nueva_categoria"))
    Categorias.guardar(datos)
    flash("Categoría guardada.", "success")
    return redirect(url_for("lista_categorias"))

@app.route("/categorias/editar/<int:id>")
def editar_categoria(id):
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))
    categoria = Categorias.buscar_id(id)
    if not categoria:
        flash("Categoría no encontrada.", "danger")
        return redirect(url_for("lista_categorias"))
    return render_template("categoria_form.html", categoria=categoria)

@app.route("/categorias/modificar/<int:id>", methods=["POST"])
def modificar_categoria(id):
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))
    categoria = Categorias.buscar_id(id)
    if not categoria:
        return redirect(url_for("lista_categorias"))
    datos = {
        "id_categoria": id,
        "nombre": request.form.get("nombre", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
    }
    if not Categorias.validar(datos):
        return redirect(url_for("editar_categoria", id=id))
    Categorias.modificar(datos)
    flash("Categoría modificada.", "success")
    return redirect(url_for("lista_categorias"))

@app.route("/categorias/eliminar/<int:id>")
def eliminar_categoria(id):
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))
    # Bloquear borrado si tiene entidades asociadas
    from flask_app.models.entidad import Entidades
    query = "SELECT COUNT(*) AS total FROM entidades WHERE categoria_id = %(id_categoria)s;"
    from flask_app.config.mysqlconnection import connectToMySQL
    resultado = connectToMySQL("esquema_certificacion").query_db(query, {"id_categoria": id})
    if resultado and resultado[0]["total"] > 0:
        flash("No puedes eliminar una categoría con registros asociados.", "danger")
        return redirect(url_for("lista_categorias"))
    Categorias.eliminar(id)
    flash("Categoría eliminada.", "success")
    return redirect(url_for("lista_categorias"))