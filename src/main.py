# main.py

def hello_http(request):
    """
    HTTP Cloud Function que retorna "Hello World!".

    Args:
        request (flask.Request): O objeto da requisição HTTP.
                                 Para este exemplo simples, não vamos usá-lo.
    Returns:
        str: Uma string "Hello World!".
    """
    return 'Hello World from Cloud Run Function!'