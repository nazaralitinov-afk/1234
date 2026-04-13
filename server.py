from flask import Flask, request, send_file
import json
import io
from datetime import datetime
import os

app = Flask(__name__)

PIXEL_GIF = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'

@app.route('/pixel.gif')
def track():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent', 'Unknown')
    ref = request.headers.get('Referer', 'Direct')
    
    victim = {
        "timestamp": datetime.now().isoformat(),
        "ip": ip,
        "user_agent": ua,
        "referer": ref
    }
    
    print(f"[Fox] +1: {ip}")
    
    try:
        with open('/tmp/victims.json', 'r') as f:
            data = json.load(f)
    except:
        data = []
    
    data.append(victim)
    
    with open('/tmp/victims.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    return send_file(io.BytesIO(PIXEL_GIF), mimetype='image/gif')

@app.route('/view')
def view():
    try:
        with open('/tmp/victims.json', 'r') as f:
            data = json.load(f)
    except:
        data = []
    
    html = "<h1>🦊 ЖЕРТВЫ</h1><pre>" + json.dumps(data, indent=2) + "</pre>"
    return html

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)