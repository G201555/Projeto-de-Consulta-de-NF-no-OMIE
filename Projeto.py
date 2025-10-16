from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

APP_KEY = "APP_KEY"
APP_SECRET = "APP_SECRET"

# Endpoints da Omie
URL_NF_PRODUTO = "https://app.omie.com.br/api/v1/produtos/nfconsultar/"
URL_NF_PDF = "https://app.omie.com.br/api/v1/produtos/notafiscalutil/"
URL_NFSE_LISTAR = "https://app.omie.com.br/api/v1/servicos/nfse/"
URL_OSDOCS = "https://app.omie.com.br/api/v1/servicos/osdocs/"

# ======================
# HTML COMPLETO
# ======================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Consulta NF - Produtos e Serviços</title>
    <style>
        /* Reset básico */
        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            background: #f4f6f8;
            color: #333;
        }

        header {
            background: #4CAF50;
            color: #fff;
            padding: 25px 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        header h1 {
            margin: 0;
            font-size: 2rem;
            letter-spacing: 1px;
        }

        main {
            max-width: 1100px;
            margin: 30px auto;
            padding: 0 20px;
        }

        h2 {
            color: #4CAF50;
            margin-bottom: 15px;
        }

        /* Container flexível para os formulários */
        .forms-container {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            margin-bottom: 30px;
        }

        form {
            background: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            flex: 1;
            min-width: 300px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        input[type="text"] {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 6px;
            transition: border 0.3s;
        }

        input[type="text"]:focus {
            border-color: #4CAF50;
            outline: none;
        }

        button {
            padding: 10px 20px;
            cursor: pointer;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 6px;
            transition: background 0.3s, transform 0.2s;
        }

        button:hover {
            background: #45a049;
            transform: translateY(-2px);
        }

        .resultado {
            background: #fff;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 6px 10px rgba(0,0,0,0.05);
        }

        .info {
            margin-bottom: 12px;
            font-size: 0.95rem;
        }

        a {
            text-decoration: none;
            color: white;
            background: #2196F3;
            padding: 8px 16px;
            border-radius: 6px;
            margin-right: 5px;
            display: inline-block;
            transition: background 0.3s;
        }

        a:hover {
            background: #0b7dda;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            font-size: 0.9rem;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 10px 8px;
            text-align: left;
        }

        th {
            background-color: #4CAF50;
            color: white;
        }

        tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        .scroll {
            overflow-x: auto;
        }

        /* Responsividade */
        @media (max-width: 768px) {
            .forms-container {
                flex-direction: column;
            }
            form {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <header>
        <h1>Consulta de Notas Fiscais</h1>
    </header>

    <main>
        <div class="forms-container">
            <form id="formProduto">
                <h2>🔹 Consultar NF de Produto</h2>
                <input type="text" id="numero_nf" placeholder="Número da NF" required>
                <button type="submit">Consultar Produto</button>
            </form>

            <form id="formServico">
                <h2>🔹 Consultar NF de Serviço</h2>
                <input type="text" id="numero_nfse" placeholder="Número da NFSe" required>
                <button type="submit">Consultar Serviço</button>
            </form>
        </div>

        <div class="resultado" id="resultado">
            <h2>Resultado:</h2>
            <div id="nfInfo"></div>
            <div id="links"></div>
            <div class="scroll" id="itensNF"></div>
        </div>
    </main>

    <script>
        async function consultar(endpoint, numero, tipo){
            const response = await fetch(endpoint, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({numero})
            });
            const data = await response.json();

            document.getElementById("nfInfo").innerHTML = "";
            document.getElementById("links").innerHTML = "";
            document.getElementById("itensNF").innerHTML = "";

            if(data.error){
                document.getElementById("nfInfo").innerText = data.error;
                return;
            }

            if(tipo === "produto"){
                const nf = data.consulta_nf;
                const linkXml = data.linkXml?.cUrlNF;
                const linkDanfe = data.linkDanfe?.cUrlDanfe;

                const infoHtml = `
                    <div class="info"><strong>NF:</strong> ${nf.ide.nNF} / Série: ${nf.ide.serie}</div>
                    <div class="info"><strong>Data de Emissão:</strong> ${nf.ide.dEmi}</div>
                    <div class="info"><strong>Emitente:</strong> ${nf.nfEmitInt?.cRazao ?? 'N/A'}</div>
                    <div class="info"><strong>Destinatário:</strong> ${nf.nfDestInt?.cRazao ?? 'N/A'}</div>
                    <div class="info"><strong>Valor Total:</strong> R$ ${nf.total.ICMSTot.vNF.toFixed(2)}</div>
                `;
                document.getElementById("nfInfo").innerHTML = infoHtml;

                let linksHtml = "";
                if(linkXml) linksHtml += `<a href="${linkXml}" target="_blank">Abrir XML</a>`;
                if(linkDanfe) linksHtml += `<a href="${linkDanfe}" target="_blank">Abrir DANFE</a>`;
                document.getElementById("links").innerHTML = linksHtml;

                if(nf.det && nf.det.length > 0){
                    let tableHtml = '<table><tr><th>Produto</th><th>CFOP</th><th>NCM</th><th>Qtd</th><th>Unid</th><th>Valor Unit.</th><th>Total</th></tr>';
                    nf.det.forEach(item => {
                        const prod = item.prod;
                        tableHtml += `<tr>
                            <td>${prod.cProd} - ${prod.xProd}</td>
                            <td>${prod.CFOP}</td>
                            <td>${prod.NCM}</td>
                            <td>${prod.qCom}</td>
                            <td>${prod.uCom}</td>
                            <td>R$ ${prod.nCMCUnitario.toFixed(2)}</td>
                            <td>R$ ${prod.vTotItem.toFixed(2)}</td>
                        </tr>`;
                    });
                    tableHtml += '</table>';
                    document.getElementById("itensNF").innerHTML = tableHtml;
                }
            } else {
                const nfse = data.consulta_nfse;
                const cab = nfse.Cabecalho;
                const serv = nfse.ListaServicos?.[0];

                const infoHtml = `
                    <div class="info"><strong>NFSe:</strong> ${cab.nNumeroNFSe}</div>
                    <div class="info"><strong>Razão Emitente:</strong> ${cab.cRazaoEmissor}</div>
                    <div class="info"><strong>Razão Destinatário:</strong> ${cab.cRazaoDestinatario}</div>
                    <div class="info"><strong>Valor Total:</strong> R$ ${cab.nValorNFSe.toFixed(2)}</div>
                    <div class="info"><strong>Data de Emissão:</strong> ${nfse.Emissao.cDataEmissao}</div>
                `;
                document.getElementById("nfInfo").innerHTML = infoHtml;

                const linksHtml = `
                    ${data.links?.cUrlNFSe ? `<a href="${data.links.cUrlNFSe}" target="_blank">NFSe Prefeitura</a>` : ""}
                    ${data.links?.cPdfNFSe ? `<a href="${data.links.cPdfNFSe}" target="_blank">PDF NFSe</a>` : ""}
                    ${data.links?.cXmlNFSe ? `<a href="${data.links.cXmlNFSe}" target="_blank">XML NFSe</a>` : ""}
                    ${data.links?.cLinkPortal ? `<a href="${data.links.cLinkPortal}" target="_blank">Portal Omie</a>` : ""}
                `;
                document.getElementById("links").innerHTML = linksHtml;

                if(serv){
                    let tableHtml = '<table><tr><th>Código Serviço</th><th>Cidade</th><th>Aliquota ISS</th><th>Valor Serviço</th><th>Valor Total</th></tr>';
                    tableHtml += `
                        <tr>
                            <td>${serv.CodigoServico}</td>
                            <td>${serv.CidadePrestacao}</td>
                            <td>${serv.nAliquotaISS}%</td>
                            <td>R$ ${serv.nValorServico.toFixed(2)}</td>
                            <td>R$ ${serv.nValorTotal.toFixed(2)}</td>
                        </tr>
                    </table>`;
                    document.getElementById("itensNF").innerHTML = tableHtml;
                }
            }
        }

        document.getElementById("formProduto").addEventListener("submit", e => {
            e.preventDefault();
            consultar("/get_nfe", document.getElementById("numero_nf").value, "produto");
        });

        document.getElementById("formServico").addEventListener("submit", e => {
            e.preventDefault();
            consultar("/get_nfse", document.getElementById("numero_nfse").value, "servico");
        });
    </script>
</body>
</html>
"""

# ======================
# ROTA PRINCIPAL
# ======================
@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_TEMPLATE)

# ======================
# NF DE PRODUTO
# ======================
@app.route("/get_nfe", methods=["POST"])
def get_nfe():
    data = request.get_json()
    numero_nf = data.get("numero")

    if not numero_nf:
        return jsonify({"error": "Digite o número da NF (nNF)"}), 400

    payload_nf = {
        "call": "ConsultarNF",
        "app_key": APP_KEY,
        "app_secret": APP_SECRET,
        "param": [{"nNF": int(numero_nf)}]
    }

    res_nf = requests.post(URL_NF_PRODUTO, json=payload_nf).json()

    if "error" in res_nf:
        return jsonify({"error": res_nf["error"]})

    nIdNF = res_nf.get("compl", {}).get("nIdNF")
    url_nf = None
    url_danfe = None

    if nIdNF:
        payload_xml = {
            "call": "GetUrlNotaFiscal",
            "app_key": APP_KEY,
            "app_secret": APP_SECRET,
            "param": [{"nCodNF": nIdNF, "cCodNFInt": ""}]
        }
        res_xml = requests.post(URL_NF_PDF, json=payload_xml).json()
        url_nf = res_xml.get("cUrlNF")

        payload_danfe = {
            "call": "GetUrlDanfe",
            "app_key": APP_KEY,
            "app_secret": APP_SECRET,
            "param": [{"nCodNF": nIdNF, "cCodNFInt": ""}]
        }
        res_danfe = requests.post(URL_NF_PDF, json=payload_danfe).json()
        url_danfe = res_danfe.get("cUrlDanfe")

    return jsonify({
        "consulta_nf": res_nf,
        "linkXml": {"cUrlNF": url_nf},
        "linkDanfe": {"cUrlDanfe": url_danfe}
    })

# ======================
# NF DE SERVIÇO (ATUALIZADO COM LINKS)
# ======================
@app.route("/get_nfse", methods=["POST"])
def get_nfse():
    data = request.get_json()
    numero_nfse = data.get("numero")

    if not numero_nfse:
        return jsonify({"error": "Digite o número da NFSe"}), 400

    # ListarNFSEs para obter nIdNF
    payload_nfse = {
        "call": "ListarNFSEs",
        "app_key": APP_KEY,
        "app_secret": APP_SECRET,
        "param": [{"nNumeroNFSe": str(numero_nfse)}]
    }

    try:
        res_nfse = requests.post(URL_NFSE_LISTAR, json=payload_nfse, timeout=10)
        res_nfse.raise_for_status()
        res_json = res_nfse.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erro na requisição: {str(e)}"}), 500
    except ValueError:
        return jsonify({"error": "Resposta inválida da API Omie"}), 500

    if "error" in res_json:
        return jsonify({"error": res_json["error"], "payload": payload_nfse})

    lista = res_json.get("nfseEncontradas", [])
    if not lista:
        return jsonify({"error": "NFSe não encontrada.", "payload": payload_nfse, "resposta_completa": res_json})

    nfse_dados = lista[0]
    nIdNF = nfse_dados.get("Cabecalho", {}).get("nCodNF")
    links = {}

    if nIdNF:
        payload_links = {
            "call": "ObterNFSe",
            "app_key": APP_KEY,
            "app_secret": APP_SECRET,
            "param": [{"nIdNf": nIdNF}]
        }
        try:
            res_links = requests.post(URL_OSDOCS, json=payload_links).json()
            links = {
                "cUrlNFSe": res_links.get("cUrlNFSe"),
                "cPdfNFSe": res_links.get("cPdfNFSe"),
                "cXmlNFSe": res_links.get("cXmlNFSe"),
                "cLinkPortal": res_links.get("cLinkPortal")
            }
        except:
            links = {}

    resultado = {
        "consulta_nfse": {
            "Cabecalho": nfse_dados.get("Cabecalho", {}),
            "Emissao": nfse_dados.get("Emissao", {}),
            "ListaServicos": nfse_dados.get("ListaServicos", [])
        },
        "links": links
    }

    return jsonify(resultado)

if __name__ == "__main__":
    print("Servidor rodando! Acesse http://127.0.0.1:5000/")
    app.run(debug=True)
