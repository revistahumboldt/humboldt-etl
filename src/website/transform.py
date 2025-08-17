import hashlib
from website.models import WebPageInsightModel
from datetime import datetime

def transform_website_data(web_raw_data: list[list]) -> list[WebPageInsightModel]:
    transformed_insights = []

    for row in web_raw_data:
        try:
            # Validar e converter data
            parsed_date = datetime.strptime(row[2], "%Y%m%d").date()
        except ValueError:
            # Se não for uma data válida, pula a linha
            print(f"Skipped line (invalid date): {row}")
            continue

        # Gerar hash único da URL
        url_hash = hashlib.md5(row[1].encode("utf-8")).hexdigest()

        transformed_insight = WebPageInsightModel(
            id=url_hash,
            title=row[0],
            url=row[1],
            date=parsed_date,
            location_country=row[3],
            device=row[4],
            page_impressions=row[5],
            pages_entries=row[6],
            visits_bounces=row[7],
            visitors=row[8],
            pages_duration_avg=float(row[9]),
            last_updated_timestamp=datetime.now()
        )
        
        transformed_insights.append(transformed_insight)

    return transformed_insights
