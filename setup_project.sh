#!/bin/bash

# Base project directory
PROJECT_ROOT="project-root"
mkdir -p "$PROJECT_ROOT"

# Create top-level files
touch "$PROJECT_ROOT/README.md" "$PROJECT_ROOT/.gitignore"

# Config directory and files
mkdir -p "$PROJECT_ROOT/config"
touch "$PROJECT_ROOT/config/config.yaml" "$PROJECT_ROOT/config/.env"

# ML Model directories and files
mkdir -p "$PROJECT_ROOT/ml_model/data/raw" "$PROJECT_ROOT/ml_model/data/processed"
mkdir -p "$PROJECT_ROOT/ml_model/notebooks" "$PROJECT_ROOT/ml_model/scripts" "$PROJECT_ROOT/ml_model/models"
touch "$PROJECT_ROOT/ml_model/requirements.txt"
touch "$PROJECT_ROOT/ml_model/scripts/train.py" "$PROJECT_ROOT/ml_model/scripts/evaluate.py"

# LLM API directories and files
mkdir -p "$PROJECT_ROOT/llm_api"
touch "$PROJECT_ROOT/llm_api/llm_integration.py" "$PROJECT_ROOT/llm_api/utils.py" "$PROJECT_ROOT/llm_api/requirements.txt"

# Backend directories and files
mkdir -p "$PROJECT_ROOT/backend/routes" "$PROJECT_ROOT/backend/models" "$PROJECT_ROOT/backend/services" "$PROJECT_ROOT/backend/utils" "$PROJECT_ROOT/backend/tests"
touch "$PROJECT_ROOT/backend/app.py"
touch "$PROJECT_ROOT/backend/routes/__init__.py" "$PROJECT_ROOT/backend/routes/crop.py" "$PROJECT_ROOT/backend/routes/llm.py"
touch "$PROJECT_ROOT/backend/requirements.txt"

# Frontend directories and files
mkdir -p "$PROJECT_ROOT/frontend/public"
mkdir -p "$PROJECT_ROOT/frontend/src/components" "$PROJECT_ROOT/frontend/src/pages" "$PROJECT_ROOT/frontend/src/services"
mkdir -p "$PROJECT_ROOT/frontend/tests"
touch "$PROJECT_ROOT/frontend/package.json"
touch "$PROJECT_ROOT/frontend/src/App.js" "$PROJECT_ROOT/frontend/src/index.js"

# Docs directory
mkdir -p "$PROJECT_ROOT/docs"

echo "Project structure created successfully in '$PROJECT_ROOT'"
