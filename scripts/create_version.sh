#!/bin/bash

# Caminho para o arquivo setup.py
SETUP_FILE=".version"

# Verifica se o arquivo setup.py existe
if [[ ! -f "$SETUP_FILE" ]]; then
    echo "Arquivo $SETUP_FILE não encontrado!"
    exit 1
fi

# Lê a versão atual do setup.py
VERSION=$(grep -oP "(?<=version=\')[0-9]+\.[0-9]+\.[0-9]+" "$SETUP_FILE")
if [[ -z "$VERSION" ]]; then
    echo "Não foi possível encontrar a versão no $SETUP_FILE."
    exit 1
fi

# Separa a versão em major, minor e patch
IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"

# Verifica se o argumento foi passado
if [[ -z "$1" ]]; then
    echo "Uso: $0 {major|minor}"
    exit 1
fi

# Incrementa a versão com base no argumento
case $1 in
    major)
        MAJOR=$((MAJOR + 1))
        MINOR=0  # Reinicia o minor para 0
        PATCH=0  # Reinicia o patch para 0
        ;;
    minor)
        MINOR=$((MINOR + 1))
        PATCH=0  # Reinicia o patch para 0
        ;;
    *)
        echo "Argumento inválido: $1. Use 'major' ou 'minor'."
        exit 1
        ;;
esac

# Nova versão
NEW_VERSION="$MAJOR.$MINOR.$PATCH"

# Atualiza o arquivo setup.py
sed -i "s/version='$VERSION'/version='$NEW_VERSION'/" "$SETUP_FILE"

echo "Versão atualizada de $VERSION para $NEW_VERSION"

# Cria o branch no formato major.minor.x
BRANCH_NAME="$MAJOR.$MINOR.x"

# Verifica se o branch já existe
if git show-ref --quiet refs/heads/"$BRANCH_NAME"; then
    echo "Branch $BRANCH_NAME já existe."
else
    # Cria o branch
    git checkout -b "$BRANCH_NAME"
    echo "Branch $BRANCH_NAME criado."
fi

# Comita as mudanças
git add "$SETUP_FILE"
git commit -m "Preparar release $NEW_VERSION"
git push --set-upstream origin $BRANCH_NAME
git check $BRANCH_NAME
