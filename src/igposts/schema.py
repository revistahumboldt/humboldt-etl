from google.cloud.bigquery import SchemaField

# Explicit definition of the ad insights table schema for BigQuery
instagram_posts_schema = [
    
    SchemaField("id", "STRING", mode="REQUIRED", description="ID"),
    SchemaField("timestamp", "DATE", mode="REQUIRED", description="Data do registro"),
    SchemaField("link", "STRING", mode="REQUIRED", description="Link do post"),
    SchemaField("media_product_type", "STRING", mode="REQUIRED", description="Posicionamento"),
    SchemaField("media_type", "STRING", mode="REQUIRED", description="Formato"),
    SchemaField("likes", "INTEGER", mode="REQUIRED", description="Likes"),
    SchemaField("comments", "INTEGER", mode="REQUIRED", description="Comentários"),
    SchemaField("saves", "INTEGER", mode="REQUIRED", description="Salvamentos"),
    SchemaField("reach", "INTEGER", mode="REQUIRED", description="Alcance"),
    SchemaField("impressions", "INTEGER", mode="REQUIRED", description="Impressoes"),
    SchemaField("video_views", "INTEGER", mode="REQUIRED", description="Views de videos"),
    SchemaField("caption", "STRING", mode="REQUIRED", description="Texto do post"),
    SchemaField("username", "INTEGER", mode="REQUIRED", description="ID da página do Instagram"),
    #timestamp for updates
    SchemaField("last_updated_timestamp", "TIMESTAMP", mode="REQUIRED", description="Last update time"),

]

    
 