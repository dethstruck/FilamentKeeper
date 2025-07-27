# FilamentKeeper

![License](https://img.shields.io/badge/license-MIT-green)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)

## Descrição

O **3D Printer Filament Stock Manager** é um gerenciador leve e eficiente para controlar o estoque de filamentos de impressoras 3D.  
Ideal para makers, pequenas oficinas e laboratórios, o sistema permite cadastrar filamentos por tipo, cor e peso, acompanhar o consumo durante as impressões e visualizar o estoque em tempo real com barras de progresso coloridas no terminal.

---

## Funcionalidades

- Cadastro e gerenciamento de diferentes filamentos  
- Atualização do estoque após uso  
- Visualização do estoque com barra de progresso  
- Interface simples em linha de comando  
- Persistência de dados usando TinyDB  
- Saída colorida com Colorama para melhor visualização  

---

## Tecnologias Utilizadas

- Python 3.8+  
- [TinyDB](https://tinydb.readthedocs.io/en/latest/) — banco de dados NoSQL simples e leve  
- [Colorama](https://pypi.org/project/colorama/) — cores no terminal  

---

## Como usar

1. Clone este repositório:  
   ```bash
   git clone https://github.com/dethstruck/filamentKeeper.git
   cd FilamentKeeper
   ```
2. Instale as dependências:
   ```bash  
   pip install -r requirements.txt
   ```
3. Execute o projeto:
   ```
   python main.py
   ```
