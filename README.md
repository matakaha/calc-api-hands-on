# 計算 API (Calc API)

Azure Functions で動作する計算 API プロジェクトです。ブラウザから URL にアクセスするだけで、掛け算・割り算の計算結果を取得できます。

---

## 概要

本プロジェクトは、HTTP リクエストで数値計算を行う 2 つの API を提供します。

| API | エンドポイント | 機能 |
|-----|---------------|------|
| 掛け算 API | `/multiply?A={値}&B={値}` | A × B の計算結果を返す |
| 割り算 API | `/divide?A={値}&B={値}` | A ÷ B の商と余りを返す |

---

## 技術スタック

| 項目 | 技術 |
|------|------|
| クラウド | Microsoft Azure（東日本リージョン） |
| コンピューティング | Azure Functions (Flex Consumption Plan) |
| 開発言語 | Python 3.11 |
| 認証 | 匿名アクセス（認証不要） |

---

## 使用例

### 掛け算 API

```
GET https://<your-function-app>.azurewebsites.net/multiply?A=12&B=34
```

**レスポンス**:
```
408
```

### 割り算 API

```
GET https://<your-function-app>.azurewebsites.net/divide?A=100&B=7
```

**レスポンス**:
```
商: 14, 余り: 2
```

---

## 入力仕様（概要）

- パラメータ `A` と `B` をクエリストリングで指定
- 0以上の整数（非負整数）のみ有効
- 9桁以内（0 ～ 999,999,999）
- 計算結果も9桁以内であること

エラー時は日本語のエラーメッセージがプレーンテキストで返却されます。

---

## フォルダ構成

```
calc-api-hands-on/
├── README.md                 # 本ファイル
├── docs/
│   ├── requirements.md       # 機能要件
│   └── non-functional-requirements.md  # 非機能要件
├── src/                      # ソースコード（実装予定）
└── tests/                    # テストコード（実装予定）
```

---

## 詳細ドキュメント

詳細な仕様については以下のドキュメントを参照してください。

- [機能要件](docs/requirements.md) - API仕様、入出力形式、エラー仕様
- [非機能要件](docs/non-functional-requirements.md) - インフラ構成、セキュリティ、パフォーマンス要件
