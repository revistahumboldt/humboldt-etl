from google.cloud.bigquery import SchemaField

# Explicit definition of the ad insights table schema for BigQuery
facebook_posts_schema = [
    
    SchemaField("id", "STRING", mode="REQUIRED", description="ID único do post "),
    SchemaField("id_page", "STRING", mode="REQUIRED", description="ID da página facebook"),
    SchemaField("created_time", "DATETIME", mode="REQUIRED", description="Data do post"),
    SchemaField("post_impressions_paid", "INTEGER", mode="REQUIRED", description="Total de impressoes pagas no post"),
    SchemaField("post_impressions_paid_unique", "INTEGER", mode="REQUIRED", description="Total de impressoes pagas únicas no post"),
    SchemaField("post_impressions_organic", "INTEGER", mode="REQUIRED", description="Total de impressoes ôrganicas no post"),
    SchemaField("post_impressions_organic_unique", "INTEGER", mode="REQUIRED", description="Total de impressoes ôrganicas únicas no post"),

    # action metrics 
    SchemaField("likes", "INTEGER", mode="REQUIRED", description="Número de curtidas no post"),
    SchemaField("shares", "INTEGER", mode="REQUIRED", description="Número de compartilhamentos no post"),
    SchemaField("comments", "INTEGER", mode="REQUIRED", description="Número de comentários no post"),
    SchemaField("others_clicks", "INTEGER", mode="REQUIRED", description="Número de cliques em outros lugares fora link e foto, no post"),
    SchemaField("photo_clicks", "INTEGER", mode="REQUIRED", description="Número de cliques em fotos, no post"),
    SchemaField("link_clicks", "INTEGER", mode="REQUIRED", description="Número de cliques em links no post"),

    #timestamp for updates
    SchemaField("last_updated_timestamp", "TIMESTAMP", mode="REQUIRED", description="Last update time"),

]


