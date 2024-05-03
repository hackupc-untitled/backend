from flask import Flask
#from mi_app.users.views import users_bp
#from mi_app.posts.views import posts_bp

app = Flask(__name__)

# Registrar los blueprints
#app.register_blueprint(users_bp)
#app.register_blueprint(posts_bp)

if __name__ == "__main__":
    app.run(debug=True)


''' EXEMPLE BLUEPRINT
    Un blueprint es un modul de la aplicacio 
    per poder organitzar els endpoints per modul/feature

    from flask import Blueprint

    users_bp = Blueprint("users", __name__)

    @users_bp.route("/users")
    def get_users():
        return "Lista de usuarios"

    @users_bp.route("/users/<int:user_id>")
    def get_user(user_id):
        return f"Información del usuario con ID {user_id}"


'''