import functions_framework
import google.generativeai as genai
import os
from flask import jsonify
from flask_cors import CORS

# Gemini API キーの設定
api_key = os.environ.get('GEMINI_API_KEY')
if api_key:
    genai.configure(api_key=api_key)

@functions_framework.http
def review_essay(request):
    """小論文をGeminiで添削するエンドポイント"""
    
    # CORS対応
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return ('', 204, headers)
    
    # リクエストボディの取得
    try:
        request_json = request.get_json()
        text = request_json.get('text', '').strip()
        
        if not text:
            return jsonify({
                'error': 'テキストが空です'
            }), 400
        
        # Gemini APIを使用して添削を実行
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""以下の小論文を日本語で詳しく添削してください。

【小論文】
{text}

以下の形式で返してください：

【総評】
（全体的な評価）

【改善点】
1. （改善点1）
2. （改善点2）
3. （改善点3）

【良い点】
✓ （良い点1）
✓ （良い点2）
✓ （良い点3）

【スコア】
・論理性: X/10
・表現力: X/10
・論拠の提示: X/10
・構成: X/10
───────────────
総合スコア: X.X/10
"""
        
        response = model.generate_content(prompt)
        review_text = response.text
        
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'application/json'
        }
        
        return (jsonify({
            'review': review_text
        }), 200, headers)
    
    except ValueError as e:
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        }
        return (jsonify({
            'error': f'リクエスト形式エラー: {str(e)}'
        }), 400, headers)
    
    except Exception as e:
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        }
        return (jsonify({
            'error': f'添削処理に失敗しました: {str(e)}'
        }), 500, headers)
