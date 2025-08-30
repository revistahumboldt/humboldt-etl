from google.cloud.bigquery import SchemaField

# Explicit definition of the ad insights table schema for BigQuery
web_page_insigths_schema = [
    
    SchemaField("id", "STRING", mode="REQUIRED", description="ID"),
    #dimensions
    SchemaField("registered_date", "DATE", mode="REQUIRED", description="Data do registro"),
    SchemaField("title", "STRING", mode="REQUIRED", description="Título do artigo"),
    SchemaField("url", "STRING", mode="REQUIRED", description="Uril da página"),
    SchemaField("location_country", "STRING", mode="REQUIRED", description="Local de visualizaçã oda página"),
    SchemaField("device", "STRING", mode="REQUIRED", description="Dispositivo de visualização da página"),
    #metrics
    SchemaField("page_impressions", "INTEGER", mode="REQUIRED", description="Impressões na página"),
    SchemaField("pages_entries", "INTEGER", mode="REQUIRED", description="Entradas realizadas pela página"),
    SchemaField("pages_exits", "INTEGER", mode="REQUIRED", description="Saídas realizadas pela página"),
    SchemaField("bounces", "INTEGER", mode="REQUIRED", description="Bounces na página"),
    SchemaField("clicks", "INTEGER", mode="REQUIRED", description="Cliques na página"),
    SchemaField("pages_duration_avg", "FLOAT", mode="REQUIRED", description="Duração da visita na página"),
    SchemaField("count_scrolldepth", "FLOAT", mode="REQUIRED", description="Total de scroll na pagina"),
    SchemaField("scrolldepth_50", "FLOAT", mode="REQUIRED", description="Percentual scrolls 50%+ na pagina"),
    SchemaField("scrolldepth_abs", "FLOAT", mode="REQUIRED", description="Scroll na pagina"),
    #timestamp for updates
    SchemaField("last_updated_timestamp", "TIMESTAMP", mode="REQUIRED", description="Last update time"),

]

    
 