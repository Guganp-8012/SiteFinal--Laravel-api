from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from .models import *
from .forms import *
import requests


def VerIndex(request):
    busca_os = OrdemServico.objects.all()

    for os in busca_os:
        valor_os = 0
        for servico in os.servico.all():
            valor_os += servico.valor_servico
        os.valor_total = valor_os

    return render(request, "index.html", {'ordemservicos': busca_os})


def RetornaToken(request):
    url = 'http://127.0.0.1:9000/api/login' # Substitua pela URL da API real
    try:
        # Dados que você deseja enviar no corpo da solicitação POST
        json = {
            'email': 'gustavo.rios801208@gmail.com',
            'password' : 'Gueobama'
        }
        # Cabeçalhos que você deseja enviar com a solicitação
        headers = {
            'Content-Type': 'application/json'
        }

        # Fazendo a solicitação POST
        request = requests.post(url, json=json, headers=headers)
        response = request.json()
    except requests.RequestException as e:
        return HttpResponse(f'Erro ao consumir a API: {str(e)}', status=500)
    
    return HttpResponse(response['token'], content_type="text/plain")


def CriarCategoria(request):
    url = 'http://127.0.0.1:9000/api/categorias'

    obter_token = RetornaToken(request)
    conteudo_bytes = obter_token.content
    token = conteudo_bytes.decode('utf-8') 

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    
    if request.method == "GET":
        nova_categoria = FormularioCategoria()

        try:
            resposta = requests.get(url, headers=headers)
            resposta.raise_for_status()
            dados = resposta.json()
        except requests.RequestException as e:
            return HttpResponse(f'Erro ao consumir a API: {str(e)}', status=500)
    
        categorias = dados['categorias']
        return render(request, "form-categoria.html", {"form_categoria": nova_categoria, "categorias": categorias})
    else:
        json = {
            'tipo': request.POST['tipo']
        }
                
        response = requests.post(url, json=json, headers=headers)
        
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()
                return redirect("pg_criar_categoria")
            except requests.JSONDecodeError:
                print("A resposta não é um JSON válido.")
        else:
            return HttpResponse('Erro ao consumir a API: ', response.status_code)
def EditarCategoria(request, id_categoria):
    url_editar_categoria = 'http://127.0.0.1:9000/api/categorias/' + str(id_categoria) # Substitua pela URL da API real
    url_listar_categorias = 'http://127.0.0.1:9000/api/categorias' # Substitua pela URL da API real

    obter_token = RetornaToken(request)
    conteudo_bytes = obter_token.content  # Obtém o conteúdo como bytes
    token = conteudo_bytes.decode('utf-8') 

    # Cabeçalhos que você deseja enviar com a solicitação
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    resposta = requests.get(url_editar_categoria, headers=headers)
    resposta.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
    dados = resposta.json()
    categoria = dados['categoria']

    resposta_categorias = requests.get(url_listar_categorias, headers=headers)
    resposta_categorias.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
    dados_categorias = resposta_categorias.json() # Obtém os dados JSON da resposta
    categorias = dados_categorias['categorias']

    if request.method == "GET":
        return render(request, "form-categoria.html", {"categoria": categoria, 'categorias' : categorias}) 
    else:
        # Dados que você deseja enviar no corpo da solicitação POST
        json = {
            'tipo': request.POST['tipo']
        }
               
        # Fazendo a solicitação POST
        response = requests.put(url_editar_categoria, json=json, headers=headers)

        # Obtendo o conteúdo da resposta
        
        if response.status_code in [200, 201]:
            try:
                return redirect("pg_criar_categoria")
            except requests.JSONDecodeError:
                print("A resposta não é um JSON válido.")
        else:
            return render(request, "form-categoria.html", {"categoria": categoria, 'categorias' : categorias}) 
