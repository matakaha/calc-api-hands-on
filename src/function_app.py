import azure.functions as func

app = func.FunctionApp()


def _text_response(message: str) -> func.HttpResponse:
    return func.HttpResponse(message, status_code=200, mimetype="text/plain")


def _validate_param(req: func.HttpRequest, name: str):
    raw = req.params.get(name)
    if raw is None:
        return None, f"{name}が指定されていません"
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return None, f"{name}が不正です"
    if value < 0:
        return None, f"{name}が不正です"
    return value, None


@app.function_name(name="multiply")
@app.route(route="multiply", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def multiply(req: func.HttpRequest) -> func.HttpResponse:
    a, err = _validate_param(req, "A")
    if err:
        return _text_response(err)
    b, err = _validate_param(req, "B")
    if err:
        return _text_response(err)

    result = a * b
    return _text_response(str(result))


@app.function_name(name="divide")
@app.route(route="divide", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def divide(req: func.HttpRequest) -> func.HttpResponse:
    a, err = _validate_param(req, "A")
    if err:
        return _text_response(err)
    b, err = _validate_param(req, "B")
    if err:
        return _text_response(err)
    if b == 0:
        return _text_response("Bは0にできません")

    result = a // b
    return _text_response(str(result))
