from google.cloud.bigquery import SchemaField

# Explicit definition of the ad insights table schema for BigQuery
instagram_page_schema = [
    
    SchemaField("id", "STRING", mode="REQUIRED", description="ID único"),
    SchemaField("date", "DATE", mode="REQUIRED", description="Data do registro"),
    # metrics
    SchemaField("follow_count", "INTEGER", mode="REQUIRED", description="Total de novos seguidores"),
    SchemaField("profile_views", "INTEGER", mode="REQUIRED", description="Total de views no perfil"),
    SchemaField("website_clicks", "INTEGER", mode="REQUIRED", description="Total de cliques no perfil"),
    #id do perfil ig
    SchemaField("page_id", "STRING", mode="REQUIRED", description="ID do perfil"),
    #timestamp for updates
    SchemaField("last_updated_timestamp", "TIMESTAMP", mode="REQUIRED", description="Last update time"),

]

    
 