#!/bin/bash

# Cloud Functions にデプロイするスクリプト
# 使用方法: bash deploy.sh

set -e

echo "🚀 Cloud Functions にデプロイを開始します..."

# プロジェクトID（環境変数から取得）
PROJECT_ID=${GCP_PROJECT_ID:-"your-project-id"}
FUNCTION_NAME="review-essay"
REGION="asia-northeast1"
RUNTIME="python311"

# デプロイコマンド
gcloud functions deploy $FUNCTION_NAME \
  --runtime $RUNTIME \
  --trigger-http \
  --allow-unauthenticated \
  --region $REGION \
  --project $PROJECT_ID \
  --entry-point review_essay \
  --source ./functions \
  --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY \
  --memory 256MB \
  --timeout 60s

echo "✅ デプロイが完了しました！"
echo "エンドポイント："
gcloud functions describe $FUNCTION_NAME --region $REGION --project $PROJECT_ID --format="value(httpsTrigger.url)"