def ExcluirCategoria(request, id_categoria):
          url = 'http://127.0.0.1:9000/api/categorias/' + str(id_categoria)
      
          obter_token = RetornaToken(request)
          conteudo_bytes = obter_token.content
          token = conteudo_bytes.decode('utf-8') 
      
          headers = {
              'Authorization': 'Bearer ' + token,
              'Content-Type': 'application/json'
          }
          
          if request.method == "GET":             
              response = requests.delete(url, headers=headers)
              
              if response.status_code in [200]:
                  try:
                      return redirect("pg_criar_categoria")
                  except requests.JSONDecodeError:
                      print("A resposta não é um JSON válido.")
              else:
                  return HttpResponse('Erro ao consumir a API: ', response.status_code)


def CriarEmpresa(request):
    url = 'http://127.0.0.1:9000/api/empresas'

    obter_token = RetornaToken(request)
    conteudo_bytes = obter_token.content
    token = conteudo_bytes.decode('utf-8') 

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    
    if request.method == "GET":
        nova_empresa = FormularioEmpresa()

        try:
            resposta = requests.get(url, headers=headers)
            resposta.raise_for_status()
            dados = resposta.json()
        except requests.RequestException as e:
            return HttpResponse(f'Erro ao consumir a API: {str(e)}', status=500)
    
        empresas = dados['empresas']
        return render(request, "form-empresa.html", {"form_empresa": nova_empresa, "empresas": empresas})
    else:
        json = {
            'razao_social': request.POST['razao_social'],
            'cnpj': request.POST['cnpj'],
            'endereco': request.POST['endereco'],
            'celular': request.POST['celular']
        }
                
        response = requests.post(url, json=json, headers=headers)
        
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()
                return redirect("pg_criar_empresa")
            except requests.JSONDecodeError:
                print("A resposta não é um JSON válido.")
        else:
            return HttpResponse('Erro ao consumir a API: ', response.status_code)      
def EditarEmpresa(request, id_empresa):
    url_editar_empresa = 'http://127.0.0.1:9000/api/empresas/' + str(id_empresa) # Substitua pela URL da API real
    url_listar_empresas = 'http://127.0.0.1:9000/api/empresas' # Substitua pela URL da API real

    obter_token = RetornaToken(request)
    conteudo_bytes = obter_token.content  # Obtém o conteúdo como bytes
    token = conteudo_bytes.decode('utf-8') 

    # Cabeçalhos que você deseja enviar com a solicitação
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    resposta = requests.get(url_editar_empresa, headers=headers)
    resposta.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
    dados = resposta.json()
    empresa = dados['empresa']

    resposta_empresas = requests.get(url_listar_empresas, headers=headers)
    resposta_empresas.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
    dados_empresas = resposta_empresas.json() # Obtém os dados JSON da resposta
    empresas = dados_empresas['empresas']

    if request.method == "GET":
        return render(request, "form-empresa.html", {"empresa": empresa, 'empresas' : empresas}) 
    else:
        # Dados que você deseja enviar no corpo da solicitação POST
        json = {
            'razao_social': request.POST['razao_social'],
            'cnpj': request.POST['cnpj'],
            'endereco': request.POST['endereco'],
            'celular': request.POST['celular']
        }
               
        # Fazendo a solicitação POST
        response = requests.put(url_editar_empresa, json=json, headers=headers)

        # Obtendo o conteúdo da resposta
        
        if response.status_code in [200, 201]:
            try:
                return redirect("pg_criar_empresa")
            except requests.JSONDecodeError:
                print("A resposta não é um JSON válido.")
        else:
            return render(request, "form-empresa.html", {"empresa": empresa, 'empresas' : empresas}) 
