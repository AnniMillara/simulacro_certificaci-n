from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.entidad import Entidades
from flask_app.models.categoria import Categorias

@app.route("/dashboard")
def dashboard():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))
    entidades = Entidades.ver_todas()
    return render_template("entidad_lista.html", entidades=entidades)

@app.route("/entidad/nueva")
def nueva_entidad():
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))
    return render_template("entidad_form.html",
                           entidad=None,
                           categorias=Categorias.ver_todas())

@app.route("/entidad/crear", methods=["POST"])
def crear_entidad():
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))
    datos = {
        "nombre": request.form.get("nombre", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
        "fecha": request.form.get("fecha") or None,
        "precio": request.form.get("precio") or None,
        "stock": request.form.get("stock") or None,
        "categoria_id": request.form.get("categoria_id"),
        "usuario_id": session["id_usuario"],
    }
    if not Entidades.validar(datos):
        return redirect(url_for("nueva_entidad"))
    Entidades.guardar(datos)
    flash("Registro guardado.", "success")
    return redirect(url_for("dashboard"))

@app.route("/entidad/detalle/<int:id>")
def detalle_entidad(id):
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))
    entidad = Entidades.buscar_id(id)
    if not entidad:
        flash("No encontrado.", "danger")
        return redirect(url_for("dashboard"))
    return render_template("entidad_detalle.html", entidad=entidad)

@app.route("/entidad/editar/<int:id>")
def editar_entidad(id):
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))
    entidad = Entidades.buscar_id(id)
    if not entidad:
        return redirect(url_for("dashboard"))
    if entidad.usuario_id != session["id_usuario"]:
        flash("No puedes editar esto.", "danger")
        return redirect(url_for("dashboard"))
    return render_template("entidad_form.html",
                           entidad=entidad,
                           categorias=Categorias.ver_todas())

@app.route("/entidad/modificar/<int:id>", methods=["POST"])
def modificar_entidad(id):
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))
    entidad = Entidades.buscar_id(id)
    if not entidad or entidad.usuario_id != session["id_usuario"]:
        flash("No puedes modificar esto.", "danger")
        return redirect(url_for("dashboard"))
    datos = {
        "id_entidad": id,
        "nombre": request.form.get("nombre", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
        "fecha": request.form.get("fecha") or None,
        "precio": request.form.get("precio") or None,
        "stock": request.form.get("stock") or None,
        "categoria_id": request.form.get("categoria_id"),
    }
    if not Entidades.validar(datos):
        return redirect(url_for("editar_entidad", id=id))
    Entidades.modificar(datos)
    flash("Registro actualizado.", "success")
    return redirect(url_for("dashboard"))

@app.route("/entidad/confirmar_eliminar/<int:id>")
def confirmar_eliminar_entidad(id):
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))
    entidad = Entidades.buscar_id(id)
    if not entidad or entidad.usuario_id != session["id_usuario"]:
        return redirect(url_for("dashboard"))
    return render_template(
        "confirmar_eliminar.html",
        mensaje=f"Vas a eliminar '{entidad.nombre}'. Esta acción no se puede deshacer.",
        accion=url_for("eliminar_entidad", id=id),
        cancelar=url_for("dashboard")
    )

@app.route("/entidad/eliminar/<int:id>")
def eliminar_entidad(id):
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))
    entidad = Entidades.buscar_id(id)
    if not entidad or entidad.usuario_id != session["id_usuario"]:
        flash("No puedes eliminar esto.", "danger")
        return redirect(url_for("dashboard"))
    Entidades.eliminar(id)
    flash("Registro eliminado.", "success")
    return redirect(url_for("dashboard"))