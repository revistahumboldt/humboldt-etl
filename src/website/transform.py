import hashlib
from website.models import WebPageInsightModel
from datetime import datetime

def transform_website_data(web_raw_data: list[list]) -> list[WebPageInsightModel]:
    transformed_insights = []

    for row in web_raw_data:
        try:
            # Validate and convert date
            parsed_date = datetime.strptime(row[0], "%Y%m%d").date()
        except ValueError:
            # If it's not a valid date, skip the line
            print(f"Skipped line (invalid date): {row}")
            continue

        # Generate unique URL hash
        url_hash = hashlib.md5(row[1].encode("utf-8")).hexdigest()

        transformed_insight = WebPageInsightModel(
            id=url_hash,
            registered_date=parsed_date,
            title=row[1],
            url=row[2],
            location_country=row[3],
            device=row[4],
            page_impressions=row[5],
            pages_entries=row[6],
            pages_exits=row[7],
            bounces=row[8],
            clicks=row[9],
            pages_duration_avg=float(row[10]),
            count_scrolldepth=float(row[11]),
            scrolldepth_50=float(row[12]),
            scrolldepth_abs=float(row[13]),
            last_updated_timestamp=datetime.now()
        )
        
        transformed_insights.append(transformed_insight)

    return transformed_insights
