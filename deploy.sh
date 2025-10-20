#!/bin/bash
# Carga variables de entorno
source .aws

echo "Variables cargadas para la cuenta $CDK_DEFAULT_ACCOUNT en región $CDK_DEFAULT_REGION"

echo "Iniciando bootstrap de CDK..."
cdk bootstrap

echo "Desplegando todos los stacks..."
cdk deploy --all

echo "Despliegue completado!"
