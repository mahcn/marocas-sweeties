# Marocas's Sweeties

Site profissional, moderno e responsivo para confeitaria artesanal de doces e sobremesas por encomenda.

## Tecnologias
- HTML5, CSS3 e JavaScript (vanilla)
- Python com Flask (backend)
- Git e GitHub (versioneamento)

## Como executar localmente
```bash
cd "C:\Users\maria\Desktop\vscode"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:SECRET_KEY = "sua-chave-secreta"
$env:WHATSAPP_NUMBER = "5511999999999"
flask run
# ou: python app.py
```
Acesse: http://127.0.0.1:5000

## Informações a preencher futuramente
- Fotos reais dos produtos em `static/images/produtos/`
- Preços definitivos em `data/produtos.json`
- Número real do WhatsApp na variável `WHATSAPP_NUMBER`
- Configurações de e-mail (SMTP) para recebimento de orçamentos
- Endereço completo para retirada e entrega