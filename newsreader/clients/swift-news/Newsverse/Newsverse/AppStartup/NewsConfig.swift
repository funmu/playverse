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
    
    // create a private constructor to make sure we use this as a singleton
    private init() {

        NewsConfig.logger.info( "Initializing NewsConfig")
        
        /*
         logger.info("Informational message")
         logger.debug("This is a debug message")
         logger.error("An error occurred: \(error)")
         */
    }
}

class AppInfo {
    
    var appName: String = "Newsverse"
    var appVersion: String = "0.0.1"
    var appBuild: String = "0"
    var appGroupID: String = "com.verse.newsverse"
}


