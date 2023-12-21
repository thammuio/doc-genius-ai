from flask import Flask, send_from_directory, current_app
import os

app = Flask(__name__)

@app.route('/_next/static/<path:path>')
def serve_next_static(path):
    return send_from_directory(os.path.join(current_app.root_path, '.next/static'), path)

@app.route('/public/<path:path>')
def serve_public(path):
    return send_from_directory('public', path)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(current_app.root_path, '.next/server/app', path)):
        return send_from_directory(os.path.join(current_app.root_path, '.next/server/app'), path)
    else:
        return send_from_directory(os.path.join(current_app.root_path, '.next/server/app'), 'index.html')

if __name__ == '__main__':
    port = int(os.getenv('CDSW_READONLY_PORT', 5000))  # Use CDSW_PUBLIC_PORT if it's set, otherwise default to 5000
    app.run(use_reloader=True, port=port, threaded=True)
