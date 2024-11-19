#!/bin/bash

source .env

# Verifica se a variável de ambiente NEO4J_HOME está definida
if [ -z "$NEO4J_HOME" ]; then
    echo "Erro: A variável de ambiente NEO4J_HOME não está definida."
    exit 1
fi

# Verifica se o Neo4j já está em execução
if pgrep -f "$NEO4J_HOME" > /dev/null; then
    echo "Neo4j já está em execução."
    # Encerra o Neo4j
    "$NEO4J_HOME/bin/neo4j" stop
else
    echo "Iniciando o Neo4j..."
    # Inicia o Neo4j em segundo plano
    "$NEO4J_HOME/bin/neo4j" start
    echo "Neo4j iniciado."
fi
