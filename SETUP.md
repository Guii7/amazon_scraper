# 🚀 SETUP RÁPIDO - Amazon Scraper

## ✅ O que foi criado

### 1. Banco de Dados
- ✅ Tabela `amazon_offers` criada no PostgreSQL
- ✅ Índices otimizados para performance
- ✅ Campos para ASIN, cupons, Prime, links de afiliado
- ✅ Status de envio para Telegram/WhatsApp/TikTok

### 2. Estrutura de Arquivos
```
python_scraper_amazon/
├── capture_session.py   ✅ Script de captura de sessão
├── scraper.py          ✅ Scraper principal
├── db_manager.py       ✅ Gerenciador de BD
├── config.yml          ✅ Configurações de URLs
├── requirements.txt    ✅ Dependências Python
├── .env.example        ✅ Template de variáveis
├── .gitignore          ✅ Arquivos ignorados
├── README.md           ✅ Documentação completa
├── puppeteer_session/  ✅ Pasta para sessão
└── logs/               ✅ Pasta para logs
```

## 📝 PRÓXIMOS PASSOS

### Passo 1: Instalar Dependências
```cmd
cd C:\Users\guii7\bear_cave_labs\n8n\python_scraper_amazon
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

### Passo 2: Configurar .env
1. Copie `.env.example` para `.env`
2. Preencha suas credenciais:
```env
AMAZON_EMAIL=seu_email@example.com
AMAZON_PASSWORD=sua_senha
AMAZON_ASSOCIATE_TAG=seu_tag-20

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=n8n
POSTGRES_USER=n8n_user
POSTGRES_PASSWORD=sua_senha_segura
```

### Passo 3: Capturar Sessão da Amazon
```cmd
python capture_session.py
```
- Faça login na Amazon quando o navegador abrir
- Aguarde confirmação de salvamento

### Passo 4: Executar Scraper
```cmd
python scraper.py
```

## ⚙️ Configurações Disponíveis

### config.yml - Adicionar URLs
```yaml
scraping_configs:
  - name: "Black Friday Amazon"
    url: "https://www.amazon.com.br/blackfriday"
    type: "product"
    max_offers: 50
    enabled: true

  # Adicione mais URLs aqui
  - name: "Cupons"
    url: "https://www.amazon.com.br/b?node=17877921011"
    type: "coupon+product"
    max_offers: 30
    enabled: false  # Desabilite se não quiser usar
```

### Tipos de Scraping
- **product**: Apenas produtos
- **coupon+product**: Produtos com cupons
- **deal**: Ofertas especiais

## 🔍 Como Funciona

1. **Captura de Sessão** (`capture_session.py`)
   - Abre navegador
   - Você faz login manualmente
   - Salva cookies em `puppeteer_session/`

2. **Scraper Principal** (`scraper.py`)
   - Carrega sessão salva
   - Navega pelas URLs do config.yml
   - Extrai dados dos produtos:
     - Nome, preço, desconto
     - ASIN, categoria
     - Prime, cupons, avaliações
   - Para cada produto:
     - Abre página individual
     - Usa SiteStripe para gerar link de afiliado
     - Salva no banco de dados
   - Respeita delays para evitar bloqueio

3. **Banco de Dados** (`db_manager.py`)
   - Salva em `amazon_offers`
   - Lógica inteligente:
     - Se produto novo: marca como 'new'
     - Se preço mudou: marca como 'new' (reenvia)
     - Se passou 5 dias: marca como 'new' (reenvia)
     - Se nada mudou: não reenvia

## 🛠️ Troubleshooting

### Erro: "Session not found"
```cmd
python capture_session.py
```

### Erro: "SiteStripe not found"
- Certifique que está logado com conta Amazon Associates
- Verifique se `AMAZON_ASSOCIATE_TAG` está configurado no .env
- O scraper gerará link manualmente usando o tag

### Erro: "Database connection failed"
```cmd
docker ps | findstr postgres
```
Verifique se container está rodando

### Produtos sem link de afiliado
- Ajuste seletores CSS no `config.yml` se a Amazon mudou o layout
- Verifique logs em `logs/` para detalhes

## 📊 Consultas Úteis no BD

```sql
-- Ver ofertas recentes
SELECT product_name, sale_price, discount_percentage, status_telegram
FROM amazon_offers
ORDER BY created_at DESC
LIMIT 20;

-- Ofertas prontas para envio
SELECT COUNT(*)
FROM amazon_offers
WHERE status_telegram = 'new';

-- Ofertas com cupom
SELECT product_name, coupon_code, sale_price
FROM amazon_offers
WHERE has_coupon = true;

-- Top descontos
SELECT product_name, list_price, sale_price, discount_percentage
FROM amazon_offers
WHERE discount_percentage > 50
ORDER BY discount_percentage DESC
LIMIT 10;
```

## 🎯 Integração com N8N

Depois de ter ofertas no banco, crie workflows no N8N para:
1. Ler ofertas com `status_telegram = 'new'`
2. Formatar mensagem com link de afiliado
3. Enviar para Telegram/WhatsApp
4. Marcar como 'sent' via query SQL

## ⚠️ IMPORTANTE

- **NÃO commitar** o arquivo `.env`
- **NÃO commitar** a pasta `puppeteer_session/`
- **Renovar sessão** regularmente (a cada 30 dias)
- **Rate limiting**: Amazon pode bloquear muitos requests. Ajuste delays no config.yml
- **API oficial**: Assim que fizer 3 vendas válidas, migre para API oficial

## 📞 Dúvidas?

Veja o `README.md` completo para mais detalhes sobre cada componente.