def ExcluirEmpresa(request, id_empresa):
    url = 'http://127.0.0.1:9000/api/empresas/' + str(id_empresa)

    obter_token = RetornaToken(request)
    conteudo_bytes = obter_token.content
    token = conteudo_bytes.decode('utf-8') 

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    if request.method == "GET":             
        response = requests.delete(url, headers=headers)
        
        if response.status_code in [200]:
            try:
                return redirect("pg_criar_empresa")
            except requests.JSONDecodeError:
                print("A resposta não é um JSON válido.")
        else:
            return HttpResponse('Erro ao consumir a API: ', response.status_code)


def CriarCliente(request):
    url = 'http://127.0.0.1:9000/api/clientes'  # Substitua pela URL da API real

    obter_token = RetornaToken(request)
    conteudo_bytes = obter_token.content  # Obtém o conteúdo como bytes
    token = conteudo_bytes.decode('utf-8') 

    # Cabeçalhos que você deseja enviar com a solicitação
    headers = {
        'Authorization': 'Bearer ' + token,
        # 'Content-Type': 'application/json'
    }
    
    if request.method == "GET":
        try:
            resposta = requests.get(url, headers=headers)
            resposta.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
            dados = resposta.json()  # Obtém os dados JSON da resposta
        except requests.RequestException as e:
            return HttpResponse(f'Erro ao consumir a API: {str(e)}', status=500)
    
        # Extraia a string desejada do JSON
        clientes = dados['clientes']
        return render(request, "form-cliente.html", { "clientes": clientes })
    else:
        # Dados que você deseja enviar no corpo da solicitação POST
        foto = request.FILES.get('foto')
        nome = request.POST['nome']
        data_nascimento = request.POST['data_nascimento']
        status = request.POST['status']

        # Preparando os dados para envio
        files = {
            'foto': (foto.name, foto, foto.content_type)
        }
        data = {
            'nome': nome,
            'data_nascimento': data_nascimento,
            'status': status
        }
       
        response = requests.post(url, data=data, files=files, headers=headers)

        # return HttpResponse(response)
        
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()
                return redirect("pg_criar_cliente")
            except requests.JSONDecodeError:
                return HttpResponse("A resposta não é um JSON válido.", status=500)
        else:
            return HttpResponse(f'Erro na solicitação: {response.status_code}', status=response.status_code)
def EditarCliente(request, id_cliente):
    url_editar_cliente = 'http://127.0.0.1:9000/api/clientes/' + str(id_cliente) # Substitua pela URL da API real
    url_listar_clientes = 'http://127.0.0.1:9000/api/clientes' # Substitua pela URL da API real

    obter_token = RetornaToken(request)
    conteudo_bytes = obter_token.content  # Obtém o conteúdo como bytes
    token = conteudo_bytes.decode('utf-8') 

    # Cabeçalhos que você deseja enviar com a solicitação
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    resposta = requests.get(url_editar_cliente, headers=headers)
    resposta.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
    dados = resposta.json()
    cliente = dados['cliente']

    resposta_clientes = requests.get(url_listar_clientes, headers=headers)
    resposta_clientes.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
    dados_clientes = resposta_clientes.json() # Obtém os dados JSON da resposta
    clientes = dados_clientes['clientes']

    if request.method == "GET":
        return render(request, "form-cliente.html", {"cliente": cliente, 'clientes' : clientes}) 
    else:
        # Dados que você deseja enviar no corpo da solicitação POST
        foto = request.FILES.get('foto')
        nome = request.POST['nome']
        data_nascimento = request.POST['data_nascimento']
        status = request.POST['status']

        # Preparando os dados para envio
        files = {
            'foto': (foto.name, foto, foto.content_type)
        }
        data = {
            'nome': nome,
            'data_nascimento': data_nascimento,
            'status': status
        }
               
        # Fazendo a solicitação POST
        response = requests.put(url_editar_cliente, data=data, files=files, headers=headers)

        # Obtendo o conteúdo da resposta
        
        if response.status_code in [200, 201]:
            try:
                return redirect("pg_criar_cliente")
            except requests.JSONDecodeError:
                print("A resposta não é um JSON válido.")
        else:
            return render(request, "form-cliente.html", {"cliente": cliente, 'clientes' : clientes}) 
