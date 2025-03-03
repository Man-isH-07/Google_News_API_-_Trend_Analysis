from pygooglenews import GoogleNews

def get_top_news(country='IN', topic='world'):  #country, topic_type
    gn = GoogleNews(lang='en', country=country)
    top_news = gn.topic_headlines(topic)
    
    if 'entries' in top_news:
        for i, entry in enumerate(top_news['entries'][:10], start=1):
            print(f"{i}. {entry['title']}")
            print(f"   {entry['link']}\n")
    else:
        print("No news found for the given topic and country.")

def search_news(query, max_results=10): #query, input_search
    gn = GoogleNews()
    search_results = gn.search(query)
    
    if 'entries' in search_results:
        for i, entry in enumerate(search_results['entries'][:max_results], start=1):
            print(f"{i}. {entry['title']}")
            print(f"   {entry['link']}\n")
    else:
        print("No search results found.")

if __name__ == "__main__":
    # print("Fetching top news...")
    # get_top_news(country='IN', topic='business')
    
    print("\nSearching for specific news...")
    search_news("champions trophy")
