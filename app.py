import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave-desenvolvimento-trocar-em-producao")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def carregar_produtos():
    caminho = os.path.join(DATA_DIR, "produtos.json")
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


PRODUTOS = carregar_produtos()
POR_SLUG = {p["slug"]: p for p in PRODUTOS}

CATEGORIAS = [
    {"id": "bolos-tradicionais", "nome": "Bolos Tradicionais"},
    {"id": "bolos-decorados", "nome": "Bolos Decorados e Personalizados"},
    {"id": "bolos-por-quilo", "nome": "Bolos por Quilo"},
    {"id": "brigadeiros-beijinhos", "nome": "Brigadeiros e Beijinhos"},
    {"id": "doces-festas", "nome": "Doces para Festas"},
    {"id": "centos-doces", "nome": "Centos de Doces"},
    {"id": "sobremesas-especiais", "nome": "Sobremesas e Produtos Especiais"},
]

WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "5511999999999")
WHATSAPP_LINK = f"https://wa.me/{WHATSAPP_NUMBER}"
WHATSAPP_FORMAT = "(11) 9 9999-9999"


@app.context_processor
def globais():
    return dict(
        categorias=CATEGORIAS,
        whatsapp_link=WHATSAPP_LINK,
        whatsapp_number=WHATSAPP_NUMBER,
        whatsapp_format=WHATSAPP_FORMAT,
    )


@app.route("/")
def index():
    destaques = [p for p in PRODUTOS if p.get("destaque")]
    return render_template("index.html", destaques=destaques)


@app.route("/catalogo")
def catalogo():
    categoria = request.args.get("categoria")
    produtos = PRODUTOS
    if categoria:
        produtos = [p for p in PRODUTOS if p["categoria"] == categoria]
    return render_template("catalogo.html", produtos=produtos, categoria_atual=categoria)


@app.route("/produto/<slug>")
def produto(slug):
    item = POR_SLUG.get(slug)
    if not item:
        return render_template("404.html"), 404
    relacionados = [
        p for p in PRODUTOS if p["categoria"] == item["categoria"] and p["slug"] != slug
    ][:4]
    return render_template("produto.html", produto=item, relacionados=relacionados)


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip()
        produto_interesse = request.form.get("produto", "").strip()
        data_evento = request.form.get("data_evento", "").strip()
        mensagem = request.form.get("mensagem", "").strip()

        corpo = (
            "Novo orçamento - Marocas's Sweeties\n"
            f"Nome: {nome}\nEmail: {email}\nTelefone: {telefone}\n"
            f"Produto de interesse: {produto_interesse}\nData do evento: {data_evento}\n"
            f"Mensagem: {mensagem}\n"
        )

        try:
            smtp_host = os.environ.get("SMTP_HOST")
            smtp_port = int(os.environ.get("SMTP_PORT", "587"))
            smtp_user = os.environ.get("SMTP_USER")
            smtp_pass = os.environ.get("SMTP_PASS")
            contato_email = os.environ.get("CONTATO_EMAIL")
            if smtp_host and smtp_user and smtp_pass and contato_email:
                import smtplib
                from email.message import EmailMessage

                msg = EmailMessage()
                msg["Subject"] = f"Orçamento: {nome}"
                msg["From"] = smtp_user
                msg["To"] = contato_email
                msg.set_content(corpo)
                with smtplib.SMTP(smtp_host, smtp_port) as server:
                    server.starttls()
                    server.login(smtp_user, smtp_pass)
                    server.send_message(msg)
        except Exception as exc:
            app.logger.warning(f"Não foi possível enviar e-mail: {exc}")

        try:
            os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)
            with open(
                os.path.join(BASE_DIR, "instance", "orcamentos.txt"), "a", encoding="utf-8"
            ) as f:
                f.write(corpo + "\n---\n")
        except Exception:
            pass

        flash(
            "Sua solicitação foi recebida com sucesso! Entraremos em contato em breve pelo WhatsApp.",
            "success",
        )
        return redirect(url_for("contato"))

    return render_template("contato.html")


@app.route("/api/produtos")
def api_produtos():
    return jsonify(PRODUTOS)


@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)