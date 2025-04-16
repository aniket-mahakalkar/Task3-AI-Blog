from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

def get_keywords_from_google_ads(client, customer_id, keyword_text):
    keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")

    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = customer_id
    request.keyword_seed.keywords.append(keyword_text)
    request.language = "languageConstants/1000"  # English
    request.geo_target_constants.append("geoTargetConstants/2840")  # US

    response = keyword_plan_idea_service.generate_keyword_ideas(request=request)

    keywords = []
    for idea in response.results[:5]:
        keywords.append({
            "keyword": idea.text,
            "search_volume": idea.keyword_idea_metrics.avg_monthly_searches,
            "competition": idea.keyword_idea_metrics.competition.name,
        })
    return keywords

if __name__ == "__main__":
    # Load the Google Ads client from YAML
    client = GoogleAdsClient.load_from_storage("google-ads.yaml")

    # Replace with your real Google Ads customer ID
    customer_id = "your id"

    # Keyword input
    keyword_input = "Echo Dot 5th Gen"

    # Run the function
    results = get_keywords_from_google_ads(client, customer_id, keyword_input)

    print("Keyword Ideas:")
    for r in results:
        print(f"{r['keyword']} | Volume: {r['search_volume']} | Competition: {r['competition']}")
