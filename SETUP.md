# 小論文添削システム - セットアップガイド

## 🚀 クイックスタート

### 1. GitHub Secrets の設定

リポジトリの Settings → Secrets and variables → Actions で以下を追加：

```
GCP_PROJECT_ID       : your-google-cloud-project-id
GCP_SA_KEY          : Google Cloud Service Account の JSON キー（Base64エンコード）
GEMINI_API_KEY      : Google Gemini API キー
```

#### GCP Service Account キーの取得と Base64 エンコード

```bash
# GCP Console で service account を作成
# キーをダウンロードして以下を実行
cat path/to/service-account-key.json | base64 | tr -d '\n' | pbcopy
```

### 2. GitHub Actions でデプロイ

`main` ブランチに `functions/` ディレクトリの変更をプッシュすると自動的にデプロイされます。

```bash
git add functions/
git commit -m "Deploy Cloud Functions"
git push origin main
```

### 3. デプロイされたエンドポイント URL の取得

GitHub Actions の実行ログから、または以下コマンドで確認：

```bash
gcloud functions describe review-essay \
  --region asia-northeast1 \
  --format="value(httpsTrigger.url)"
```

### 4. index.html を更新

`index.html` の `CLOUD_FUNCTION_URL` を実際のエンドポイント URL に置き換えます：

```javascript
const CLOUD_FUNCTION_URL = 'https://asia-northeast1-YOUR_PROJECT_ID.cloudfunctions.net/review-essay';
```

---

## 📋 必要な準備

### Google Cloud の設定

1. **Google Cloud プロジェクトを作成**
   - [Google Cloud Console](https://console.cloud.google.com)

2. **Gemini API を有効化**
   - APIs & Services → Library
   - "Generative Language API" を検索して有効化

3. **Service Account を作成**
   - APIs & Services → Credentials
   - "Create Credentials" → "Service Account"
   - キーを JSON 形式でダウンロード

4. **IAM ロールを付与**
   - Service Account に以下のロールを付与：
     - Cloud Functions Admin
     - Service Account User

---

## 🔧 ローカルテスト

### 環境構築

```bash
# Python 仮想環境の作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存パッケージのインストール
pip install -r functions/requirements.txt
pip install flask

# 環境変数の設定
export GEMINI_API_KEY="your-api-key"
```

### ローカルサーバーの起動

```bash
functions-framework --target review_essay --debug
```

アクセス: `http://localhost:8080`

### テストリクエスト

```bash
curl -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"text": "あなたの小論文テキスト"}'
```

---

## 📝 プロンプトのカスタマイズ

`functions/main.py` の `prompt` 変数を編集して、添削のスタイルを変更できます。

例：より厳しい添削にする
```python
prompt = f"""以下の小論文を厳しく添削してください。特に論理的矛盾や不明確な表現を指摘してください。

【小論文】
{text}
...
```

---

## 🐛 トラブルシューティング

### デプロイが失敗する
- `GCP_SA_KEY` が正しく Base64 エンコードされているか確認
- Service Account に適切な IAM ロールがあるか確認

### API が 500 エラーを返す
- Gemini API キーが正しいか確認
- API が有効化されているか確認
- Cloud Functions のログを確認：
  ```bash
  gcloud functions logs read review-essay --region asia-northeast1
  ```

### CORS エラーが出る
- 本番環境では CORS ヘッダーが正しく設定されている
- ブラウザのデベロッパーツールでネットワークタブを確認

---

## 📊 料金見積もり

- **Google Cloud Functions**: 月 200 万呼び出しまで無料
- **Gemini API**: 無料利用枠あり（詳細は [Google AI Studio](https://ai.google.dev/) で確認）

---

## 🔐 セキュリティ考慮事項

- このエンドポイントは `allow-unauthenticated` で設定されています
- 本番環境では認証の追加を検討してください
- レート制限の実装を推奨します

