#!/bin/bash

# Caminhos dos arquivos
VERSION_FILE=".version"
CONFIG_FILE="config/server.local.yml"

# Verifica se o arquivo .version existe
if [[ ! -f "$VERSION_FILE" ]]; then
  echo "Erro: Arquivo .version não encontrado!"
  exit 1
fi

# Extrai a versão do arquivo .version
VERSION=$(grep "^version=" "$VERSION_FILE" | cut -d'=' -f2)

# Verifica se a versão foi lida com sucesso
if [[ -z "$VERSION" ]]; then
  echo "Erro: Não foi possível ler a versão do arquivo .version!"
  exit 1
fi

# Verifica se o arquivo de configuração existe
if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "Erro: Arquivo de configuração $CONFIG_FILE não encontrado!"
  exit 1
fi

# Substitui a versão no arquivo YAML
sed -i.bak "s/version: .*/version: ${VERSION}/" "$CONFIG_FILE"

# Mensagem de sucesso
echo "Versão atualizada para $VERSION em $CONFIG_FILE"

python -m aiohttp.web -H 0.0.0.0 -P 8080 freedomserver.server_run:run -c config/server.local.yml