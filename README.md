# TVApp - Aplicativo de Streaming de Vídeos

Um aplicativo Python desenvolvido com BeeWare que replica a funcionalidade do projeto original, incluindo integração com Turso, ytdlp e streamlink para extração de links de vídeo e streams do YouTube.

## Características

- **Interface Gráfica**: Desenvolvida com BeeWare/Toga para multiplataforma
- **Banco de Dados**: Integração com Turso (SQLite na nuvem)
- **Extração de Streams**: Suporte para streamlink e ytdlp
- **Reprodução de Vídeo**: Player HTML5 integrado
- **Multiplataforma**: Funciona em Windows, macOS, Linux, iOS e Android

## Funcionalidades

1. **Buscar Lives**: Digite o nome de uma live (live1, live2, live3, live4) e reproduza o stream
2. **Atualizar Links**: Atualiza automaticamente os links M3U8 das lives no banco de dados
3. **Reprodução**: Player de vídeo integrado com suporte a streams M3U8

## Estrutura do Projeto

```
TVApp/
├── src/
│   └── tvapp/
│       ├── __init__.py
│       ├── __main__.py
│       ├── app.py              # Interface principal do aplicativo
│       ├── stream_manager.py   # Gerenciamento de streams e banco de dados
│       ├── config.py          # Configurações do aplicativo
│       └── resources/
├── .env                       # Variáveis de ambiente (Turso)
├── ytdlp                     # Executável ytdlp
├── pyproject.toml            # Configuração do projeto BeeWare
└── README.md
```

## Configuração

### 1. Variáveis de Ambiente (.env)

```env
DATABASE_URL=libsql://sua-database-url.turso.io
DATABASE_AUTH_TOKEN=seu-token-de-autenticacao
CRON_TOKEN=seu-token-cron
```

### 2. Dependências

O projeto utiliza as seguintes dependências principais:

- `toga` - Framework de interface gráfica
- `libsql-client` - Cliente para Turso/SQLite
- `streamlink` - Extração de streams
- `python-dotenv` - Gerenciamento de variáveis de ambiente

## Instalação e Execução

### 1. Instalar Dependências

```bash
pip install briefcase libsql-client python-dotenv streamlink
```

### 2. Configurar Ambiente

1. Copie o arquivo `.env` com suas credenciais do Turso
2. Certifique-se de que o arquivo `ytdlp` está presente e executável

### 3. Executar em Modo Desenvolvimento

```bash
cd TVApp
briefcase dev
```

### 4. Construir Aplicativo

```bash
# Para Linux
briefcase build

# Para criar pacote distribuível
briefcase package
```

## Como Usar

1. **Iniciar o Aplicativo**: Execute o TVApp
2. **Atualizar Links**: Clique em "Atualizar Links" para buscar os streams mais recentes
3. **Reproduzir Live**: Digite o nome da live (live1, live2, live3, live4) e clique em "Abrir Live"
4. **Assistir**: O vídeo será reproduzido no player integrado

## Lives Disponíveis

- **live1**: SBT
- **live2**: Bluey Português Brasil
- **live3**: Rádio Novas de Paz
- **live4**: Rede Brasil Rádio

## Tecnologias Utilizadas

- **BeeWare/Toga**: Framework de interface gráfica multiplataforma
- **Turso**: Banco de dados SQLite na nuvem
- **Streamlink**: Extração de streams de vídeo
- **ytdlp**: Ferramenta de download/extração de vídeos do YouTube
- **Python**: Linguagem de programação principal

## Arquitetura

O aplicativo segue uma arquitetura modular:

1. **app.py**: Interface do usuário e lógica de apresentação
2. **stream_manager.py**: Lógica de negócio para gerenciamento de streams
3. **config.py**: Configurações centralizadas
4. **Banco de Dados**: Armazenamento de links M3U8 no Turso

## Compatibilidade

- **Desktop**: Windows, macOS, Linux
- **Mobile**: iOS, Android (com algumas limitações de reprodução)
- **Web**: Suporte experimental via toga-web

## Limitações

- A reprodução de streams M3U8 depende do suporte do navegador/sistema
- Alguns streams podem ter restrições geográficas
- A qualidade do stream depende da disponibilidade no YouTube

## Contribuição

Este projeto foi desenvolvido como uma versão BeeWare do projeto original. Para contribuições:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto mantém a mesma licença do projeto original.

