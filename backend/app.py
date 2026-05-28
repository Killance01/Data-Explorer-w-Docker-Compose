import os
import socket
from flask import Flask
from prometheus_client import make_wsgi_app, Counter
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

# Métrica para contar las solicitudes
REQUEST_COUNT = Counter('backend_requests_total', 'Total de solicitudes recibidas en este backend', ['method', 'endpoint'])

# Obtenemos el número de instancia desde una variable de entorno
INSTANCE_ID = os.environ.get('INSTANCE_ID', 'Desconocida')

@app.route('/')
def index():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    hostname = socket.gethostname()
    return {
        "status": "success",
        "message": f"Hola desde el Backend Instancia #{INSTANCE_ID}",
        "container_id": hostname
    }, 200

# Integramos prometheus_client para exponer la ruta /metrics
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)