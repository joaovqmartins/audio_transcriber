# Audio Transcriber

Aplicativo desktop simples e leve para transcrição de áudio, com interface
gráfica minimalista. Arraste um arquivo `.mp3`, `.ogg`, `.wav` ou `.m4a`, clique
em **Transcrever** e receba o texto — a transcrição é feita pela **API de STT da
Groq**, que roda o modelo Whisper na nuvem com alta velocidade.

> **Atenção:** o app requer conexão com a internet e envia o arquivo de áudio
> para os servidores da Groq para ser transcrito. Se você precisa que o áudio
> nunca saia da sua máquina, esta versão não atende esse requisito.

## Índice

1. [O que é o projeto](#o-que-é-o-projeto)
2. [Requisitos](#requisitos)
3. [Instalar o Python](#instalar-o-python)
4. [Instalar as dependências](#instalar-as-dependências)
5. [Obter uma chave de API da Groq](#obter-uma-chave-de-api-da-groq)
6. [Como executar](#como-executar)
7. [Gerar um executável (.exe)](#gerar-um-executável-exe)
8. [Formatos suportados](#formatos-suportados)
9. [Limites da API](#limites-da-api)
10. [Escolhendo velocidade x precisão](#escolhendo-velocidade-x-precisão)
11. [Solução de problemas](#solução-de-problemas)

## O que é o projeto

Um MVP focado em um único fluxo: **arrastar áudio → transcrever na nuvem →
visualizar → copiar/salvar**. Sem login, sem banco de dados, sem servidor
próprio — só a interface local conversando com a API da Groq.

Estrutura do projeto:

```text
transcrever_audio/
├── main.py                        # ponto de entrada
├── requirements.txt                # dependências de runtime
├── requirements-dev.txt            # + ferramentas de build (PyInstaller)
├── build.spec                      # config do PyInstaller (gerar o .exe)
├── README.md
│
├── app/
│   ├── config.py                  # caminhos, modelos, idiomas
│   ├── themes.py                  # temas do app (ícone e paleta de cada um)
│   ├── ui/
│   │   ├── main_window.py         # interface gráfica (PySide6)
│   │   ├── settings_dialog.py     # diálogo da chave de API e do tema
│   │   ├── widgets.py             # botões, combobox e spinner personalizados
│   │   ├── icons.py               # ícones vetoriais da interface
│   │   ├── title_bar.py           # cores da barra de título no Windows
│   │   └── style.py               # folha de estilo (QSS) gerada a partir do tema
│   ├── transcription/
│   │   └── groq_engine.py         # motor de transcrição (API da Groq)
│   └── utils/
│       ├── audio.py               # validação de arquivos, tamanho
│       └── settings.py            # persistência local da chave de API e do tema
│
└── assets/
    └── icons/                     # um ícone por tema (inclui o .ico do executável)
```

## Requisitos

* Windows 10/11, Linux ou macOS
* Python 3.10 ou superior
* Conexão com a internet (necessária para toda transcrição, não só na primeira execução)
* Uma chave de API da Groq (gratuita)
* **No Linux:** as bibliotecas gráficas do Qt (veja [Instalar as dependências](#instalar-as-dependências) abaixo)

## Instalar o Python

**Windows:**

1. Baixe o instalador em [python.org/downloads](https://www.python.org/downloads/)
   (recomendado: versão 3.11.x ou 3.12.x).
2. Durante a instalação, marque a opção **"Add python.exe to PATH"**.
3. Verifique a instalação num terminal (PowerShell ou cmd):

```bash
python --version
```

**Linux:**

A maioria das distribuições já vem com Python 3 instalado, mas o pacote de
ambiente virtual (`venv`) às vezes precisa ser instalado à parte. Exemplo no
Ubuntu/Debian:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

Em outras distros, use o gerenciador de pacotes equivalente (`dnf`, `pacman`,
etc.) para instalar `python3`, `python3-venv`/`python-virtualenv` e `pip`.

Verifique a instalação:

```bash
python3 --version
```

> **Atenção:** no Linux e no macOS o comando geralmente é `python3` (não
> `python`). Sempre que este README disser `python`, use `python3` nesses
> sistemas.

**macOS:**

```bash
brew install python
```

## Instalar as dependências

1. Crie e ative um ambiente virtual **dentro da pasta do projeto** — isso não
   é opcional: distribuições Linux recentes (Ubuntu 23.04+, Debian 12+)
   bloqueiam `pip install` fora de um venv por padrão, e é a causa mais comum
   do erro `ModuleNotFoundError: No module named 'groq'` ao tentar rodar o app.

```bash
# Windows (PowerShell ou cmd)
python -m venv venv
venv\Scripts\activate

# Linux ou macOS
python3 -m venv venv
source venv/bin/activate
```

   Depois de ativado, o início da linha do terminal deve mostrar `(venv)`.
   Confirme que o `pip` do venv está sendo usado:

```bash
# Linux/macOS
which python
# deve terminar em algo como .../transcrever_audio/venv/bin/python
```

2. Instale as dependências (com o venv **ainda ativado**):

```bash
pip install -r requirements.txt
```

Isso instala o **PySide6** (interface gráfica), o **groq** (cliente oficial
da API de transcrição) e o **httpx** (conexão com a API, usada também para
cancelar uma transcrição em andamento). Nenhum modelo de IA é baixado para o
seu computador.

3. Confirme que as dependências foram instaladas corretamente:

```bash
python -c "import groq, PySide6; print('OK')"
```

Se aparecer `ModuleNotFoundError` aqui, o venv não está ativado (repita o
passo 1) ou a instalação do passo 2 falhou — role a tela para cima e veja se
o `pip install` mostrou algum erro.

### Bibliotecas gráficas do Qt no Linux

O PySide6 depende de bibliotecas do sistema para abrir janelas (plugin
`xcb`/Wayland). Se o app não abrir e o erro mencionar `xcb`, `Could not load
the Qt platform plugin` ou `libEGL`/`libGL`, instale os pacotes do sistema
(exemplo no Ubuntu/Debian):

```bash
sudo apt install libxcb-cursor0 libxcb-xinerama0 libgl1
```

Em outras distros, procure pelo pacote equivalente a `libxcb-cursor0` (ex.:
`xcb-util-cursor` no Fedora/Arch).

## Obter uma chave de API da Groq

1. Crie uma conta gratuita em [console.groq.com](https://console.groq.com/).
2. Acesse [console.groq.com/keys](https://console.groq.com/keys) e clique em
   **Create API Key**.
3. Copie a chave (começa com `gsk_...`).
4. Abra o Audio Transcriber, clique no ícone de cadeado (🔒) no canto
   superior direito, cole a chave no campo e clique em **Salvar**.

A chave é salva localmente — nunca é enviada a nenhum lugar além da própria
API da Groq:

* Windows: `%USERPROFILE%\.audio_transcriber\settings.json`
* Linux/macOS: `~/.audio_transcriber/settings.json`

## Como executar

### Abrir o app

Abra um terminal na pasta do projeto e, com as
[dependências instaladas](#instalar-as-dependências), rode o comando do seu
sistema. Assim não é preciso ativar o ambiente virtual antes:

```bash
# Windows (PowerShell)
.\venv\Scripts\python.exe main.py

# Windows (cmd)
venv\Scripts\python.exe main.py

# Linux ou macOS
venv/bin/python main.py
```

Se o ambiente virtual já estiver ativado (com `(venv)` no início da linha do
terminal), basta `python main.py`.

No **VS Code**, abra a pasta do projeto e aperte `F5`: a configuração
"Audio Transcriber (main.py)" já vem pronta em `.vscode/launch.json`.

### Transcrever um áudio

1. **Configure a chave de API** (só na primeira vez): clique no cadeado no canto
   superior direito e informe sua chave. Veja
   [como obter uma chave](#obter-uma-chave-de-api-da-groq).
2. **Carregue o áudio:** arraste o arquivo para a área central, clique nela ou
   use `Ctrl+O`.
3. **Escolha o modelo e o idioma:** o modelo pode ser **Preciso** (padrão) ou
   **Rápido**, e o idioma pode ser Português, Inglês, Espanhol ou "Detectar
   automaticamente". Veja
   [Escolhendo velocidade x precisão](#escolhendo-velocidade-x-precisão).
4. **Clique em Transcrever** ou use `Ctrl+Enter`, e acompanhe o status abaixo
   do botão.
5. **Revise o texto:** a caixa de transcrição é editável, então dá para corrigir
   nomes e termos antes de usar o resultado. A seta ao lado de "Transcrição"
   esconde a área de arquivo e as opções, deixando mais espaço para o texto.
6. **Copie ou salve:** use **Copiar** ou **Salvar** (`Ctrl+S`, gera um `.txt`).
   O que vai para a cópia ou para o arquivo é o texto com as suas edições.

> **Atenção:** carregar outro arquivo limpa a caixa de transcrição. Copie ou
> salve o texto antes.

### Cancelar uma transcrição

Durante o processamento, o botão mostra "Transcrevendo...". Passe o mouse sobre
ele: o botão fica vermelho com o texto **Cancelar**, e o clique interrompe o
envio na hora. O arquivo continua carregado, então você pode ajustar as opções e
transcrever de novo.

### Atalhos de teclado

| Atalho | Ação |
| --- | --- |
| `Ctrl+O` | Selecionar um arquivo de áudio |
| `Ctrl+Enter` | Iniciar a transcrição |
| `Ctrl+S` | Salvar o texto em `.txt` |

## Gerar um executável (.exe)

Com o [PyInstaller](https://pyinstaller.org/), o app vira um único arquivo que
abre com dois cliques, sem Python nem ambiente virtual. É o melhor caminho para
**passar o app para outra pessoa**.

### Como gerar

O ambiente virtual precisa já ter sido criado (veja
[Instalar as dependências](#instalar-as-dependências)), mas não é preciso
ativá-lo: os comandos abaixo usam o `venv` diretamente.

1. Abra um terminal na pasta do projeto, onde fica o `build.spec`.
2. Instale as ferramentas de build, necessárias só na primeira vez:

```bash
# Windows
.\venv\Scripts\python.exe -m pip install -r requirements-dev.txt

# Linux ou macOS
venv/bin/python -m pip install -r requirements-dev.txt
```

3. Gere o executável, o que costuma levar cerca de um minuto:

```bash
# Windows
.\venv\Scripts\pyinstaller.exe build.spec

# Linux ou macOS
venv/bin/pyinstaller build.spec
```

4. Quando aparecer `Build complete!`, o arquivo estará na pasta `dist/`:

| Sistema | Arquivo gerado |
| --- | --- |
| Windows | `dist/AudioTranscriber.exe` |
| Linux ou macOS | `dist/AudioTranscriber` |

As pastas `build/` e `dist/` são ignoradas pelo Git.

### Atualizar o executável

O executável é uma cópia do código do momento em que foi gerado, então ele não
se atualiza sozinho. Depois de mudar o código:

1. **Rode de novo o comando do passo 3** de [Como gerar](#como-gerar). O arquivo
   em `dist/` é substituído pela versão nova.
2. **Abra o app de novo:** se ele estava aberto durante o build, essa janela
   continua na versão antiga até ser fechada.

Alguns cuidados ao gerar uma nova versão:

* **O build usa o que está na pasta naquele momento:** isso inclui a branch atual
  e as alterações sem commit. Para gerar uma versão estável, volte para o `main`
  antes.
* **Dependência nova:** se o `requirements.txt` mudou, repita o passo 2 antes de
  gerar.
* **Arquivos novos:** o que estiver em `assets/` entra sozinho no executável.
  Arquivos de outras pastas precisam ser adicionados em `datas`, no `build.spec`.
* **Outras pessoas:** quem já tem o app não recebe a atualização, então é preciso
  enviar o arquivo novo. A chave de API continua funcionando, porque ela fica na
  pasta do usuário, e não dentro do executável.

### Como usar e distribuir

Basta copiar esse **único arquivo**: quem recebe não precisa instalar Python
nem qualquer dependência. Antes de enviar, vale saber que:

* **É preciso gerar em cada sistema:** o PyInstaller não faz build cruzado. Um
  `.exe` gerado no Windows não roda no Linux, e vice-versa.
* **A chave de API não vai junto:** ela fica salva no computador de quem a
  configurou, nunca dentro do executável. Cada pessoa informa a própria chave no
  cadeado, e o executável pode ser compartilhado sem expor a sua.
* **O Windows pode mostrar um aviso:** o executável não tem assinatura digital,
  então o SmartScreen pode exibir "O Windows protegeu o computador". Para abrir
  mesmo assim, clique em **Mais informações** e depois em **Executar assim
  mesmo**. Alguns antivírus também desconfiam de executáveis do PyInstaller.
* **O arquivo é grande e demora um pouco para abrir:** são cerca de 55 MB, porque
  ele carrega o próprio Python e o PySide6. A cada abertura ele se descompacta
  numa pasta temporária, o que leva alguns segundos.

`requirements-dev.txt` e `build.spec` só são usados para **gerar** o executável.
Quem recebe o arquivo pronto não precisa deles.

## Formatos suportados

De entrada: **`.mp3`**, **`.ogg`**, **`.wav`** e **`.m4a`**, enviados
diretamente para a API (a própria Groq decodifica o áudio, não é necessário
FFmpeg local). Para adicionar outro formato aceito pela Groq, basta incluir a
extensão em `SUPPORTED_EXTENSIONS`, em [`app/config.py`](app/config.py) —
nenhuma outra parte do código precisa mudar.

Exportação de saída, por enquanto: só `.txt`. Formatos como `.srt`, `.vtt` ou
`.json` (com timestamps por trecho) podem ser adicionados no futuro — a
lógica de exportação já está separada da lógica de transcrição.

## Limites da API

* Tamanho máximo de arquivo: **25 MB** (definido em `MAX_FILE_SIZE_MB`, em
  [`app/config.py`](app/config.py)). Arquivos maiores são rejeitados com uma
  mensagem amigável antes de qualquer envio.
* A API da Groq tem uma camada gratuita com limites de uso (requisições por
  minuto/dia). Se você ultrapassar o limite, a API retorna um erro que é
  exibido na interface sem travar o aplicativo.

## Escolhendo velocidade x precisão

O combo **Modelo** na interface tem duas opções, definidas em
[`app/config.py`](app/config.py) (`MODEL_OPTIONS`):

* **Rápido** (`whisper-large-v3-turbo`) — mais barato e mais rápido, ótimo
  para a maioria dos áudios.
* **Preciso** (`whisper-large-v3`, padrão) — melhor qualidade de transcrição,
  recomendado quando precisão importa mais que velocidade ou custo.

Para adicionar ou ajustar perfis, basta editar a lista `MODEL_OPTIONS` em
`app/config.py` com o identificador de outro modelo suportado pela Groq —
nenhuma outra parte do código precisa mudar.

## Solução de problemas

* **`ModuleNotFoundError: No module named 'groq'`** (ou `PySide6`): o
  ambiente virtual não está ativado, ou as dependências não foram instaladas
  nele. No Linux/macOS, rode `source venv/bin/activate` (Windows:
  `venv\Scripts\activate`) e depois `pip install -r requirements.txt`
  novamente — confira com `which python` (Linux/macOS) que ele aponta para
  dentro da pasta `venv`. Veja [Instalar as dependências](#instalar-as-dependências).
* **`pip install` falha com "externally-managed-environment"** (comum em
  Ubuntu/Debian recentes): é o sistema bloqueando instalação de pacotes fora
  de um venv — não use `--break-system-packages`, apenas crie e ative o
  ambiente virtual como descrito acima antes de instalar.
* **"A execução de scripts foi desabilitada neste sistema"** ao ativar o venv no
  PowerShell: rode o app sem ativar, com `.\venv\Scripts\python.exe main.py`, ou
  ative o venv pelo `cmd`.
* **`'pyinstaller' não é reconhecido`** ao gerar o executável: o PyInstaller só
  existe dentro do `venv`, e o comando foi rodado sem ele. Use
  `.\venv\Scripts\pyinstaller.exe build.spec`, como em
  [Como gerar](#como-gerar).
* **`command not found: python`** no Linux/macOS: use `python3` no lugar de
  `python` (o comando `python` sozinho geralmente não existe nessas
  plataformas).
* **Erro mencionando `xcb`, `Could not load the Qt platform plugin` ou
  `libEGL`/`libGL`** no Linux: faltam bibliotecas gráficas do sistema — veja
  [Bibliotecas gráficas do Qt no Linux](#bibliotecas-gráficas-do-qt-no-linux).
* **"Nenhuma chave de API da Groq configurada"**: clique no ícone de cadeado
  e informe sua chave (veja
  [Obter uma chave de API da Groq](#obter-uma-chave-de-api-da-groq)).
* **"Chave de API inválida ou expirada"**: gere uma nova chave em
  [console.groq.com/keys](https://console.groq.com/keys) e atualize nas
  configurações do app.
* **"Não foi possível conectar à internet"**: verifique sua conexão — a
  transcrição não funciona offline nesta versão.
* **Arquivo acima do limite de 25 MB**: compacte o áudio (ex.: reduza o
  bitrate do MP3) ou corte o trecho relevante antes de enviar.
* **Mensagem de erro amigável na interface**: o aplicativo nunca fecha
  sozinho em caso de falha de transcrição; a mensagem de erro é exibida em
  uma janela e o app continua utilizável.