def ExcluirCliente(request, id_cliente):
          url = 'http://127.0.0.1:9000/api/clientes/' + str(id_cliente)
      
          obter_token = RetornaToken(request)
          conteudo_bytes = obter_token.content
          token = conteudo_bytes.decode('utf-8') 
      
          headers = {
              'Authorization': 'Bearer ' + token,
              'Content-Type': 'application/json'
          }
          
          if request.method == "GET":             
              response = requests.delete(url, headers=headers)
              
              if response.status_code in [200]:
                  try:
                      return redirect("pg_criar_cliente")
                  except requests.JSONDecodeError:
                      print("A resposta não é um JSON válido.")
              else:
                  return HttpResponse('Erro ao consumir a API: ', response.status_code)


def CriarProduto(request):
    url = 'http://127.0.0.1:9000/api/produtos'

    obter_token = RetornaToken(request)
    conteudo_bytes = obter_token.content
    token = conteudo_bytes.decode('utf-8') 

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    
    if request.method == "GET":
        nova_produto = FormularioProduto
        try:
            resposta = requests.get(url, headers=headers)
            resposta.raise_for_status()
            dados = resposta.json()
        except requests.RequestException as e:
            return HttpResponse(f'Erro ao consumir a API: {str(e)}', status=500)
    
        produtos = dados['produtos']
        return render(request, "form-produto.html", {"form_produto": nova_produto, "produtos": produtos})
    else:
        json = {
            'nome': request.POST['nome'],
            'valor': request.POST['valor'],
            'descricao': request.POST['descricao']
        }
                
        response = requests.post(url, json=json, headers=headers)
        
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()
                return redirect("pg_criar_produto")
            except requests.JSONDecodeError:
                print("A resposta não é um JSON válido.")
        else:
            return HttpResponse('Erro ao consumir a API: ', response.status_code)
def EditarProduto(request, id_produto):
    url_editar_produto = 'http://127.0.0.1:9000/api/produtos/' + str(id_produto) # Substitua pela URL da API real
    url_listar_produtos = 'http://127.0.0.1:9000/api/produtos' # Substitua pela URL da API real

    obter_token = RetornaToken(request)
    conteudo_bytes = obter_token.content  # Obtém o conteúdo como bytes
    token = conteudo_bytes.decode('utf-8') 

    # Cabeçalhos que você deseja enviar com a solicitação
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    resposta = requests.get(url_editar_produto, headers=headers)
    resposta.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
    dados = resposta.json()
    produto = dados['produto']

    resposta_produtos = requests.get(url_listar_produtos, headers=headers)
    resposta_produtos.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
    dados_produtos = resposta_produtos.json() # Obtém os dados JSON da resposta
    produtos = dados_produtos['produtos']

    if request.method == "GET":
        return render(request, "form-produto.html", {"produto": produto, 'produtos' : produtos}) 
    else:
        # Dados que você deseja enviar no corpo da solicitação POST
        json = {
            'nome': request.POST['nome'],
            'valor': request.POST['valor'],
            'descricao': request.POST['descricao']
        }
               
        # Fazendo a solicitação POST
        response = requests.put(url_editar_produto, json=json, headers=headers)

        # Obtendo o conteúdo da resposta
        
        if response.status_code in [200, 201]:
            try:
                return redirect("pg_criar_produto")
            except requests.JSONDecodeError:
                print("A resposta não é um JSON válido.")
        else:
            return render(request, "form-produto.html", {"produto": produto, 'produtos' : produtos}) 
