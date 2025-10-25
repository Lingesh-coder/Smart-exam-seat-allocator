from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)

    load_dotenv()

    CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['MONGODB_URI'] = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/exam_allocator')

    from routes.students import students_bp
    from routes.rooms import rooms_bp
    from routes.subjects import subjects_bp
    from routes.allocations import allocations_bp

    app.register_blueprint(students_bp, url_prefix='/api')
    app.register_blueprint(rooms_bp, url_prefix='/api')
    app.register_blueprint(subjects_bp, url_prefix='/api')
    app.register_blueprint(allocations_bp, url_prefix='/api')

    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Exam Seat Allocator API is running'}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
