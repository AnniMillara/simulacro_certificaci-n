from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.peluche import Peluches


@app.route("/peluche")
def peluches():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))
    peluches = Peluches.ver_todas()
    return render_template("peluche_lista.html", peluches=peluches)


@app.route("/peluche/nuevo")
def nuevo_peluche():
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))
    datos_previos = session.pop("form_peluche", None)
    return render_template("peluche_form.html",
                           peluche=None,
                           datos=datos_previos)


@app.route("/peluche/crear", methods=["POST"])
def crear_peluche():
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))

    datos = {
        "nombre": request.form.get("nombre", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
        "donador_id": session["id_usuario"],
        "adoptador_id": None,
    }
    if not Peluches.validar(datos):
        session["form_peluche"] = {
            "nombre": datos["nombre"],
            "descripcion": datos["descripcion"]
        }
        return redirect(url_for("nuevo_peluche"))

    Peluches.guardar(datos)
    flash("Registro guardado. ദ്ദി( ˘̀ ֊ ˘́)", "success")
    return redirect(url_for("peluches"))


@app.route("/peluche/detalle/<int:id>")
def detalle_peluche(id):
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))

    peluche = Peluches.buscar_id(id)
    if not peluche:
        flash("Ups parece que tu amigo no fue encontrado. (,,•᷄﹏•᷅,,)", "danger")
        return redirect(url_for("peluches"))

    if peluche.donador_id != session["id_usuario"]:
        Peluches.sumar_visita(id)
        peluche = Peluches.buscar_id(id)

    return render_template("peluche_detalle.html", peluche=peluche)


@app.route("/peluche/editar/<int:id>")
def editar_peluche(id):
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))

    peluche = Peluches.buscar_id(id)
    if not peluche:
        return redirect(url_for("peluches"))
    if peluche.donador_id != session["id_usuario"]:
        flash("No puedes editar esto, no te pertenece... (ㆆ_ㆆ)", "danger")
        return redirect(url_for("peluches"))

    datos_previos = session.pop("form_peluche", None)

    return render_template("peluche_form.html",
                           peluche=peluche,
                           datos=datos_previos)


@app.route("/peluche/modificar/<int:id>", methods=["POST"])
def modificar_peluche(id):
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))

    peluche = Peluches.buscar_id(id)
    if not peluche or peluche.donador_id != session["id_usuario"]:
        flash("Ups, parece que algo salió mal, ( ,,⩌'︿'⩌,,)", "danger")
        return redirect(url_for("peluches"))

    datos = {
        "id_peluche": id,
        "nombre": request.form.get("nombre", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
        "donador_id": session["id_usuario"],
    }

    if not Peluches.validar(datos):
        session["form_peluche"] = {
            "nombre": datos["nombre"],
            "descripcion": datos["descripcion"]
        }
        return redirect(url_for("editar_peluche", id=id))

    Peluches.modificar(datos)
    flash("Registro actualizado. ദ്ദി◝ ⩊ ◜.ᐟ", "success")
    return redirect(url_for("peluches"))


@app.route("/peluche/adoptar/<int:id>", methods=["POST"])
def adoptar_peluche(id):
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))

    peluche = Peluches.buscar_id(id)
    if not peluche:
        flash("Peluche no encontrado.", "danger")
        return redirect(url_for("peluches"))

    if peluche.adoptador_id is not None:
        flash("Este peluche ya fue adoptado. (｡•́︿•̀｡)", "danger")
        return redirect(url_for("peluches"))

    if peluche.donador_id == session["id_usuario"]:
        flash("No puedes adoptar tu propio peluche. (¬_¬)", "danger")
        return redirect(url_for("peluches"))

    datos = {
        "id_peluche": id,
        "adoptador_id": session["id_usuario"],
    }
    Peluches.adoptar(datos)
    flash("¡Felicidades!! .✺◟(＾∇＾)◞✺", "success")
    return redirect(url_for("peluches"))


@app.route("/peluche/confirmar_eliminar/<int:id>")
def confirmar_eliminar_peluche(id):
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))

    peluche = Peluches.buscar_id(id)
    if not peluche or peluche.donador_id != session["id_usuario"]:
        flash("Ups, parece que algo salió mal, (,,Ծ‸Ծ,, )", "danger")
        return redirect(url_for("peluches"))

    return render_template(
        "confirmar_eliminar.html",
        mensaje=f"Vas a eliminar '{peluche.nombre}'. Esta acción no se puede deshacer.",
        accion=url_for("eliminar_peluche", id=id),
        cancelar=url_for("peluches")
    )


@app.route("/peluche/eliminar/<int:id>")
def eliminar_peluche(id):
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))

    peluche = Peluches.buscar_id(id)
    if not peluche or peluche.donador_id != session["id_usuario"]:
        flash("No puedes eliminar esto.", "danger")
        return redirect(url_for("peluches"))

    Peluches.eliminar(id)
    flash("Registro eliminado.", "success")
    return redirect(url_for("peluches"))