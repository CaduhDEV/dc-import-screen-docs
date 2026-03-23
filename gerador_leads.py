from openpyxl import Workbook  # type: ignore
import csv
import random
import string
from datetime import datetime, timedelta

print("=== GERADOR DE LEADS (FULL QA MODE) ===")

qtd_leads = int(input("Quantidade de leads: "))
modo_pais = input("Modo de país (1 = específico | 2 = aleatório global): ")

pais_especifico = None
if modo_pais == "1":
    pais_especifico = input("Digite o país em inglês (ex: Brazil): ")

modo_data = input("Formato de data (1 = fixo | 2 = aleatório): ")

formato_data = None
formato_tipo = None

if modo_data == "1":
    print("\nFormatos disponíveis:")
    print("1 - YYYY-MM-DD")
    print("2 - YYYY/MM/DD")
    print("3 - DD/MM/YYYY")
    print("4 - MM/DD/YYYY")
    print("5 - ISO datetime")
    print("6 - Timestamp (segundos)")
    print("7 - Timestamp (ms)")
    
    escolha = input("Escolha o formato: ")
    
    formatos_map = {
        "1": "%Y-%m-%d",
        "2": "%Y/%m/%d",
        "3": "%d/%m/%Y",
        "4": "%m/%d/%Y",
        "5": "%Y-%m-%dT%H:%M:%S"
    }
    
    formato_data = formatos_map.get(escolha, "%Y-%m-%d")
    formato_tipo = escolha


usar_especiais = input("Testar caracteres especiais? (s/n): ").lower() == "s"
campos_especiais = []

if usar_especiais:
    print("\nCampos: nome, email, empresa, endereco, bairro, cidade, notas, site")
    campos_input = input("Digite os campos separados por vírgula: ")
    campos_especiais = [c.strip().lower() for c in campos_input.split(",")]

def aplicar_especiais(texto):
    especiais = ["‍","‌","‎","‏","✓","★","∞","🔥","💀","🚀","ç","ã","é","漢"]
    return texto + random.choice(especiais)

def maybe_special(campo, valor):
    if usar_especiais and campo in campos_especiais:
        return aplicar_especiais(valor)
    return valor

ddi_map = {
    "Afghanistan":"93","Albania":"355","Algeria":"213","Andorra":"376","Angola":"244",
    "Argentina":"54","Armenia":"374","Australia":"61","Austria":"43","Azerbaijan":"994",
    "Bahamas":"1","Bahrain":"973","Bangladesh":"880","Belarus":"375","Belgium":"32",
    "Belize":"501","Benin":"229","Bhutan":"975","Bolivia":"591","Bosnia and Herzegovina":"387",
    "Botswana":"267","Brazil":"55","Brunei":"673","Bulgaria":"359","Burkina Faso":"226",
    "Burundi":"257","Cambodia":"855","Cameroon":"237","Canada":"1","Chile":"56",
    "China":"86","Colombia":"57","Costa Rica":"506","Croatia":"385","Cuba":"53",
    "Cyprus":"357","Czech Republic":"420","Denmark":"45","Dominican Republic":"1",
    "Ecuador":"593","Egypt":"20","El Salvador":"503","Estonia":"372","Ethiopia":"251",
    "Finland":"358","France":"33","Georgia":"995","Germany":"49","Ghana":"233",
    "Greece":"30","Guatemala":"502","Haiti":"509","Honduras":"504","Hungary":"36",
    "Iceland":"354","India":"91","Indonesia":"62","Iran":"98","Iraq":"964",
    "Ireland":"353","Israel":"972","Italy":"39","Japan":"81","Jordan":"962",
    "Kazakhstan":"7","Kenya":"254","Kuwait":"965","Latvia":"371","Lebanon":"961",
    "Lithuania":"370","Luxembourg":"352","Malaysia":"60","Mexico":"52","Morocco":"212",
    "Mozambique":"258","Netherlands":"31","New Zealand":"64","Nigeria":"234","Norway":"47",
    "Pakistan":"92","Panama":"507","Paraguay":"595","Peru":"51","Philippines":"63",
    "Poland":"48","Portugal":"351","Qatar":"974","Romania":"40","Russia":"7",
    "Saudi Arabia":"966","Serbia":"381","Singapore":"65","Slovakia":"421","Slovenia":"386",
    "South Africa":"27","South Korea":"82","Spain":"34","Sweden":"46","Switzerland":"41",
    "Thailand":"66","Turkey":"90","Ukraine":"380","United Arab Emirates":"971",
    "United Kingdom":"44","United States":"1","Uruguay":"598","Venezuela":"58","Vietnam":"84"
}

