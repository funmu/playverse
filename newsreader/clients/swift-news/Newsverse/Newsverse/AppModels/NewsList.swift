//
//  NewsList.swift
//  Newsverse
//
//  manages the news list for a given source and type
//
//  Created by Murali Krishnan on 1/19/25.
//

import Foundation

struct NewsItem: Codable {
    
    /*
    here is a sample news item that will get mapped
    {
        "source": {
          "id": null,
          "name": "Yahoo Entertainment"
        },
        "author": "Mat Smith",
        "title": "The Morning After: What to expect at CES 2025",
        "description": "The holidays haven’t even kicked off, but we’re already looking to next year when, almost immediately, some of the Engadget team will head to Las Vegas for tech’s biggest annual conference. The pitches from companies, both legit and unhinged, are already fill…",
        "url": "https://consent.yahoo.com/v2/collectConsent?sessionId=1_cc-session_b8d5b11a-45bf-40d5-98c0-33fe6962feb7",
        "urlToImage": null,
        "publishedAt": "2024-12-17T12:15:28Z",
        "content": "If you click 'Accept all', we and our partners, including 237 who are part of the IAB Transparency &amp; Consent Framework, will also store and/or access information on a device (in other words, use … [+678 chars]"
      },
    */
    var title: String = ""
    var description: String?
    var author: String?
    var publishedAt: String?

    var url: String = ""
    var urlToImage: String?
    
    // var content: String?
    // var sourceName: String?
    
    init( title: String, description: String,
          url: String, urlToImage: String?,
          author: String, publishedAt: String) {
        
        self.title = title
        self.description = description
        self.url = url
        self.urlToImage = urlToImage
        self.author = author
        self.publishedAt = publishedAt
    }
    
    func toText() -> String {
        return "\(title)\n\n\(description ?? "")\n\(url)"
    }
}

struct NewsResponse: Codable {
    
    var status: String
    var totalResults: Int
    var articles: [NewsItem]
}

class NewsListProvider {
    
    var urlPrefix: String = ""   // default unless it is changed
    var apiKey: String = ""
    
    init( url: String, apiKey: String) {
        self.urlPrefix = url
        self.apiKey = apiKey
    }
}

class NewsListModel: ObservableObject {
    
    @Published var newsItems = [NewsItem]()
    @Published var newsFromSource: String = ""
    @Published var newsFromType: String = ""
    
    func fetchNewsItems(forSource source: String, withType type: String) {
        
        let newsProvider = NewsConfig.shared.newsProvider
        let urlForNews = "\(newsProvider.urlPrefix)\(type)?sources=\(source)&apiKey=\(newsProvider.apiKey)"
        NewsConfig.logger.info("Fetching news from [\(source)] for [\(type)]")
//        NewsConfig.logger.info("URL is\(urlForNews)")
        
        if ( (source.isEmpty || (source == newsFromSource)
              || type.isEmpty || (type == newsFromType)) ) {
            
            NewsConfig.logger.debug("Input parameters are similar to what we have already. Do not fetch news.")
            return
        }
        
        guard let url = URL(string: urlForNews) else {
            NewsConfig.logger.error("Invalid NEWS URL: \(urlForNews)")
            return
        }
        
        let urlRequest = URLRequest(url: url)
        
        URLSession.shared.dataTask(with: urlRequest) {
            (data, response, error) in
            
            if let error = error {
                NewsConfig.logger.error("Error fetching news: \(error)")
                return
            }
            
            guard let data = data else {
                
                NewsConfig.logger.error("NO data found for fetching news")
                return
            }
            
            if let decodedNewsItems = try? JSONDecoder().decode(NewsResponse.self, from: data) {
                
                // successfully decoded the data. let us use it
                // set the values in the main thread
                
                NewsConfig.logger.info( "\(decodedNewsItems.totalResults) NewsItems downloaded with status \(decodedNewsItems.status)")
                
                DispatchQueue.main.async {
                    // setting the newsItems will publish changes for upstream UI to pick it up
                    self.newsItems = decodedNewsItems.articles
                }
                
                return;
            }
        }.resume()
    }
}
