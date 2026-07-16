# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Visão geral do projeto

SGE (Sistema de Gerenciamento de Estoque) é um sistema de gerenciamento de estoque em Django 6. Ele expõe
a mesma funcionalidade de duas formas: views/templates Django renderizadas no servidor para a interface
web, e uma API REST DRF + JWT em `/api/v1/` para integração entre sistemas. O idioma do domínio (UI,
labels, nomes) é português (marca, categoria, fornecedor, produto, entrada = inflow, saída = outflow).

## Comandos

```bash
# Ativar o virtualenv já existente em ./env
source env/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Rodar as migrations
python manage.py migrate

# Subir o servidor de desenvolvimento
python manage.py runserver

# Criar um usuário admin (necessário para logar — não há autocadastro)
python manage.py createsuperuser

# Gerar migrations após alterar um model
python manage.py makemigrations <app_name>
```

Não há suíte de testes, linter ou formatter configurados neste repositório (nenhum `tests.py` com
conteúdo, nenhuma config de flake8/pytest/pyproject) — não assuma que `pytest`/`ruff`/etc. existem a menos
que você mesmo os adicione.

O Docker Compose (`docker-compose.yml`) roda a aplicação contra um container Postgres 15 (`sge_web` +
`sge_db`); `docker-compose up` executa migrate e depois `runserver 0.0.0.0:8000`.

## Arquitetura

### Estrutura dos apps — um app Django por entidade de domínio

`brands`, `categories`, `suppliers`, `products`, `inflows`, `outflows`, `authentication` são apps Django
independentes, cada um seguindo a mesma estrutura: `models.py`, `views.py`, `urls.py`, `forms.py`,
`serializers.py`, `admin.py`, `apps.py`, `templates/`. Ao adicionar uma nova entidade, replique essa
estrutura em vez de inventar uma nova.

Cada app de entidade (exceto `authentication`) expõe:
- Views baseadas em classe do Django (`ListView`/`CreateView`/`UpdateView`/`DeleteView`/`DetailView`)
  protegidas por `LoginRequiredMixin` + `PermissionRequiredMixin`, usando as permissões nativas de model
  do Django (ex.: `products.view_product`, `products.add_product`) — atribuídas a usuários/grupos pelo
  admin site.
- Views DRF `generics.ListCreateAPIView` / `RetrieveUpdateDestroyAPIView` (ou `RetrieveAPIView` para
  models somente-append) em `api/v1/<entidade>/`, usando o serializer do mesmo app.

Todos os `urls.py` de cada app são montados na raiz em `app/urls.py`
(`path('', include('<app>.urls'))`), então nomes de rota como `product_list`,
`product-create-list-api-view` precisam permanecer únicos entre todos os apps.

### Quantidade em estoque é orientada por signals, não calculada na leitura

`Product.quantity` é um campo inteiro persistido. Ele só é alterado através de signals em
`inflows/signals.py` e `outflows/signals.py`, ambos escutando `post_save` no respectivo model e disparando
apenas `if created`:
- Criar um `Inflow` (entrada de estoque vinda de um `Supplier`) incrementa `product.quantity`.
- Criar um `Outflow` (uma venda) decrementa `product.quantity`.

Registros de `Inflow`/`Outflow` são tratados como um ledger somente-append — não há views de update para
nenhum dos dois, apenas list/create/detail. Se for alterar a lógica que afeta a quantidade, o lugar certo
são esses signal handlers, não espalhar isso pelas views. `OutflowForm.clean_quantity` é o único ponto que
impede vender mais do que há em estoque (rejeita quantidade maior que `product.quantity` atual); o
serializer DRF de outflow **não** faz essa validação.

Tanto `Inflow.product` quanto `Outflow.product` usam `on_delete=models.PROTECT`, assim como
`Product.brand` e `Product.category` — apagar uma marca/categoria/produto que tenha registros
dependentes vai levantar `ProtectedError` em vez de fazer cascade.

### Métricas do dashboard (`app/metrics.py`)

A view home (`app/views.py`) agrega dados entre apps (totais, lucro, vendas dos últimos 7 dias, contagem
de produtos por categoria/marca) importando os models diretamente de `products`, `outflows`,
`categories`, `brands` — não há service layer nem um app de métricas compartilhado. Ao adicionar uma nova
métrica, ela entra aqui e é injetada no contexto de `home.html` como JSON para os componentes de gráfico.

### Modelo de autenticação

Login baseado em sessão (`LoginView`/`LogoutView` do `django.contrib.auth`) protege as views HTML; JWT
(`rest_framework_simplejwt`) protege a API (`DEFAULT_AUTHENTICATION_CLASS` em `app/settings.py`). Os
endpoints de token estão em `authentication/urls.py`, sob `api/v1/authetication/token/` (atenção:
"authetication" está com erro de digitação no path real da URL — isso é intencional/já existente, não
"corrija" silenciosamente sem checar quem consome essa rota). As permission classes globais do DRF exigem
tanto `IsAuthenticated` quanto `DjangoModelPermissions`, então qualquer nova view de API já herda o mesmo
comportamento de permissões das views HTML sem configuração extra.

### Frontend

Sem build step / bundler em Node — Tailwind CSS v4 e Alpine.js são carregados via CDN (`<script>`/`<link>`)
em `app/templates/base.html`, junto com Bootstrap Icons. As classes utilitárias do Tailwind ficam
diretamente nos widgets de cada `forms.py` (veja `products/forms.py` como referência canônica de
estilização dos inputs). Partials compartilhados ficam em `app/templates/components/`
(`_sidebar.html`, `_header.html`, `_footer.html`, `_pagination.html`, `_sales_metrics.html`,
`_product_metrics.html`) e são incluídos pelos templates de list/detail de cada app.

### Cuidados com settings

`app/settings.py` tem duas entradas em `DATABASES`: `default` (Postgres, casa com os nomes de
serviço/credenciais do docker-compose) e `dev` (sqlite, não usada a menos que `default` seja repontado
para ela — o Django ignora entradas que não sejam `default` a menos que o código as referencie
explicitamente). `DEBUG = True` e `SECRET_KEY` estão hardcoded para desenvolvimento local; trate qualquer
pedido de hardening de produção como algo que mexe diretamente neste arquivo, já que não há separação de
settings por ambiente.
