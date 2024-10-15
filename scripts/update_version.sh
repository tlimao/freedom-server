#!/bin/bash

# Caminho para o arquivo setup.py
SETUP_FILE="setup.py"

# Função para incrementar a versão
increment_version() {
    version=$1
    part=$2

    # Divide a versão nos componentes major, minor e patch
    IFS='.' read -r major minor patch <<< "$version"

    # Incrementa a parte específica da versão com base na opção fornecida
    case $part in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
        *)
            echo "Parte da versão desconhecida: $part. Use 'major', 'minor' ou 'patch'."
            exit 1
            ;;
    esac

    # Retorna a nova versão
    echo "$major.$minor.$patch"
}

# Obtém a versão atual do setup.py (assume que a linha da versão tem o formato: version='x.y.z')
current_version=$(grep -Po "(?<=version=')[0-9]+\.[0-9]+\.[0-9]+(?=')" $SETUP_FILE)

if [ -z "$current_version" ]; then
    echo "Erro: Não foi possível encontrar a versão no arquivo $SETUP_FILE"
    exit 1
fi

# Mostra a versão atual
echo "Versão atual: $current_version"

# Determina qual parte da versão incrementar
increment_type=$1
if [ -z "$increment_type" ]; then
    increment_type="patch"  # Padrão: incrementa o patch
fi

# Incrementa a versão
new_version=$(increment_version "$current_version" "$increment_type")

# Atualiza o arquivo setup.py com a nova versão
sed -i "s/version='$current_version'/version='$new_version'/g" $SETUP_FILE

# Mostra a nova versão
echo "Nova versão: $new_version"

# Extrai major e minor da nova versão para criar a branch major.minor.x
IFS='.' read -r new_major new_minor new_patch <<< "$new_version"
branch_name="$new_major.$new_minor.x"

# Verifica se a branch já existe
branch_exists=$(git branch --list "$branch_name")

if [ -z "$branch_exists" ]; then
    # Se a branch não existir, cria e muda para ela
    echo "Criando nova branch: $branch_name"
    git checkout -b "$branch_name"
else
    # Se a branch já existir, muda para ela
    echo "Branch $branch_name já existe. Mudando para a branch."
    git checkout "$branch_name"
fi

# Faz o commit automático com Git
git add $SETUP_FILE
git commit -m "Atualiza versão: $current_version -> $new_version"

# Faz o push para a branch
git push --set-upstream origin "$branch_name"

echo "Commit realizado e enviado para a branch $branch_name no repositório."
