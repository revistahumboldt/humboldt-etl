from facebook_business.adobjects.page import Page
from init_fb_api import _initialize_facebook_api
from facebook_business.exceptions import FacebookRequestError 

def find_page(page_id: str, fb_app_id: str, app_secret: str, access_token: str):
    try:
        _initialize_facebook_api(fb_app_id, app_secret, access_token)
    except Exception as e:
        print(f"Erro ao inicializar a API: {e}")
        return

    try:
        page = Page(page_id)
        fields_to_get = ['instagram_business_account']
        
        page_data = page.api_get(fields=fields_to_get)

        # O linter pode reclamar, mas este é o padrão correto.
        # Adicione o comentário 'type: ignore' para suprimir o aviso do Pylance.
        instagram_account_info = page_data.get('instagram_business_account') # type: ignore
        
        if instagram_account_info:
            instagram_user_id = instagram_account_info.get('id')
            print(f"ID do Instagram User: {instagram_user_id}\n")
            return instagram_user_id
        else:
            print("Nenhuma conta do Instagram business encontrada para esta página.")
            return None

    except FacebookRequestError as e:
        print(f"Erro da API do Facebook: {e.api_error_message}")
        return None
    except Exception as e:
        print(f"Erro ao processar a página: {e}")
        return None