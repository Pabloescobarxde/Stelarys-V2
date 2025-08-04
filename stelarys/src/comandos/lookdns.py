from stelarys.src.utiles.imports import *

class Command:
    def run(self, args):
        if len(args) < 1:
            print("")
            print(f"      {GRAY}({R}#{GRAY}) {W}Obten los dns de un dominio")
            print("")
            print(f"      {GRAY}({G}!{GRAY}) {O}Ejemplos de como usar el comando")
            print("")
            print(f"        {GRAY}→ {W}lookdns {G}mc.universocraft.com")
            print("")
            print(f"      {GRAY}({G}#{GRAY}) {GRAY}→ {W} Una ves usada te dara los dns del dominio")
            print("")
            return

        domain = args[0]


        try:
            ipaddress.ip_address(domain)
            print(f"       {GRAY}({R}!{GRAY}) {LR}No se puede realizar una consulta DNS directa sobre una IP. Usa un dominio válido.")
            return
        except ValueError:
            pass 

        print("")
        print(f"       {GRAY}({G}*{GRAY}) {W}Buscando información para {LR}{domain}")
        print("")

        dns_records = [
            'A', 'AAAA', 'CNAME', 'MX', 'NS', 'PTR', 'SOA', 'SRV', 'TXT',
            'CAA', 'SPF', 'NAPTR'
        ]

        try:

            dns.resolver.resolve(domain, 'A')  
        except dns.resolver.NXDOMAIN:
            print(f"       {GRAY}({R}!{GRAY}) {LR}El dominio no existe.")
            return
        except dns.resolver.NoNameservers:
            print(f"       {GRAY}({R}!{GRAY}) {LR}El dominio no existe. Verifique intente de nuevo.")
            return
        except Exception as e:
            print(f"       {GRAY}({R}!{GRAY}) {LR}Error al consultar el dominio: ")
            return

       
        for rtype in dns_records:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                print(f"        {GRAY}({R}#{GRAY}) {W}{rtype} Records:")
                for rdata in answers:
                    print(f"          {GRAY}({G}#{GRAY}) {LR}{rdata.to_text()}")
                print("")
            except dns.resolver.NoAnswer:
                continue  
            except dns.resolver.NXDOMAIN:
                
                print(f"        {GRAY}({R}!{GRAY}) {LR}Dominio inválido.")
                return
            except Exception:
                continue  
