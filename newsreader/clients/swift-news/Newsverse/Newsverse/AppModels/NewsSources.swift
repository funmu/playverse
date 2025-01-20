//
//  NewsSources.swift
//  Newsverse
//
//  Created by Murali Krishnan on 1/19/25.
//

import Foundation

class NewsSources: ObservableObject {
    
    @Published var contentSource: String = "bbc-news"
    @Published var contentType: String = "top-headlines"
    
    var sourceTitle: String {
        get { self.contentSources[self.contentSource] ?? self.contentSource }
    }
    
    var displayContentType: [String] =
        ["top-headlines", "everything"];
    
    var contentSources: [String:String] = [
            "reuters"       : "Reuters",
            "associated-press": "Asspciated Press",
            "ap"            : "Associated Press",
            "bloomberg"     : "Bloomberg News",
            "fortune"       : "Fortune",
            "newsweek"      : "Newsweek",
            "new-york-magazine" : "New York Magazine",
            "new-scientist" : "New Scientist",

            "abc-news"      : "ABC News",
            "bbc-news"      : "BBC News",
            "cbs-news"      : "CBS News",
            "nbc-news"      : "NBC News",
            "cnn"           : "CNN (Cable News Network)",
            "cnbc"          : "CNBC",
            "msnbc"         : "MSNBC News",

            "buzzfeed"      : "Buzzfeed",
            "engadget"      : "Engadget",
            "ars-technica"  : "Ars Technica",
            "google-news"   : "Google News",
            "hacker-news"   : "Hacker News",
            "techcrunch"    : "TechCrunch",
            "gizmodo"       : "Gizmodo",
    ]
    
    init() {
        load()
    }
    
    func load() {
        // load up from the past saved value if any
        
        self.contentType = UserDefaults.standard.string( forKey: "contentType") ?? "top-headlines"
        self.contentSource = UserDefaults.standard.string( forKey: "contentSource") ?? "reuters"
    }

    func save() {
        // save for the future use
        UserDefaults.standard.set( self.contentType, forKey: "contentType")
        UserDefaults.standard.set( self.contentSource, forKey: "contentSource")
    }

}
