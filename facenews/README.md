# NEWS experience composed using FaceVerse

## Outline 

1. Prompt of what we want: Let us build a web app for "news" that is powered by NewsAPI 

2. Define the main component: News Component

- One component with 2 methods:
 - hello: ping method
 - getNews: gets the news with scope parameters (ex: language, country, domain)

3. Identify the parts that we want

- Web Experience for users to consume news
- Backend parts that provides list of news
- Ancillary parts: Deployment, Management, Monitoring

4. What does the List and NewsItem get mapped to?

Objects:
 - L:st
 - NewsItem

 a) User chooses to mape NewsItem to Card

Mapping:
   DataModel: list[NewsItem]
   UIModel: List
   Parameters:
    ViewMode: [Grid, List]
    Filters: Sort( key="NewsItem.publishedAt", order: [newest, oldest])

 Mapping:
   DataModel: NewsItem
   UIModel: Card
   Mapping-of-fields:
    CardTitle: NewsItem.title
    Card: NewsItem.title

  description: string;
  author: string;
  publishedAt: string;
  url: string;
  urlToImage: string;
    