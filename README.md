# NutriLog
NutriLog - Diário Alimentar Inteligente

## Sobre o Projeto

Aplicaçãoq permite que o usuário registre suas refeições em tempo real, armazenando dados nutricionais para acompanhamento diário. 


## 🚀 Tecnologias Utilizadas

- **Backend:** Python 3.9 + FastAPI (Alta performance e validação de dados com Pydantic).
- **Banco de Dados:** PostgreSQL (Driver psycopg2).
- **Frontend:** HTML5, Vanilla JS e TailwindCSS (Interface moderna e responsiva).
- **Infraestrutura:** Docker (Containerização) e suporte a 12-Factor App via `DATABASE_URL`.

## ⚙️ Funcionalidades

- [x] Registro Detalhado: Adição de múltiplos itens/ingredientes por refeição.
- [x] Timestamp Personalizável: Registro retroativo ou em tempo real (Data e Hora).
- [x] Histórico Semanal: Visualização agrupada por datas (Hoje, Ontem, etc).
- [x] Persistência de Dados: Uso de banco SQL robusto (nada de dados voláteis).
- [x] Feedback Visual: Interface com notificações (Toasts) e validação de erros.

## 💻 Como Rodar Localmente

### Pré-requisitos

- Python 3.9+
- PostgreSQL instalado e rodando.

### Passo a Passo

**Clone o repositório:**

```bash
git clone https://github.com/SEU-USUARIO/nutrilog.git
cd nutrilog
```

**Configure o Banco de Dados:**  
Crie um banco chamado `food_tracker` no seu Postgres local.

```bash
# No terminal Linux/Mac ou SQL Shell
createdb food_tracker
```

> **Nota:** O código espera que a senha do usuário postgres seja `postgres`. Se for diferente, ajuste a variável de ambiente `DATABASE_URL`.

**Instale as dependências:**

```bash
pip install -r requirements.txt
```

**Execute o servidor:**

```bash
python food_tracker.py
```

**Acesse:**  
Abra [http://localhost:8000](http://localhost:8000) no seu navegador.

## 🎨 Layout e Design

A interface foi construída pensando na experiência do usuário (UX), utilizando TailwindCSS para um design limpo e responsivo.

- Tema: Esmeralda/Saúde.
- Ícones: Lucide Icons.
- Mobile First: Funciona perfeitamente em celulares.

## 👨‍💻 Autor

Desenvolvido por Dex057 © 2025.
