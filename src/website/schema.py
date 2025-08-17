from google.cloud.bigquery import SchemaField

# Explicit definition of the ad insights table schema for BigQuery
web_page_insigths_schema = [
    
    SchemaField("id", "STRING", mode="REQUIRED", description="ID"),
    SchemaField("title", "STRING", mode="REQUIRED", description="Título do artigo"),
    SchemaField("url", "STRING", mode="REQUIRED", description="Uril da página"),
    SchemaField("date", "DATE", mode="REQUIRED", description="Data do registro"),
    SchemaField("location_country", "STRING", mode="REQUIRED", description="Local de visualizaçã oda página"),
    SchemaField("device", "STRING", mode="REQUIRED", description="Dispositivo de visualização da página"),
    SchemaField("page_impressions", "INTEGER", mode="REQUIRED", description="Impressões na página"),
    SchemaField("pages_entries", "INTEGER", mode="REQUIRED", description="Entradas realizadas pela página"),
    SchemaField("visits_bounces", "INTEGER", mode="REQUIRED", description="Bounces na página"),
    SchemaField("visitors", "INTEGER", mode="REQUIRED", description="Visitantes"),
    SchemaField("pages_duration_avg", "FLOAT", mode="REQUIRED", description="Duração da visita na página"),
    #timestamp for updates
    SchemaField("last_updated_timestamp", "TIMESTAMP", mode="REQUIRED", description="Last update time"),

]

    
 