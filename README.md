# calc-api-hands-on

Azure Functions で実装した計算APIのハンズオンプロジェクト

## 概要

このプロジェクトは、Azure Functions (Python) を使用した簡単な計算APIを提供します。

### 提供API

- `/api/multiply` - 掛け算API (A × B)
- `/api/divide` - 割り算API (A ÷ B、小数点以下切り捨て)

## 前提条件

- Python 3.11以上
- pip

## セットアップ

### 依存関係のインストール

```bash
# 本番用依存関係
pip install -r src/requirements.txt

# 開発用依存関係（テスト実行に必要）
pip install -r requirements-dev.txt
```

## テスト

### テスト実行

プロジェクトルートで以下のコマンドを実行します：

```bash
# すべてのテストを実行
pytest tests/

# 詳細表示付きで実行
pytest tests/ -v

# カバレッジレポート付きで実行
pytest tests/ --cov=src --cov-report=term-missing

# カバレッジレポートをHTMLで生成
pytest tests/ --cov=src --cov-report=html
```

### テスト構成

- `tests/test_function_app.py` - function_app.py の単体テスト
  - `_text_response()` - レスポンス生成関数のテスト
  - `_validate_param()` - パラメータ検証関数のテスト
  - `multiply()` - 掛け算エンドポイントのテスト
  - `divide()` - 割り算エンドポイントのテスト

### カバレッジ

現在のテストカバレッジ: **100%**

## APIの仕様

詳細な仕様は以下のドキュメントを参照してください：

- [機能要件](docs/functional_requirements.md)
- [非機能要件](docs/non_functional_requirements.md)

### 使用例

```
# 掛け算: 2 × 3 = 6
GET {baseUrl}/api/multiply?A=2&B=3
=> 6

# 割り算: 10 ÷ 3 = 3 (小数点以下切り捨て)
GET {baseUrl}/api/divide?A=10&B=3
=> 3

# エラー例: Bが0
GET {baseUrl}/api/divide?A=5&B=0
=> Bは0にできません
```

## ライセンス

MIT License
