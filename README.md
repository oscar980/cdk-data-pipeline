# CDK Data Pipeline

Pipeline de datos completo usando AWS CDK con Lambda, Glue, Athena y Lake Formation.

## 🏗️ Arquitectura

```
Lambda (Ingesta) → S3 → Glue Crawler → Glue Database → Athena
```

### Componentes:
- **StorageStack**: Buckets S3 para datos y resultados
- **IngestionStack**: Lambda para ingesta de datos desde APIs
- **GlueStack**: Base de datos y crawler para detección de esquemas
- **AthenaStack**: WorkGroup para consultas SQL

## 🚀 Despliegue

### Prerequisitos:
- AWS CLI configurado
- CDK instalado (`npm install -g aws-cdk`)
- Python 3.9+
- Credenciales AWS válidas

### Pasos:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/oscar980/cdk-data-pipeline.git
   cd cdk-data-pipeline
   ```

2. **Instalar dependencias:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno:**
   ```bash
   cp .aws.example .aws
   # Editar .aws con tus credenciales
   ```

4. **Desplegar:**
   ```bash
   ./deploy.sh
   ```

## 🔧 Configuración de Lake Formation

**IMPORTANTE**: Después del despliegue, necesitas otorgar permisos de Lake Formation:

```bash
# 1. Permisos al rol de Glue para la base de datos
aws lakeformation grant-permissions --cli-input-json file://grant_permissions.json --region us-east-1

# 2. Permisos al rol de Glue para S3
aws lakeformation grant-permissions --cli-input-json file://grant_s3_permissions.json --region us-east-1

# 3. Permisos al root para la base de datos
aws lakeformation grant-permissions --cli-input-json file://grant_root_permissions.json --region us-east-1

# 4. Permisos al root para S3
aws lakeformation grant-permissions --cli-input-json file://grant_root_s3_permissions.json --region us-east-1

# 5. Permisos al root para la tabla
aws lakeformation grant-permissions --cli-input-json file://grant_root_table_permissions.json --region us-east-1
```

## 📊 Uso

### 1. Ejecutar Lambda de ingesta:
```bash
aws lambda invoke \
  --function-name IngestionStack-IngestionLambdaEF25F265 \
  --payload '{"api_url": "https://jsonplaceholder.typicode.com/users"}' \
  response.json \
  --region us-east-1
```

### 2. Ejecutar Glue Crawler:
```bash
aws glue start-crawler --name cdk_data_pipeline_crawler --region us-east-1
```

### 3. Consultar en Athena:
```sql
SELECT * FROM cdk_data_pipeline_db_users.users LIMIT 5;
```

## 🧪 Testing

```bash
python -m pytest tests/unit/ -v
```

## 📁 Estructura del Proyecto

```
cdk-data-pipeline/
├── cdk_data_pipeline/
│   ├── storage_stack.py      # Buckets S3
│   ├── ingestion_stack.py    # Lambda de ingesta
│   ├── glue_stack.py         # Glue Database y Crawler
│   ├── athena_stack.py       # Athena WorkGroup
│   └── lambda_src/
│       └── data_ingestion.py  # Código Lambda
├── tests/
│   └── unit/
│       └── test_cdk_data_pipeline_stack.py
├── app.py                    # Aplicación principal CDK
├── deploy.sh                 # Script de despliegue
├── grant_*.json              # Archivos de permisos Lake Formation
└── requirements.txt          # Dependencias Python
```

## 🔧 Configuración

### Variables de entorno (.aws):
```bash
export CDK_DEFAULT_ACCOUNT="your-account-id"
export CDK_DEFAULT_REGION="us-east-1"
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
```

## 🏷️ Recursos Creados

- **S3 Buckets**: 
  - `cdk-data-bucket-oscar` (datos)
  - `cdk-athena-results-oscar` (resultados)
- **Lambda**: `IngestionStack-IngestionLambdaEF25F265`
- **Glue Database**: `cdk_data_pipeline_db_users`
- **Glue Crawler**: `cdk_data_pipeline_crawler`
- **Athena WorkGroup**: `cdk_data_pipeline_wg_users`

## 🧹 Limpieza

```bash
cdk destroy --all
```

## 📝 Notas

- **Lake Formation**: Se activa automáticamente con Glue
- **Permisos**: Requieren configuración manual inicial usando los archivos `grant_*.json`
- **Formato de datos**: JSONL (JSON Lines) para mejor compatibilidad
- **Esquema**: Detectado automáticamente por el crawler

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request