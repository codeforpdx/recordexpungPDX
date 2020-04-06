import os.path
from flask import abort

def register(app):
    # mimic nginx 'try_files' directive for react
    #
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>", methods=["GET", "HEAD", "OPTIONS"])
    def try_files_static_index(path):
        static_path = os.path.join(app.static_folder, path)
        if os.path.exists(static_path) and not os.path.isdir(static_path):
            return app.send_static_file(path)
        else:
            return app.send_static_file("index.html")

    @app.route("/<path:path>", methods=["POST", "PUT", "PATCH", "DELETE"])
    def bad_static_file_http_method(path):
        abort(404)
