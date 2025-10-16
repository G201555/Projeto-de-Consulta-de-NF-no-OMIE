Consulta de Notas Fiscais - Produtos e Serviços (Omie API)

Este projeto é uma aplicação web construída em Python utilizando Flask, que permite consultar Notas Fiscais de Produtos (NFe) e Notas Fiscais de Serviços (NFSe) através da API Omie. Ele oferece uma interface simples e interativa para visualizar informações detalhadas das notas, incluindo links para XML, DANFE e PDF da NFSe.

Funcionalidades

Consulta de NFe e NFSe pelo número da nota.

Exibição de informações detalhadas do emitente, destinatário e valores.

Listagem dos itens da NFe, com informações de produto, quantidade, NCM, CFOP e valor.

Listagem dos serviços da NFSe, incluindo código do serviço, cidade de prestação, alíquota ISS e valores.

Geração de links diretos para:

XML da NFe

DANFE da NFe

PDF da NFSe

Interface responsiva, amigável e de fácil uso.

Retorno de informações completas em JSON para análise ou integração adicional.

Tecnologias Utilizadas

Python 3.x

Flask

Requests

HTML, CSS e JavaScript para a interface web

Estrutura do Projeto
/projeto-consulta-nf
│
├─ app.py              # Aplicação Flask principal
├─ templates/          # (Opcional) Templates HTML, se usar render_template
└─ static/             # (Opcional) Arquivos CSS/JS adicionais

Como Executar

Clone o repositório:

git clone https://github.com/SEU_USUARIO/consulta-nf.git
cd consulta-nf


Instale as dependências:

pip install flask requests


Configure suas chaves APP_KEY e APP_SECRET da Omie no arquivo app.py.

Execute a aplicação:

python app.py


Abra o navegador e acesse:

http://127.0.0.1:5000/

Uso

Digite o número da NFe ou NFSe no formulário correspondente e clique em "Consultar".

Os detalhes da nota e os links para XML, DANFE ou PDF serão exibidos na mesma página.

Observações

O projeto utiliza as APIs oficiais da Omie. É necessário possuir uma conta ativa e as credenciais de acesso.

Para NFSe, a aplicação utiliza a API de ListarNFSEs e a API de ObterNFSe para gerar os links de download do PDF e XML.
