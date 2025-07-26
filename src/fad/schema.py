from google.cloud.bigquery import SchemaField

# Explicit definition of the ad insights table schema for BigQuery
ad_insights_schema = [
    
    SchemaField("id", "STRING", mode="REQUIRED", description="ID único do insight (geralmente ad_id + data)"),
    SchemaField("ad_id", "STRING", mode="REQUIRED", description="ID do anúncio"),
    SchemaField("date_start", "DATE", mode="REQUIRED", description="Data de início do insight"),
    SchemaField("date_stop", "DATE", mode="REQUIRED", description="Data de término do insight"),
    SchemaField("ad_name", "STRING", mode="REQUIRED", description="Nome do anúncio"),
    SchemaField("adset_name", "STRING", mode="REQUIRED", description="Nome do conjunto de anúncios"),
    SchemaField("campaign_name", "STRING", mode="REQUIRED", description="Nome da campanha"),
    SchemaField("objective", "STRING", mode="REQUIRED", description="Objetivo da campanha (ex: LINK_CLICKS)"),
    SchemaField("optimization_goal", "STRING", mode="REQUIRED", description="Meta de otimização (ex: LANDING_PAGE_VIEWS)"),
    SchemaField("spend", "FLOAT", mode="REQUIRED", description="Gasto total em moeda local"),
    SchemaField("frequency", "FLOAT", mode="REQUIRED", description="Frequência média do anúncio"),
    SchemaField("reach", "INTEGER", mode="REQUIRED", description="Número de pessoas alcançadas"),
    SchemaField("impressions", "INTEGER", mode="REQUIRED", description="Número de impressões do anúncio"),

    # can be null 
    SchemaField("age", "STRING", mode="NULLABLE", description="Faixa etária do público (ex: 25-34)"),
    SchemaField("gender", "STRING", mode="NULLABLE", description="Gênero do público (male, female, unknown)"),

    # action metrics 
    SchemaField("link_clicks", "INTEGER", mode="REQUIRED", description="Número de cliques em links"),
    SchemaField("post_reactions", "INTEGER", mode="REQUIRED", description="Número de reações (curtidas, amores, etc.)"),
    SchemaField("pageview_br", "INTEGER", mode="REQUIRED", description="Número de pageviews Brasil"),
    SchemaField("pageview_latam", "INTEGER", mode="REQUIRED", description="Número de pageviews LatAm"),
    SchemaField("comments", "INTEGER", mode="REQUIRED", description="Número de comentários"),
    SchemaField("page_engagement", "INTEGER", mode="REQUIRED", description="Engajamento com a página"),
    SchemaField("post_engagement", "INTEGER", mode="REQUIRED", description="Engajamento com a publicação"),
    SchemaField("shares", "INTEGER", mode="REQUIRED", description="Número de compartilhamentos"),
    SchemaField("video_views", "INTEGER", mode="REQUIRED", description="Número de visualizações de vídeo"),
    
    #timestamp for updates
    SchemaField("last_updated_timestamp", "TIMESTAMP", mode="REQUIRED", description="Last update time"),

]