# Guia de Instalação - TVApp

Este guia fornece instruções detalhadas para instalar e executar o TVApp em diferentes sistemas operacionais.

## Pré-requisitos

### Sistema Operacional
- **Linux**: Ubuntu 20.04+ ou distribuições equivalentes
- **Windows**: Windows 10+ (com WSL recomendado)
- **macOS**: macOS 10.15+

### Software Necessário
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional, para clonar o repositório)

## Instalação no Linux (Ubuntu/Debian)

### 1. Atualizar o Sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar Dependências do Sistema
```bash
sudo apt install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libcairo2-dev \
    libgirepository1.0-dev \
    pkg-config \
    git
```

### 3. Instalar Briefcase (BeeWare)
```bash
pip3 install briefcase
```

### 4. Clonar ou Extrair o Projeto
```bash
# Se usando Git
git clone <url-do-repositorio>
cd TVApp

# Ou extrair o arquivo ZIP
unzip TVApp.zip
cd TVApp
```

### 5. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:
```bash
nano .env
```

Adicione suas credenciais do Turso:
```env
DATABASE_URL=libsql://sua-database-url.turso.io
DATABASE_AUTH_TOKEN=seu-token-de-autenticacao
CRON_TOKEN=seu-token-cron
```

### 6. Instalar Dependências Python
```bash
pip3 install libsql-client python-dotenv streamlink
```

### 7. Executar em Modo Desenvolvimento
```bash
briefcase dev
```

## Instalação no Windows

### 1. Instalar Python
- Baixe Python 3.8+ do site oficial: https://python.org
- Durante a instalação, marque "Add Python to PATH"

### 2. Instalar Git (Opcional)
- Baixe do site oficial: https://git-scm.com

### 3. Abrir PowerShell ou Command Prompt como Administrador

### 4. Instalar Briefcase
```cmd
pip install briefcase
```

### 5. Baixar o Projeto
```cmd
# Se usando Git
git clone <url-do-repositorio>
cd TVApp

# Ou extrair o arquivo ZIP manualmente
```

### 6. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na pasta do projeto com suas credenciais do Turso.

### 7. Instalar Dependências
```cmd
pip install libsql-client python-dotenv streamlink
```

### 8. Executar
```cmd
briefcase dev
```

## Instalação no macOS

### 1. Instalar Homebrew (se não tiver)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Instalar Python e Dependências
```bash
brew install python3 pkg-config cairo gobject-introspection
```

### 3. Instalar Briefcase
```bash
pip3 install briefcase
```

### 4. Seguir os Passos 4-8 do Linux

## Configuração do Banco Turso

### 1. Criar Conta no Turso
- Acesse: https://turso.tech
- Crie uma conta gratuita

### 2. Criar Database
```bash
turso db create yt-m3u8-links
```

### 3. Obter Credenciais
```bash
# URL do banco
turso db show yt-m3u8-links

# Token de autenticação
turso db tokens create yt-m3u8-links
```

### 4. Configurar .env
Use as credenciais obtidas no arquivo `.env`.

## Solução de Problemas

### Erro: "Could not find a version that satisfies the requirement youtube-dlp"
- O youtube-dlp não está disponível via pip em alguns sistemas
- O projeto usa o executável `ytdlp` incluído como fallback

### Erro: "Python dependency not found" (Linux)
```bash
sudo apt install python3-dev python3-pkgconfig
```

### Erro: "No module named 'gi'" (Linux)
```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

### Erro de Compilação no Windows
- Instale o Visual Studio Build Tools
- Ou use o WSL (Windows Subsystem for Linux)

### Problemas de Reprodução de Vídeo
- Alguns streams podem ter restrições geográficas
- Verifique se o link M3U8 é válido
- Teste com diferentes lives

## Construindo Executáveis

### Para Linux
```bash
briefcase build
briefcase package
```

### Para Windows
```bash
briefcase build windows
briefcase package windows
```

### Para macOS
```bash
briefcase build macOS
briefcase package macOS
```

## Estrutura de Arquivos Após Instalação

```
TVApp/
├── .env                    # Configurações (criar manualmente)
├── ytdlp                   # Executável ytdlp
├── pyproject.toml          # Configuração do projeto
├── src/
│   └── tvapp/
│       ├── app.py          # Aplicação principal
│       ├── stream_manager.py
│       └── config.py
├── test_app.py            # Script de teste
├── README.md
└── INSTALL.md
```

## Testando a Instalação

Execute o script de teste:
```bash
python test_app.py
```

Se todos os testes passarem, a instalação foi bem-sucedida!

## Suporte

Para problemas ou dúvidas:
1. Verifique os logs em `logs/briefcase.*.log`
2. Execute o script de teste para diagnosticar problemas
3. Consulte a documentação do BeeWare: https://beeware.org

