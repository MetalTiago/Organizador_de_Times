# Organizador de Times

Este é um aplicativo feito em Python com interface gráfica utilizando [Flet](https://flet.dev/), que permite organizar times de futebol de maneira prática e rápida.

## 🎯 Funcionalidades

- Cadastro e gerenciamento de jogadores
- Criação automática de times equilibrados
- Interface moderna e intuitiva
- Armazenamento de dados local (provavelmente via SQLite ou arquivos)

## 🚀 Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/MetalTiago/Organizador_de_Times.git
cd Organizador_de_Times
```

### 2. Instale as dependências

Certifique-se de ter o Python instalado (3.10 ou superior). Em seguida, rode:

```bash
pip install -r requirements.txt
```

### 3. Execute o projeto

```bash
python main.py
```

> Obs: O aplicativo abrirá uma janela gráfica feita com Flet.

## 📁 Estrutura do Projeto

```
Organizador_de_Times/
│
├── components.py        # Elementos da interface
├── db_handler.py        # Lógica de banco de dados
├── main.py              # Ponto de entrada do app
├── organizer.py         # Lógica de organização dos times
└── requirements.txt     # Lista de dependências do projeto
```

## 📦 Tecnologias utilizadas

- [Python](https://www.python.org/)
- [Flet](https://flet.dev/)
- SQLite (ou similar para armazenamento local)

## 🧑‍💻 Autor

Desenvolvido por MetalTiago.  
GitHub: [@MetalTiago](https://github.com/MetalTiago)
