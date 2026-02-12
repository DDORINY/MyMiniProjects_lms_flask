from flask import Flask
from config import Config

from routes.main_routes import bp as main_bp
from routes.member_routes import bp as member_bp
from routes.board_routes import bp as board_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ 블루프린트 등록
    app.register_blueprint(main_bp)
    app.register_blueprint(member_bp)
    app.register_blueprint(board_bp)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001, debug=True)
