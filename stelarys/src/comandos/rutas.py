from stelarys.src.utiles.imports import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Command:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=100,
            pool_maxsize=100,
            max_retries=1
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        self.found_routes = []
        self.wordlist_dir = os.path.join("stelarys", "data", "wordlists")
        self.lock = threading.Lock()
        
    def run(self, argumentos):
        if not argumentos:
            print("")
            print(f"      {GRAY}({R}#{GRAY}) {W}Scanea rutas http/https con grandes wordlist")
            print("")
            print(f"      {GRAY}({G}!{GRAY}) {O}Ejemplos de como usar el comando")
            print("")
            print(f"        {GRAY}→ {W}rutas {G}localhost:8080")
            print(f"        {GRAY}→ {W}rutas {G}192.168.1.100")
            print("")
            print(f"      {GRAY}({G}#{GRAY}) {GRAY}→ {W}Una vez usado te mostrara las rutas encontradas")
            print("")
            return
            
        target = argumentos[0]
        threads = int(argumentos[1]) if len(argumentos) > 1 else 50
        
        print("")
        print(f"        {GRAY}({O}!{GRAY}) {W}Scaneando las rutas {GRAY}- {W}Target: {G}{target}")
        
        try:
            wordlist_type = self.select_wordlist()
            wordlist_file = self.setup_wordlist(wordlist_type)
            self.scan_routes(target, threads, wordlist_file)
            
            if self.found_routes:
                self.interactive_requests()
                
        except KeyboardInterrupt:
            print("")
            print(f"        {GRAY}({R}#{GRAY}) {LR}Escaneo interrumpido por el usuario")
            print("")
        except Exception as e:
            print("")
            print(f"        {GRAY}({R}-{GRAY}) {LR}Error en el escaneo: {e}")
            print("")

    def select_wordlist(self):
        print("")
        print(f"        {GRAY}({G}?{GRAY}) {W}Selecciona el tamaño de wordlist:")
        print("")
        print(f"            {G}1{GRAY}. {R}Pequeña {GRAY}({LR}~2K rutas{GRAY}) - {W}Rapida")
        print(f"            {G}2{GRAY}. {O}Mediana {GRAY}({LR}~10K rutas{GRAY}) - {W}Equilibrada") 
        print(f"            {G}3{GRAY}. {G}Grande {GRAY}({LR}~50K rutas{GRAY}) - {W}Completa")
        
        while True:
            try:
                print("")
                choice = input(f"           {GRAY}({LR}>{GRAY}) {W}Opcion {GRAY}({G}1{GRAY}/{G}2{GRAY}/{G}3{GRAY}){W}: ").strip()
                if choice in ['1', '2', '3']:
                    return choice
                else:
                    print("")
                    print(f"            {GRAY}({R}#{GRAY}) {LR}Opcion invalida. Usa 1, 2 o 3")
            except KeyboardInterrupt:
                raise
            except:
                print("")
                print(f"            {GRAY}({R}#{GRAY}) {LR}Entrada invalida")

    def create_wordlist_dir(self):
        if not os.path.exists(self.wordlist_dir):
            os.makedirs(self.wordlist_dir)

    def download_wordlist(self, wordlist_type):
        print("")
        
        if wordlist_type == "1":
            urls = [
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt",
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/api/api-endpoints.txt"
            ]
            filename = "small_wordlist.txt"
        elif wordlist_type == "2":
            urls = [
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/directory-list-2.3-medium.txt",
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/api/api-endpoints.txt"
            ]
            filename = "medium_wordlist.txt"
        else:
            urls = [
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/directory-list-2.3-big.txt",
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/big.txt",
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/api/api-endpoints.txt"
            ]
            filename = "big_wordlist.txt"
        
        all_routes = set()
        wordlist_path = os.path.join(self.wordlist_dir, filename)
        
        for url in urls:
            try:
                file_name = url.split('/')[-1]
                print(f"            {GRAY}({LR}*{GRAY}) {W}Descargando: {G}{file_name}")
                response = requests.get(url, timeout=60)
                response.raise_for_status()
                
                routes = response.text.strip().split('\n')
                count = 0
                for route in routes:
                    route = route.strip()
                    if route and not route.startswith('#') and len(route) < 50:
                        all_routes.add(route)
                        count += 1
                        
            except Exception as e:
                print(f"        {GRAY}({LR}#{GRAY}) {W}Error descargando {url}: {e}")
        
        with open(wordlist_path, 'w', encoding='utf-8') as f:
            for route in sorted(all_routes):
                f.write(f"{route}\n")
        
        print("")
        print(f"          {GRAY}({R}#{GRAY}) {W}Wordlist guardada: {G}{len(all_routes)} rutas")
        
        return wordlist_path

    def load_wordlist(self, wordlist_file):
        if not os.path.exists(wordlist_file):
            return []
        
        routes = []
        with open(wordlist_file, 'r', encoding='utf-8') as f:
            for line in f:
                route = line.strip()
                if route and not route.startswith('#'):
                    routes.append(route)
        
        return routes

    def check_route(self, base_url, route):
        try:
            if not route.startswith('/'):
                route = '/' + route
            
            url = urljoin(base_url, route)
            response = self.session.get(url, timeout=5, allow_redirects=False, verify=False)
            
            status_code = response.status_code
            content_length = len(response.content)
            
            if status_code in [200, 201, 202, 301, 302, 401, 403, 405, 500]:
                result = {
                    'url': url,
                    'status': status_code,
                    'length': content_length,
                    'content_type': response.headers.get('content-type', 'unknown'),
                    'server': response.headers.get('server', 'unknown')
                }
                
                with self.lock:
                    self.found_routes.append(result)
                
                return result
                
        except:
            pass
        
        return None

    def get_status_icon(self, status_code):
        if status_code in [200, 201, 202]:
            return f"{G}+{GRAY}"
        elif status_code in [301, 302]:
            return f"{O}~{GRAY}"
        elif status_code in [401, 403]:
            return f"{R}!{GRAY}"
        elif status_code >= 500:
            return f"{LR}X{GRAY}"
        else:
            return f"{W}?{GRAY}"

    def get_status_color(self, status_code):
        if status_code in [200, 201, 202]:
            return G
        elif status_code in [301, 302]:
            return O
        elif status_code in [401, 403]:
            return R
        elif status_code >= 500:
            return LR
        else:
            return W

    def print_progress_bar(self, current, total, start_time):
        percent = (current / total) * 100
        elapsed = time.time() - start_time
        
        if percent < 33:
            bar_color = LR
        elif percent < 66:
            bar_color = O
        else:
            bar_color = G
        
        filled = int(40 * current / total)
        bar = "█" * filled + "░" * (40 - filled)
        
        sys.stdout.write(f"\r        {GRAY}({bar_color}#{GRAY}) {bar_color}[{bar}] {percent:6.2f}% {GRAY}| {W}{current}/{total} {GRAY}| {W}{elapsed:.1f}s{RESET}")
        sys.stdout.flush()

    def scan_routes(self, target, threads, wordlist_file):
        print("")
        print(f"             {R}- {W}Target: {G}{target}")
        print(f"             {R}- {W}Threads: {G}{threads}")
        
        routes = self.load_wordlist(wordlist_file)
        if not routes:
            print("")
            print(f"          {GRAY}({R}-{GRAY}) {LR}No se pudo cargar la wordlist")
            return
        
        
        if not target.startswith(('http://', 'https://')):
            if ':443' in target or 'https' in target.lower():
                target = 'https://' + target.replace(':443', '')
            else:
                target = 'http://' + target
        
        start_time = time.time()
        completed = 0
        
        print("")
        print(f"        {GRAY}({LR}#{GRAY}) {W}Iniciando escaneo...")
        print("")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {
                executor.submit(self.check_route, target, route): route 
                for route in routes
            }
            
            for future in as_completed(futures):
                completed += 1
                result = future.result()
                
                if completed % 25 == 0 or completed == len(routes):
                    self.print_progress_bar(completed, len(routes), start_time)
        
        elapsed_total = time.time() - start_time
        
        print("")
        print("")
        print(f"          {GRAY}({R}*{GRAY}) {W}Escaneo completado en {G}{elapsed_total:.1f} segundos")
        print(f"          {GRAY}({R}*{GRAY}) {W}Rutas encontradas: {G}{len(self.found_routes)}")
        
        if self.found_routes:
            print("")
            print(f"        {GRAY}({G}#{GRAY}) {W}Resumen de rutas encontradas:")
            print("")
            
            by_status = {}
            for route in self.found_routes:
                status = route['status']
                if status not in by_status:
                    by_status[status] = []
                by_status[status].append(route)
            
            for status in sorted(by_status.keys()):
                routes_list = by_status[status]
                icon = self.get_status_icon(status)
                status_color = self.get_status_color(status)
                print(f"            {GRAY}({icon}) {status_color}Codigo {status} {GRAY}({W}{len(routes_list)} rutas{GRAY}):")
                print("")
                
                for i, route in enumerate(sorted(routes_list, key=lambda x: x['url'])):
                    if i < 8:
                        content_type = route.get('content_type', 'unknown').split(';')[0]
                        print(f"                {G}{i+1}{GRAY}. {W}{route['url']} {GRAY}| {W}{route['length']} bytes {GRAY}| {W}{content_type}")
                    elif i == 8:
                        print(f"                {GRAY}... y {W}{len(routes_list) - 8} {GRAY}rutas más")
                        break
                print("")
        else:
            print("")
            print(f"        {GRAY}({R}-{GRAY}) {LR}No se encontraron rutas accesibles")
            print("")
            print(f"        {GRAY}({O}!{GRAY}) {W}Esto puede deberse a:")
            print(f"            {GRAY}→ {W}El servidor bloquea escaneos automatizados")
            print(f"            {GRAY}→ {W}Firewall o WAF activo")
            print(f"            {GRAY}→ {W}El servidor no está activo")
            print(f"            {GRAY}→ {W}Todas las rutas devuelven 404")
            print("")

    def interactive_requests(self):
        print(f"        {GRAY}({G}?{GRAY}) {W}¿Quieres hacer peticiones a las rutas encontradas?")
        print("")
        print(f"            {G}1{GRAY}. {W}GET {GRAY}- {W}Peticion GET simple")
        print(f"            {G}2{GRAY}. {W}POST {GRAY}- {W}Peticion POST con datos")
        print(f"            {G}3{GRAY}. {W}PUT {GRAY}- {W}Peticion PUT")
        print(f"            {G}4{GRAY}. {W}DELETE {GRAY}- {W}Peticion DELETE")
        print(f"            {G}5{GRAY}. {W}OPTIONS {GRAY}- {W}Ver metodos permitidos")
        print(f"            {G}6{GRAY}. {W}HEAD {GRAY}- {W}Solo headers")
        print(f"            {G}7{GRAY}. {W}cURL {GRAY}- {W}Generar comando cURL")
        print(f"            {G}8{GRAY}. {R}Salir")
        
        while True:
            try:
                print("")
                choice = input(f"           {GRAY}({LR}>{GRAY}) {W}Selecciona opcion {GRAY}({G}1-8{GRAY}){W}: ").strip()
                
                if choice == "8":
                    print("")
                    break
                elif choice in ["1", "2", "3", "4", "5", "6", "7"]:
                    self.show_routes_menu()
                    try:
                        print("")
                        route_index = int(input(f"           {GRAY}({LR}>{GRAY}) {W}Numero de ruta: ")) - 1
                        if 0 <= route_index < len(self.found_routes):
                            selected_route = self.found_routes[route_index]
                            self.execute_request(choice, selected_route)
                        else:
                            print("")
                            print(f"        {GRAY}({R}-{GRAY}) {LR}Numero de ruta invalido")
                    except ValueError:
                        print("")
                        print(f"        {GRAY}({R}-{GRAY}) {LR}Entrada invalida")
                else:
                    print("")
                    print(f"        {GRAY}({R}-{GRAY}) {LR}Opcion invalida")
                    
            except KeyboardInterrupt:
                print("")
                break

    def show_routes_menu(self):
        print("")
        print(f"        {GRAY}({G}+{GRAY}) {W}Rutas disponibles:")
        print("")
        for i, route in enumerate(self.found_routes):
            status_color = self.get_status_color(route['status'])
            print(f"            {G}{i+1}{GRAY}. {W}{route['url']} {GRAY}[{status_color}{route['status']}{GRAY}]")

    def execute_request(self, method_choice, route_info):
        url = route_info['url']
        
        try:
            if method_choice == "1":  # GET
                response = self.session.get(url, verify=False, timeout=10)
                self.show_response(response, "GET", url)
                
            elif method_choice == "2":  # POST
                print("")
                data = input(f"           {GRAY}({LR}>{GRAY}) {W}Datos POST (JSON/form-data) [Enter para vacio]: ").strip()
                headers = {'Content-Type': 'application/json'}
                
                if data:
                    try:
                        json_data = json.loads(data)
                        response = self.session.post(url, json=json_data, verify=False, timeout=10)
                    except json.JSONDecodeError:
                        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                        response = self.session.post(url, data=data, headers=headers, verify=False, timeout=10)
                else:
                    response = self.session.post(url, verify=False, timeout=10)
                    
                self.show_response(response, "POST", url)
                
            elif method_choice == "3":  # PUT
                print("")
                data = input(f"           {GRAY}({LR}>{GRAY}) {W}Datos PUT (JSON) [Enter para vacio]: ").strip()
                if data:
                    try:
                        json_data = json.loads(data)
                        response = self.session.put(url, json=json_data, verify=False, timeout=10)
                    except json.JSONDecodeError:
                        response = self.session.put(url, data=data, verify=False, timeout=10)
                else:
                    response = self.session.put(url, verify=False, timeout=10)
                self.show_response(response, "PUT", url)
                
            elif method_choice == "4":  # DELETE
                response = self.session.delete(url, verify=False, timeout=10)
                self.show_response(response, "DELETE", url)
                
            elif method_choice == "5":  # OPTIONS
                response = self.session.options(url, verify=False, timeout=10)
                self.show_response(response, "OPTIONS", url)
                
            elif method_choice == "6":  # HEAD
                response = self.session.head(url, verify=False, timeout=10)
                self.show_response(response, "HEAD", url)
                
            elif method_choice == "7":  # cURL
                self.generate_curl(url)
                
        except Exception as e:
            print("")
            print(f"        {GRAY}({R}-{GRAY}) {LR}Error en la peticion: {e}")

    def show_response(self, response, method, url):
        print("")
        print(f"        {GRAY}({G}+{GRAY}) {W}Respuesta {G}{method} {W}a {G}{url}")
        print(f"        {GRAY}({G}+{GRAY}) {W}Status Code: {G}{response.status_code}")
        print("")
        print(f"        {GRAY}({G}#{GRAY}) {W}Headers:")
        for header, value in list(response.headers.items())[:5]:
            print(f"            {GRAY}→ {W}{header}: {G}{value}")
        if len(response.headers) > 5:
            print(f"            {GRAY}... y {W}{len(response.headers) - 5} {GRAY}headers más")
        
        print("")
        print(f"        {GRAY}({G}#{GRAY}) {W}Contenido {GRAY}({W}{len(response.content)} bytes{GRAY}):")
        print("")
        try:
            if 'application/json' in response.headers.get('content-type', ''):
                json_data = response.json()
                content = json.dumps(json_data, indent=2, ensure_ascii=False)[:800]
                print(f"            {G}{content}")
                if len(str(json_data)) > 800:
                    print(f"            {GRAY}... (truncado)")
            else:
                content = response.text[:800]
                print(f"            {W}{content}")
                if len(response.text) > 800:
                    print(f"            {GRAY}... (truncado)")
        except:
            content = response.text[:500]
            print(f"            {W}{content}")
        print("")

    def generate_curl(self, url):
        print("")
        print(f"        {GRAY}({G}+{GRAY}) {W}Comandos cURL para {G}{url}{W}:")
        print("")
        print(f"            {GRAY}→ {W}GET:    {G}curl -X GET '{url}'")
        print(f"            {GRAY}→ {W}POST:   {G}curl -X POST '{url}' -H 'Content-Type: application/json' -d '{{}}'")
        print(f"            {GRAY}→ {W}PUT:    {G}curl -X PUT '{url}' -H 'Content-Type: application/json' -d '{{}}'")
        print(f"            {GRAY}→ {W}DELETE: {G}curl -X DELETE '{url}'")
        print(f"            {GRAY}→ {W}HEAD:   {G}curl -I '{url}'")
        print("")

    def setup_wordlist(self, wordlist_type):
        self.create_wordlist_dir()
        
        wordlist_files = {
            "1": os.path.join(self.wordlist_dir, "small_wordlist.txt"),
            "2": os.path.join(self.wordlist_dir, "medium_wordlist.txt"), 
            "3": os.path.join(self.wordlist_dir, "big_wordlist.txt")
        }
        
        wordlist_file = wordlist_files[wordlist_type]
        
        if os.path.exists(wordlist_file):
            routes = self.load_wordlist(wordlist_file)
            if len(routes) < 100:
                print("")
                print(f"        {GRAY}({O}!{GRAY}) {W}Wordlist incompleta, descargando...")
                return self.download_wordlist(wordlist_type)
            else:
                print("")
                print(f"        {GRAY}({G}+{GRAY}) {W}Wordlist cargada: {G}{len(routes)} rutas")
                return wordlist_file
        else:
            return self.download_wordlist(wordlist_type)