countries = list(ddi_map.keys())

origens = ["Facebook Ads","Google Ads","Instagram","Indicação","Orgânico"]


def rand_str(n):
    return ''.join(random.choices(string.ascii_lowercase, k=n))

def rand_num(n):
    return ''.join(random.choices(string.digits, k=n))

def gerar_cpf():
    return rand_num(11)

def gerar_site(nome):
    dominio = random.choice([".com",".com.br",".net",".io"])
    return f"www.{nome.replace(' ','').lower()}{dominio}"

def gerar_data():
    start = datetime(1960,1,1)
    end = datetime(2005,12,31)
    data = start + timedelta(days=random.randint(0,(end-start).days))

    if modo_data == "1":
        if formato_tipo == "6":
            return str(int(data.timestamp()))
        elif formato_tipo == "7":
            return str(int(data.timestamp()*1000))
        else:
            return data.strftime(formato_data)

    formatos = [
        lambda d: d.strftime("%Y-%m-%d"),
        lambda d: d.strftime("%d/%m/%Y"),
        lambda d: d.strftime("%Y-%m-%dT%H:%M:%SZ"),
        lambda d: str(int(d.timestamp())),
        lambda d: str(int(d.timestamp()*1000)),
    ]

    return random.choice(formatos)(data)

def gerar_lead(country):
    nome = maybe_special("nome", f"Lead {rand_str(5)}")
    telefone = f"+{ddi_map[country]} {rand_num(10)}"
    email = maybe_special("email", f"{rand_str(6)}@mail.com")
    documento = gerar_cpf() if country == "Brazil" else f"ID-{rand_num(8)}"
    empresa = maybe_special("empresa", f"Empresa {rand_str(5)}")
    endereco = maybe_special("endereco", f"Rua {rand_str(6)}")
    numero = random.randint(1,9999)
    bairro = maybe_special("bairro", f"Bairro {rand_str(5)}")
    cidade = maybe_special("cidade", f"Cidade {rand_str(5)}")
    uf = rand_str(2).upper()
    cep = rand_num(8)
    complemento = f"Apto {random.randint(1,999)}"
    data = gerar_data()
    origem = random.choice(origens)
    notas = maybe_special("notas","Lead teste")
    site = maybe_special("site", gerar_site(nome))

    return [
        nome, telefone, email, documento, empresa,
        endereco, numero, bairro, cidade, uf, country,
        data, origem, cep, complemento, notas, site
    ]

wb = Workbook()
ws = wb.active

headers = [
    "Nome","Telefone","Email","Documento","Empresa",
    "Endereço","Número","Bairro","Cidade","UF","País",
    "Data de Nascimento","Origem","CEP","Complemento","Notas","Site"
]

ws.append(headers)
rows = []

for _ in range(qtd_leads):
    if modo_pais == "1":
        country = pais_especifico if pais_especifico in ddi_map else "Brazil"
    else:
        country = random.choice(countries)

    row = gerar_lead(country)
    ws.append(row)
    rows.append(row)


wb.save("leads.xlsx")

with open("leads.csv","w",newline="",encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print("✅ Arquivos gerados com sucesso!")