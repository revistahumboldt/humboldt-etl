from google.cloud.bigquery import SchemaField

# Explicit definition of the ad insights table schema for BigQuery
instagram_posts_schema = [
    
    SchemaField("id", "STRING", mode="REQUIRED", description="ID"),
    SchemaField("date", "DATE", mode="REQUIRED", description="Data do registro"),
    SchemaField("link", "STRING", mode="REQUIRED", description="Link do post"),
    SchemaField("media_product_type", "STRING", mode="REQUIRED", description="Posicionamento"),
    SchemaField("media_type", "STRING", mode="REQUIRED", description="Formato"),
    #metrics
    SchemaField("likes", "INTEGER", mode="REQUIRED", description="Likes"),
    SchemaField("comments", "INTEGER", mode="REQUIRED", description="Comentários"),
    SchemaField("saves", "INTEGER", mode="REQUIRED", description="Salvamentos"),
    SchemaField("shares", "INTEGER", mode="REQUIRED", description="Compartilhamentos"),
    SchemaField("views", "INTEGER", mode="REQUIRED", description="Visualizações únicas do post"),
    SchemaField("impressions", "INTEGER", mode="REQUIRED", description="Impressões do post"),
    SchemaField("reach", "INTEGER", mode="REQUIRED", description="Alcance do post"),
    SchemaField("profile_activity", "INTEGER", mode="NULLABLE", description="Atividade no perfil (cliques no perfil)"),
    SchemaField("total_interactions", "INTEGER", mode="NULLABLE", description="Total de interações (likes, comentários, compartilhamentos e salvamentos)"),
    SchemaField("ig_reels_avg_watch_time", "INTEGER", mode="NULLABLE", description="A quantidade média de tempo gasto no reels."),
    SchemaField("ig_reels_video_view_total_time", "INTEGER", mode="NULLABLE", description="A quantidade total de tempo gasto no reels."),

    #video metrics
    SchemaField("caption", "STRING", mode="REQUIRED", description="Texto do post"),
    SchemaField("username", "STRING", mode="REQUIRED", description="Nome da página do Instagram"),
    SchemaField("page_id", "STRING", mode="REQUIRED", description="ID da página do Instagram"),
    #timestamp for updates
    SchemaField("last_updated_timestamp", "TIMESTAMP", mode="REQUIRED", description="Last update time"),

]

    
 