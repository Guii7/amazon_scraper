# Amazon Affiliate Scraper

Scraper automatizado para capturar ofertas da Amazon e gerar links de afiliado via SiteStripe.

## 📋 Funcionalidades

- **Captura de sessão**: Script para fazer login na Amazon e salvar cookies para uso posterior
- **Scraping configurável**: URLs customizáveis com quantidade de ofertas por página
- **SiteStripe**: Geração automática de links de afiliado navegando item por item
- **Tipos de scraping**: Produtos, produtos com cupons, ofertas especiais
- **Multi-canal**: Integração com Telegram, WhatsApp e TikTok
- **Banco de dados**: Armazenamento estruturado no PostgreSQL

## 🗂️ Estrutura

```
python_scraper_amazon/
├── capture_session.py      # Script para capturar e salvar sessão da Amazon
├── scraper.py             # Script principal de scraping
├── db_manager.py          # Gerenciador de conexão com PostgreSQL
├── config.yml             # Configurações de URLs e parâmetros
├── .env                   # Credenciais (não commitar!)
├── requirements.txt       # Dependências Python
├── README.md             # Este arquivo
├── puppeteer_session/    # Pasta para cookies e session data
└── logs/                 # Logs de execução
```

## 🚀 Setup

### 1. Instalar dependências

```bash
# Navegue até a pasta do projeto
cd /caminho/para/python_scraper_amazon

# Crie e ative o ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
playwright install chromium
```

### 2. Configurar credenciais

Copie `.env.example` para `.env` e preencha:

```env
# Amazon Credentials
AMAZON_EMAIL=seu_email@example.com
AMAZON_PASSWORD=sua_senha

# Amazon Associate
AMAZON_ASSOCIATE_TAG=seu_tag_de_afiliado

# PostgreSQL (Docker n8n)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=n8n
POSTGRES_USER=n8n_user
POSTGRES_PASSWORD=sua_senha_postgres
```

### 3. Configurar URLs de scraping

Edite `config.yml` para definir as URLs que deseja scrapear:

```yaml
scraping_configs:
  - name: "Black Friday"
    url: "https://www.amazon.com.br/blackfriday"
    type: "product"
    max_offers: 50

  - name: "Cupons + Produtos"
    url: "https://www.amazon.com.br/promocoes"
    type: "coupon+product"
    max_offers: 30
```

## 📝 Uso

### Passo 1: Capturar sessão

Primeiro, faça login na Amazon e salve a sessão:

```bash
python capture_session.py
```

Isso abrirá um navegador onde você deve:
1. Fazer login na sua conta Amazon
2. Aguardar salvamento automático dos cookies
3. Fechar o navegador

### Passo 2: Executar scraper

```bash
python scraper.py
```

O scraper irá:
1. Carregar a sessão salva
2. Navegar pelas URLs configuradas
3. Coletar informações dos produtos
4. Abrir cada produto individualmente
5. Usar o SiteStripe para gerar link de afiliado
6. Salvar no banco de dados

## 🔍 Campos capturados

### Informações básicas
- Nome do produto
- ASIN (Amazon Standard Identification Number)
- URL original e URL de afiliado
- Imagem principal

### Preços
- Preço original (list_price)
- Preço com desconto (sale_price)
- Percentual de desconto
- Informações de cupom (se houver)

### Detalhes adicionais
- Elegível para Prime
- Avaliação e número de reviews
- Informações de frete
- Categoria do produto

### Status de envio
- Telegram (new/sent/error)
- WhatsApp (new/sent/error)
- TikTok (new/sent/error)

## 🔧 Troubleshooting

### Erro: "Session not found"
Execute novamente `capture_session.py` para renovar a sessão.

### Erro: "SiteStripe not found"
Certifique-se de que:
- Você está logado com uma conta Amazon Associate válida
- O SiteStripe está habilitado nas configurações da sua conta

### Erro: "Database connection failed"
Verifique:
- Container PostgreSQL está rodando: `docker ps | findstr postgres`
- Credenciais no `.env` estão corretas
- Porta 5432 está acessível

## 🗃️ Banco de Dados

### Tabela: amazon_offers

```sql
-- Ver ofertas recentes
SELECT product_name, sale_price, status_telegram
FROM amazon_offers
ORDER BY created_at DESC
LIMIT 10;

-- Ver ofertas prontas para envio
SELECT COUNT(*)
FROM amazon_offers
WHERE status_telegram = 'new';

-- Ver ofertas com cupom
SELECT product_name, coupon_code, coupon_discount
FROM amazon_offers
WHERE has_coupon = true;
```

## ⚠️ Limitações

- **Rate limiting**: Amazon pode bloquear muitos requests. O scraper tem delays para evitar isso.
- **Captcha**: Se aparecer captcha, você precisará resolver manualmente e capturar sessão novamente.
- **API oficial**: Assim que fizer 3 vendas válidas, migre para a API oficial da Amazon.

## 📄 Licença

Uso pessoal. Respeite os Termos de Serviço da Amazon.
