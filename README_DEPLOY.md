## Tutorial: Como Fazer Deploy de uma Aplicação Flask no PythonAnywhere

### 1. **Preparação**

Antes de começar, certifique-se de que:

- Você tenha uma conta no [PythonAnywhere](https://www.pythonanywhere.com/).
- Seu código-fonte esteja pronto e funcionando localmente com Flask.

### 2. **Configuração do Ambiente**

#### **2.1. Crie um Novo Projeto no PythonAnywhere**

1. **Faça login** na sua conta do PythonAnywhere.
2. Vá para a seção **"Web"** no painel de controle.
3. Clique no botão **"Add a new web app"**.

#### **2.2. Escolha o Tipo de Aplicação**

1. Selecione **Flask** como o framework para sua aplicação.
2. Escolha a versão do Python que você está usando.

### 3. **Preparação do Código**

#### **3.1. Prepare o Código para Deploy**

1. **Verifique** se seu código está no formato adequado para produção.
2. Certifique-se de que o arquivo principal do Flask (`app.py`, por exemplo) está configurado corretamente. Um exemplo básico é:

    ```python
    from flask import Flask

    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Hello, World!"

    if __name__ == "__main__":
        app.run()
    ```
3. Adicionalmente, você pode carregar o código no github e 


Claro! Aqui está a seção atualizada com uma sugestão para carregar o código no GitHub e cloná-lo no PythonAnywhere:

---

#### **3.1. Prepare o Código para Deploy**

1. **Verifique** se seu código está no formato adequado para produção.
2. **Certifique-se de que o arquivo principal do Flask** (por exemplo, `app.py`) está configurado corretamente. Um exemplo básico é:

    ```python
    from flask import Flask

    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Hello, World!"

    if __name__ == "__main__":
        app.run()
    ```

3. **Carregue seu código no GitHub**:
   - Se ainda não fez isso, crie um repositório no [GitHub](https://github.com/) e faça o upload do seu código.

4. **Clone o repositório no PythonAnywhere**:
   - Abra um novo **console Bash** no PythonAnywhere.
   - Navegue até o diretório onde deseja clonar o repositório:

     ```bash
     cd ~/your_project_directory
     ```

   - Clone o repositório usando o comando `git clone`. Substitua `your-repo-url` pela URL do seu repositório GitHub:

     ```bash
     git clone https://github.com/username/your-repository.git
     ```

   - Navegue até o diretório do repositório clonado:

     ```bash
     cd your-repository
     ```

   - Ou vá para a seção **"Files"** no painel de controle. Use o **"Upload a file"** para enviar o código para a pasta desejada, geralmente em `/home/username/your_project/`.

### 4. **Configuração do Ambiente Virtual com Pipenv**

#### **4.1. Instale Pipenv (se não estiver instalado)**

1. Abra um novo **console Bash**.
2. Verifique se `pipenv` está instalado. Caso contrário, instale-o com:

    ```bash
    pip install pipenv
    ```

#### **4.2. Crie um Ambiente Virtual com Pipenv**

1. Navegue até o diretório do seu projeto:

    ```bash
    cd ~/your_project
    ```

2. Crie um ambiente virtual e instale as dependências definidas no `Pipfile`:

    ```bash
    pipenv install
    ```

   Se você ainda não tiver um `Pipfile`, você pode criar um e adicionar suas dependências:

    ```bash
    pipenv install flask
    ```

   Ou se você já tem um `Pipfile.lock` com suas dependências, basta executar:

    ```bash
    pipenv install --ignore-pipfile
    ```

3. **Ative o ambiente virtual**:

    ```bash
    pipenv shell
    ```

### 5. **Configuração do Web App**

#### **5.1. Configure o Arquivo WSGI**

1. Na seção **"Web"** do painel de controle, localize e edite o arquivo WSGI (`/var/www/your_project_wsgi.py`).

2. Configure o arquivo WSGI para apontar para sua aplicação Flask. Por exemplo:

    ```python
    import sys
    import os
    from pathlib import Path

    # Adicione o diretório do projeto ao caminho
    project_home = '/home/username/your_project'
    if project_home not in sys.path:
        sys.path.append(project_home)

    from app import app as application
    ```

   Certifique-se de substituir `app` pelo nome do seu arquivo Python principal (sem a extensão `.py`).

#### **5.2. Configure o Web App**

1. Na seção **"Web"**, ajuste as configurações da aplicação:
   - **Source code**: O diretório onde seu código está localizado.
   - **Working directory**: O diretório de trabalho do seu projeto.
   - **Virtualenv**: O caminho para o ambiente virtual criado com `pipenv`. Normalmente, será algo como `/home/username/your_project/.venv`.

2. **Defina o "Static files"** e **"Media files"** se sua aplicação tiver arquivos estáticos ou de mídia.

### 6. **Reinicie o Web App**

1. Na seção **"Web"**, clique no botão **"Reload"** para reiniciar o seu web app e aplicar as novas configurações.

### 7. **Verificação e Testes**

1. **Acesse seu site** usando o domínio fornecido pelo PythonAnywhere para verificar se tudo está funcionando corretamente.
2. Verifique os **arquivos de log** em caso de problemas (como descrito anteriormente) para depurar qualquer erro.
