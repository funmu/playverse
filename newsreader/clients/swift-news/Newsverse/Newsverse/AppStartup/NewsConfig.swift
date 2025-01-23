//
//  NewsConfig.swift
//  Newsverse - keeps track of configuration and global state information
//
//  Created by Murali Krishnan on 1/19/25.
//

import Foundation
import os

class NewsConfig {
    
    static var logger: Logger = Logger(subsystem: "com.verse.newsverse", category: "diagnostics")
    static var shared: NewsConfig = NewsConfig()
    
    var appInfo: AppInfo = AppInfo()
    @Published var newsSources: NewsSources = NewsSources()
    var newsProvider: NewsListProvider
        = NewsListProvider( url: "http://localhost:8080/", apiKey: "") // testing endpoint
        
    // create a private constructor to make sure we use this as a singleton
    private init() {

        NewsConfig.logger.info( "Initializing NewsConfig")
        
        // initialize a key from the environment / information properties
        
        self.newsProvider = self._createNewsProvider();
        
        /*
         logger.info("Informational message")
         logger.debug("This is a debug message")
         logger.error("An error occurred: \(error)")
         */
    }
    
    private func _createNewsProvider() -> NewsListProvider {

        let apiUrl: String? = Bundle.main.object(forInfoDictionaryKey: "NEWS_API_URL") as? String
        let apiKey: String? = Bundle.main.object(forInfoDictionaryKey: "NEWS_API_KEY") as? String
        var newsProvider: NewsListProvider

        if let apiUrl = apiUrl,
           let apiKey = apiKey {

            newsProvider = NewsListProvider( url: apiUrl, apiKey: apiKey)
            NewsConfig.logger.info("Success: a NEWS List Provider is setup ")
        } else {
            newsProvider = NewsListProvider( url: "http://localhost:8080/", apiKey: "") // testing endpoint
            NewsConfig.logger.error("Failed: NEWS list provider could not be setup!")
            // fatalError("Failed: NEWS list provider could not be setup!")
        }
        
        return newsProvider;
    }
}

class AppInfo {
    
    let appName: String = Bundle.main.infoDictionary!["CFBundleDisplayName"] as! String
    let appVersion: String =  Bundle.main.infoDictionary!["CFBundleShortVersionString"] as! String
    let appBuild: String = Bundle.main.infoDictionary!["CFBundleVersion"] as! String
    let appGroupID: String = Bundle.main.infoDictionary!["CFBundleIdentifier"] as! String
}