def ExcluirProduto(request, id_produto):
          url = 'http://127.0.0.1:9000/api/produtos/' + str(id_produto)
      
          obter_token = RetornaToken(request)
          conteudo_bytes = obter_token.content
          token = conteudo_bytes.decode('utf-8') 
      
          headers = {
              'Authorization': 'Bearer ' + token,
              'Content-Type': 'application/json'
          }
          
          if request.method == "GET":             
              response = requests.delete(url, headers=headers)
              
              if response.status_code in [200]:
                  try:
                      return redirect("pg_criar_produto")
                  except requests.JSONDecodeError:
                      print("A resposta não é um JSON válido.")
              else:
                  return HttpResponse('Erro ao consumir a API: ', response.status_code)


def CriarServico(request):
    url = 'http://127.0.0.1:9000/api/servicos' # Substitua pela URL da API real
    url_categorias = 'http://127.0.0.1:9000/api/categorias'
    url_empresas = 'http://127.0.0.1:9000/api/empresas'

    obter_token = RetornaToken(request)
    conteudo_bytes = obter_token.content  # Obtém o conteúdo como bytes
    token = conteudo_bytes.decode('utf-8') 

    # Cabeçalhos que você deseja enviar com a solicitação
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    resposta_categorias = requests.get(url_categorias, headers=headers)
    resposta_categorias.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
    dados_categorias = resposta_categorias.json() # Obtém os dados JSON da resposta
    categorias = dados_categorias['categorias']

    resposta_empresas = requests.get(url_empresas, headers=headers)
    resposta_empresas.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
    dados_empresas = resposta_empresas.json() # Obtém os dados JSON da resposta
    empresas = dados_empresas['empresas']
    
    if request.method == "GET":
        novo_servico = FormularioServico()

        try:
            resposta = requests.get(url, headers=headers)
            resposta.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
            dados = resposta.json() # Obtém os dados JSON da resposta
        except requests.RequestException as e:
            return HttpResponse(f'Erro ao consumir a API: {str(e)}', status=500)
    
        # Extraia a string desejada do JSON
        servicos = dados['servicos']
        return render(request, "form-servico.html", {"categorias": categorias, "empresas": empresas, "servicos": servicos})
    else:
       # Dados que você deseja enviar no corpo da solicitação POST
        json = {
            'tipo': request.POST['tipo'],
            'valor': request.POST['valor'],
            'empresa_id': request.POST['empresa_id'],
            'categoria_id': request.POST['categoria_id']
        }
               
        # Fazendo a solicitação POST
        response = requests.post(url, json=json, headers=headers)

        # Obtendo o conteúdo da resposta
        
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()
                return redirect("pg_criar_servico")
            except requests.JSONDecodeError:
                print("A resposta não é um JSON válido.")
        else:
            return HttpResponse('Erro ao consumir a API: ', response.status_code)
def EditarServico(request, id_servico):
    url_editar_servico = 'http://127.0.0.1:9000/api/servicos/' + str(id_servico) # Substitua pela URL da API real
    url_listar_servicos = 'http://127.0.0.1:9000/api/servicos' # Substitua pela URL da API real
    url_categorias = 'http://127.0.0.1:9000/api/categorias'
    url_empresas = 'http://127.0.0.1:9000/api/empresas'

    obter_token = RetornaToken(request)
    conteudo_bytes = obter_token.content  # Obtém o conteúdo como bytes
    token = conteudo_bytes.decode('utf-8') 

    # Cabeçalhos que você deseja enviar com a solicitação
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    resposta = requests.get(url_editar_servico, headers=headers)
    resposta.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
    dados = resposta.json()
    servico = dados['servico']

    # Obter os dados do serviço
    resposta_servicos = requests.get(url_listar_servicos, headers=headers)
    resposta_servicos.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
    dados_servicos = resposta_servicos.json() # Obtém os dados JSON da resposta
    servicos = dados_servicos['servicos']

    # Obter categorias
    resposta_categorias = requests.get(url_categorias, headers=headers)
    resposta_categorias.raise_for_status()
    dados_categorias = resposta_categorias.json()
    categorias = dados_categorias['categorias']

    # Obter empresas
    resposta_empresas = requests.get(url_empresas, headers=headers)
    resposta_empresas.raise_for_status()
    dados_empresas = resposta_empresas.json()
    empresas = dados_empresas['empresas']

    if request.method == "GET":
        return render(request, "form-servico.html", {"servico": servico, 'servicos' : servicos, "categorias": categorias, "empresas": empresas})
    else:
        # Dados que você deseja enviar no corpo da solicitação POST
        json = {
            'tipo': request.POST['tipo'],
            'valor': request.POST['valor'],
            'empresa_id': request.POST['empresa_id'],
            'categoria_id': request.POST['categoria_id']
        }
               
        # Fazendo a solicitação POST
        response = requests.put(url_editar_servico, json=json, headers=headers)

        # Obtendo o conteúdo da resposta
        
        if response.status_code in [200, 201]:
            try:
                return redirect("pg_criar_servico")
            except requests.JSONDecodeError:
                print("A resposta não é um JSON válido.")
        else:
            return render(request, "form-servico.html", {"servico": servico, 'servicos' : servicos}) 
