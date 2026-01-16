"""
Azure Functions - 計算API（掛け算・割り算）
"""
import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# 定数
MAX_DIGITS = 9
MAX_VALUE = 999_999_999


def validate_input(a_str: str | None, b_str: str | None) -> tuple[int, int] | str:
    """
    入力パラメータのバリデーションを行う。
    
    Returns:
        tuple[int, int]: 正常時は (A, B) のタプル
        str: エラー時はエラーメッセージ
    """
    # パラメータ未指定チェック
    if a_str is None or a_str == "":
        return "エラー: パラメータAが未指定です"
    if b_str is None or b_str == "":
        return "エラー: パラメータBが未指定です"
    
    # 整数チェック
    try:
        a = int(a_str)
    except ValueError:
        return "エラー: パラメータAは整数である必要があります"
    
    try:
        b = int(b_str)
    except ValueError:
        return "エラー: パラメータBは整数である必要があります"
    
    # 負の数チェック
    if a < 0:
        return "エラー: パラメータAは0以上である必要があります"
    if b < 0:
        return "エラー: パラメータBは0以上である必要があります"
    
    # 9桁超過チェック
    if a > MAX_VALUE:
        return "エラー: パラメータAは9桁以内である必要があります"
    if b > MAX_VALUE:
        return "エラー: パラメータBは9桁以内である必要があります"
    
    return (a, b)


@app.route(route="multiply", methods=["GET"])
def multiply(req: func.HttpRequest) -> func.HttpResponse:
    """
    掛け算API: A × B の計算結果を返す
    
    入力: クエリストリング A, B（0以上の整数、9桁以内）
    出力: 計算結果（数値のみ）
    """
    a_str = req.params.get("A")
    b_str = req.params.get("B")
    
    # バリデーション
    result = validate_input(a_str, b_str)
    if isinstance(result, str):
        return func.HttpResponse(result, status_code=200, mimetype="text/plain")
    
    a, b = result
    
    # 計算
    product = a * b
    
    # 結果が9桁超過チェック
    if product > MAX_VALUE:
        return func.HttpResponse(
            "エラー: 計算結果が9桁を超えています",
            status_code=200,
            mimetype="text/plain"
        )
    
    return func.HttpResponse(str(product), status_code=200, mimetype="text/plain")


@app.route(route="divide", methods=["GET"])
def divide(req: func.HttpRequest) -> func.HttpResponse:
    """
    割り算API: A ÷ B の商と余りを返す
    
    入力: クエリストリング A, B（0以上の整数、9桁以内）
    出力: 「商: X, 余り: Y」形式
    """
    a_str = req.params.get("A")
    b_str = req.params.get("B")
    
    # バリデーション
    result = validate_input(a_str, b_str)
    if isinstance(result, str):
        return func.HttpResponse(result, status_code=200, mimetype="text/plain")
    
    a, b = result
    
    # ゼロ除算チェック
    if b == 0:
        return func.HttpResponse(
            "エラー: 0で割ることはできません",
            status_code=200,
            mimetype="text/plain"
        )
    
    # 計算
    quotient = a // b
    remainder = a % b
    
    return func.HttpResponse(
        f"商: {quotient}, 余り: {remainder}",
        status_code=200,
        mimetype="text/plain"
    )
