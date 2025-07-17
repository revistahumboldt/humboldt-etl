# src/facebook_etl/models.py

from datetime import date, datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --------------------------------------------------------------------------------
# 1. Modelo para Insights de Anúncios Brutos do Facebook (como vêm da API)
#    - Baseado na resposta da Facebook Marketing API para AdsInsights
# --------------------------------------------------------------------------------

class Action(BaseModel):
    """Representa um item de ação dentro do campo 'actions'."""
    action_type: str
    value: float

class RawAdInsight(BaseModel):
    """
    Representa a estrutura bruta de um objeto AdsInsights retornado pela API do Facebook.
    Não todos os campos estão aqui, apenas um exemplo.
    """
    account_id: str
    campaign_name: Optional[str] = None
    adset_name: Optional[str] = None
    ad_name: Optional[str] = None
    impressions: Optional[str] = None # Vêm como string da API, precisam ser convertidos
    clicks: Optional[str] = None      # Vêm como string da API
    spend: Optional[str] = None       # Vêm como string da API
    reach: Optional[str] = None       # Vêm como string da API
    date_start: date
    date_stop: date
    actions: Optional[List[Action]] = None # Lista de objetos Action
    # Adicione outros campos conforme você extrai da API do Facebook


# --------------------------------------------------------------------------------
# 2. Modelo para Dados de Insights Transformados (Prontos para Carregamento no BigQuery)
#    - Este modelo reflete a estrutura da sua tabela no BigQuery
# --------------------------------------------------------------------------------

class TransformedAdInsight(BaseModel):
    """
    Representa a estrutura de um registro de insight de anúncio após a transformação,
    pronto para ser carregado no BigQuery.
    """
    ad_account_id: str
    campaign_name: str
    adset_name: str
    ad_name: str
    date: date # Tipo Date para BigQuery DATE
    impressions: int
    clicks: int
    spend: float
    reach: int
    leads: int = 0         # Campo adicionado na transformação
    purchases: float = 0.0 # Campo adicionado na transformação
    ctr: float
    etl_load_timestamp: datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc)) # Timestamp de carga

    # Você pode adicionar validações personalizadas ou propriedades calculadas aqui
    # @validator('spend', pre=True)
    # def convert_spend_to_float(cls, v):
    #     if isinstance(v, str):
    #         return float(v)
    #     return v

    class Config:
        """Configurações opcionais para o Pydantic."""
        orm_mode = True # Permite que modelos Pydantic sejam criados a partir de objetos arbitrários (útil para ORMs ou outros objetos)
        # allow_population_by_field_name = True # Se seus campos no JSON de entrada tiverem nomes diferentes
        # alias_generator = to_camel # Se a API usa camelCase e você quer snake_case em Python