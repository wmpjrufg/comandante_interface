## Tutorial: Como Acessar os Arquivos de Log no PythonAnywhere

### 1. **Acessando o Painel de Controle**

1. **Faça login** na sua conta do PythonAnywhere.
2. Vá para o **Dashboard** da sua conta.

### 2. **Acessando os Arquivos de Log**

Os arquivos de log são úteis para diagnosticar problemas com seu aplicativo. No PythonAnywhere, você pode acessar os arquivos de log através do console ou do painel de controle.

#### **Acessando Logs via Console**

1. **Abra um novo console** na sua área de trabalho do PythonAnywhere (selecione "Bash" como o tipo de console).

2. **Navegue até a pasta de logs**. Geralmente, os arquivos de log são armazenados em `/var/log/`. Você pode usar o seguinte comando para navegar até o diretório:

    ```bash
    cd /var/log
    ```

3. **Listar arquivos de log**. Use o comando `ls` para listar os arquivos de log disponíveis:

    ```bash
    ls -l
    ```

4. **Visualize os arquivos de log**. Você pode usar comandos como `cat`, `less` ou `tail` para visualizar os logs. Por exemplo, para visualizar o arquivo `access.log`, você pode usar:

    ```bash
    cat comandante.pythonanywhere.com.access.log
    ```

    Ou para acompanhar as atualizações em tempo real:

    ```bash
    tail -f comandante.pythonanywhere.com.access.log
    ```

#### **Acessando Logs via Painel de Controle**

1. **Navegue até a seção de Logs** no painel de controle do PythonAnywhere. Você pode encontrar a seção de logs em "Web" > "Log Files".

2. **Selecione o tipo de log** que deseja visualizar (Access, Error ou Server).

3. **Clique no arquivo de log** para visualizá-lo diretamente no navegador. Você pode baixar os logs antigos, se necessário, clicando no link correspondente.

### 3. **Rotação de Logs**

Os arquivos de log são periodicamente rotacionados para evitar que ocupem muito espaço. Os logs antigos podem ser encontrados na pasta `/var/log` e são geralmente nomeados de forma a incluir uma data ou número de versão.