def ExcluirServico(request, id_servico):
          url = 'http://127.0.0.1:9000/api/servicos/' + str(id_servico)
      
          obter_token = RetornaToken(request)
          conteudo_bytes = obter_token.content
          token = conteudo_bytes.decode('utf-8') 
      
          headers = {
              'Authorization': 'Bearer ' + token,
              'Content-Type': 'application/json'
          }
          
          if request.method == "GET":             
              response = requests.delete(url, headers=headers)
              
              if response.status_code in [200]:
                  try:
                      return redirect("pg_criar_servico")
                  except requests.JSONDecodeError:
                      print("A resposta não é um JSON válido.")
              else:
                  return HttpResponse('Erro ao consumir a API: ', response.status_code)


def CriarOrdemServico(request): 
    url = 'http://127.0.0.1:9000/api/ordem_servicos' # Substitua pela URL da API real
    url_clientes = 'http://127.0.0.1:9000/api/clientes'
    url_servicos = 'http://127.0.0.1:9000/api/servicos'

    obter_token = RetornaToken(request)
    conteudo_bytes = obter_token.content  # Obtém o conteúdo como bytes
    token = conteudo_bytes.decode('utf-8') 

    # Cabeçalhos que você deseja enviar com a solicitação
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    resposta_clientes = requests.get(url_clientes, headers=headers)
    resposta_clientes.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
    dados_clientes = resposta_clientes.json() # Obtém os dados JSON da resposta
    clientes = dados_clientes['clientes']

    resposta_servicos = requests.get(url_servicos, headers=headers)
    resposta_servicos.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
    dados_servicos = resposta_servicos.json() # Obtém os dados JSON da resposta
    servicos = dados_servicos['servicos']
   
    
    if request.method == "GET":
        nova_ordemservico = FormularioOrdemServico()

        try:
            resposta = requests.get(url, headers=headers)
            resposta.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
            dados = resposta.json() # Obtém os dados JSON da resposta
        except requests.RequestException as e:
            return HttpResponse(f'Erro ao consumir a API: {str(e)}', status=500)
    
        # Extraia a string desejada do JSON
        ordem_servicos = dados['ordem_servicos']
        return render(request, "form-ordemservico.html", {"clientes": clientes, "servicos": servicos, "ordem_servicos": ordem_servicos})
    else:
       # Dados que você deseja enviar no corpo da solicitação POST
        json = {
            'cliente_id': request.POST['cliente_id'],
            'servico_id': request.POST['servico_id'],
            'data_inicio': request.POST['data_inicio'],
            'data_finalizacao': request.POST['data_finalizacao'],
            'status': request.POST['status'],
        }
               
        # Fazendo a solicitação POST
        response = requests.post(url, json=json, headers=headers)

        # Obtendo o conteúdo da resposta
        
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()
                return redirect("pg_criar_ordemservico")
            except requests.JSONDecodeError:
                print("A resposta não é um JSON válido.")
        else:
            return HttpResponse('Erro ao consumir a API: ', response.status_code)
