from flask import Flask, render_template, session, redirect, url_for
from config.settings import Config

app = Flask(__name__)
app.config.from_object(Config)

# Register Blueprints
from routes.upload_routes import upload_bp
from routes.test_routes import test_bp
from routes.result_routes import result_bp
from routes.recruiter_routes import recruiter_bp
from routes.auth_routes import auth_bp
from routes.employee_routes import employee_bp
from routes.admin_routes import admin_bp

app.register_blueprint(upload_bp)
app.register_blueprint(test_bp)
app.register_blueprint(result_bp)
app.register_blueprint(recruiter_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def index():
    user = session.get('user')
    if user:
        if user['role'] == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif user['role'] == 'recruiter':
            return redirect(url_for('recruiter.dashboard'))
        elif user['role'] == 'employee':
            return redirect(url_for('employee.dashboard'))
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)
