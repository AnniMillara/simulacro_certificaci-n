from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app, bcrypt
from flask_app.models.usuario import Usuarios
from flask_app.models.peluche import Peluches


# Inicio
@app.route("/")
def inicio():
    if "id_usuario" in session:
        return redirect(url_for("perfil", id=session["id_usuario"]))
    return render_template("login.html")


# Registro
@app.route("/registro", methods=["POST"])
def registro():
    datos = {
        "nombre": request.form.get("nombre", "").strip(),
        "apellido": request.form.get("apellido", "").strip(),
        "email": request.form.get("email", "").strip(),
        "contrasena": request.form.get("contrasena", "").strip(),
        "confirmar_contrasena": request.form.get("confirmar_contrasena", "").strip(),
    }
    if not Usuarios.validar_registro(datos):
        return redirect(url_for("inicio"))

    hash_pw = bcrypt.generate_password_hash(datos["contrasena"]).decode("utf-8")
    data = {
        "nombre": datos["nombre"],
        "apellido": datos["apellido"],
        "email": datos["email"],
        "contrasena": hash_pw,
    }
    nuevo_id = Usuarios.guardar(data)
    if not nuevo_id:
        flash("No fue posible crear el usuario.", "danger")
        return redirect(url_for("inicio"))

    session["id_usuario"] = nuevo_id
    session["nombre"] = datos["nombre"]
    flash("Usuario creado correctamente.", "success")
    return redirect(url_for("perfil", id=nuevo_id))


# Login
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip()
    contrasena = request.form.get("contrasena", "").strip()

    if not email or not contrasena:
        flash("Email y contraseña son obligatorios.", "danger")
        return redirect(url_for("inicio"))

    usuario = Usuarios.buscar_email(email)
    if not usuario or not bcrypt.check_password_hash(usuario.contrasena, contrasena):
        flash("Email o contraseña incorrectos.", "danger")
        return redirect(url_for("inicio"))

    session["id_usuario"] = usuario.id_usuario
    session["nombre"] = usuario.nombre
    flash("Bienvenido de vuelta.", "success")
    return redirect(url_for("perfil", id=usuario.id_usuario))


# Perfil
@app.route("/perfil/<int:id>")
def perfil(id):
    if "id_usuario" not in session or session["id_usuario"] != id:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))

    usuario = Usuarios.buscar_id(id)
    if not usuario:
        session.clear()
        return redirect(url_for("inicio"))

    donados = Peluches.buscar_donador(id)
    adoptados = Peluches.buscar_adoptante(id)

    return render_template("perfil.html",
                            usuario=usuario,
                            donados=donados,
                            adoptados=adoptados)


# Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada.", "success")
    return redirect(url_for("inicio"))


# Eliminar cuenta
@app.route("/perfil/confirmar_eliminar/<int:id>")
def confirmar_eliminar_usuario(id):
    if "id_usuario" not in session or session["id_usuario"] != id:
        return redirect(url_for("inicio"))

    usuario = Usuarios.buscar_id(id)
    if not usuario:
        return redirect(url_for("inicio"))

    return render_template(
        "confirmar_eliminar.html",
        mensaje=f"Vas a eliminar tu perfil, {usuario.nombre}. Esta acción no se puede deshacer.",
        accion=url_for("eliminar_usuario", id=id),
        cancelar=url_for("perfil", id=id)
    )


@app.route("/perfil/eliminar/<int:id>")
def eliminar_usuario(id):
    if "id_usuario" not in session or session["id_usuario"] != id:
        return redirect(url_for("inicio"))

    Usuarios.eliminar(id)
    session.clear()
    flash("Perfil eliminado.", "success")
    return redirect(url_for("inicio"))