def EditarOrdemServico(request, id_ordem_servico):
    url_editar_ordem_servico = 'http://127.0.0.1:9000/api/ordem_servicos/' + str(id_ordem_servico) # Substitua pela URL da API real
    url_listar_ordem_servicos = 'http://127.0.0.1:9000/api/ordem_servicos' # Substitua pela URL da API real
    url_clientes = 'http://127.0.0.1:9000/api/clientes'
    url_servicos = 'http://127.0.0.1:9000/api/servicos'

    obter_token = RetornaToken(request)
    conteudo_bytes = obter_token.content  # Obtém o conteúdo como bytes
    token = conteudo_bytes.decode('utf-8') 

    # Cabeçalhos que você deseja enviar com a solicitação
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    resposta = requests.get(url_editar_ordem_servico, headers=headers)
    resposta.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
    dados = resposta.json()
    ordem_servico = dados['ordem_servico']

    # Obter os dados de ordens de serviço
    resposta_ordem_servicos = requests.get(url_listar_ordem_servicos, headers=headers)
    resposta_ordem_servicos.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
    dados_ordem_servicos = resposta_ordem_servicos.json() # Obtém os dados JSON da resposta
    ordem_servicos = dados_ordem_servicos['ordem_servicos']

    # Obter clientes
    resposta_clientes = requests.get(url_clientes, headers=headers)
    resposta_clientes.raise_for_status()
    dados_clientes = resposta_clientes.json()
    clientes = dados_clientes['clientes']


    # Obter servicos
    resposta_servicos = requests.get(url_servicos, headers=headers)
    resposta_servicos.raise_for_status()
    dados_servicos = resposta_servicos.json()
    servicos = dados_servicos['servicos']

    if request.method == "GET":
        return render(request, "form-ordemservico.html", {"ordem_servico": ordem_servico, 'ordem_servicos' : ordem_servicos, "clientes": clientes, "servicos": servicos})
    else:
        # Dados que você deseja enviar no corpo da solicitação POST
        json = {
            'tipo': request.POST['tipo'],
            'valor': request.POST['valor'],
            'servico_id': request.POST['servico_id'],
            'cliente_id': request.POST['cliente_id']
        }
               
        # Fazendo a solicitação POST
        response = requests.put(url_editar_ordem_servico, json=json, headers=headers)

        # Obtendo o conteúdo da resposta
        
        if response.status_code in [200, 201]:
            try:
                return redirect("pg_criar_ordem_servico")
            except requests.JSONDecodeError:
                print("A resposta não é um JSON válido.")
        else:
            return render(request, "form-ordemservico.html", {"ordem_servico": ordem_servico, 'ordem_servicos' : ordem_servicos}) 
def ExcluirOrdemServico(request, id_ordem_servico):
          url = 'http://127.0.0.1:9000/api/ordem_servicos/' + str(id_ordem_servico) # Substitua pela URL da API real
      
          obter_token = RetornaToken(request)
          conteudo_bytes = obter_token.content  # Obtém o conteúdo como bytes
          token = conteudo_bytes.decode('utf-8') 
      
          # Cabeçalhos que você deseja enviar com a solicitação
          headers = {
              'Authorization': 'Bearer ' + token,
              'Content-Type': 'application/json'
          }
          
          if request.method == "GET":             
              # Fazendo a solicitação DELETE
              response = requests.delete(url, headers=headers)
      
              # Obtendo o conteúdo da resposta
              
              if response.status_code in [200]:
                  try:
                      return redirect("pg_criar_ordemservico")
                  except requests.JSONDecodeError:
                      print("A resposta não é um JSON válido.")
              else:
                  return HttpResponse('Erro ao consumir a API: ', response.status_code)