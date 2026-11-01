import http.server
import socketserver
import webbrowser
import os

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class UnityWebGLRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Cabeceras requeridas para WebGL con compresión Gzip
        if self.path.endswith('.unityweb'):
            self.send_header('Content-Encoding', 'gzip')
        if '.wasm' in self.path:
            self.send_header('Content-Type', 'application/wasm')
        elif '.js' in self.path:
            self.send_header('Content-Type', 'application/javascript')
        elif '.data' in self.path:
            self.send_header('Content-Type', 'application/octet-stream')
        super().end_headers()

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    print(f"=====================================================")
    print(f"  Servidor Local de Botánica Interactiva (WebGL)")
    print(f"  URL: http://localhost:{PORT}/index.html")
    print(f"=====================================================")
    print("Presiona Ctrl + C en esta ventana para detener el servidor.\n")
    
    # Abrir navegador automáticamente
    webbrowser.open(f"http://localhost:{PORT}/index.html")
    
    with socketserver.TCPServer(("", PORT), UnityWebGLRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")

