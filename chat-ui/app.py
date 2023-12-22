from flask import Flask, send_from_directory, current_app
import os

app = Flask(__name__)

@app.route('/_next/static/<path:path>')
def serve_next_static(path):
    return send_from_directory(os.path.join(current_app.root_path, 'chat-ui/.next/static'), path)

@app.route('/public/<path:path>')
def serve_public(path):
    return send_from_directory('public', path)

@app.route('/_next/image/<path:path>')
def serve_next_image(path):
    return send_from_directory(os.path.join(current_app.root_path, 'chat-ui/.next/static/media'), path)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(current_app.root_path, 'chat-ui/.next/server/app', path)):
        return send_from_directory(os.path.join(current_app.root_path, 'chat-ui/.next/server/app'), path)
    else:
        return send_from_directory(os.path.join(current_app.root_path, 'chat-ui/.next/server/app'), 'index.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ["CDSW_READONLY_PORT"]))
