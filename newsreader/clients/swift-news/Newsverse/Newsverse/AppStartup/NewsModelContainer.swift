//
//  NewsModelContainer.swift
//  Newsverse
//
//  Keeps track of state informatoin for this Newsverse app
//
//  Created by Murali Krishnan on 1/19/25.
//

import Foundation
import SwiftData

class NewsVerseModelContainer: ObservableObject {
    
    static let shared = NewsVerseModelContainer()
    static let container = NewsVerseModelContainer.shared.container
    
    let container: ModelContainer

    private init() {

        let appGroupID = NewsConfig.shared.appInfo.appGroupID
        
        if let appGroupURL = FileManager.default.containerURL(forSecurityApplicationGroupIdentifier: appGroupID) {
            let newsStoreURL = appGroupURL.appendingPathComponent("Library/Application Support/default.store")

            NewsConfig.logger.info("Using Application Group Store at \(newsStoreURL)")

            let newsSchema = Schema([
               // Add objects of interest
            ])

            // Initialize the container with the persistent configuration
            let modelConfiguration = ModelConfiguration( schema: newsSchema, url: newsStoreURL)
            
            do {

                container = try ModelContainer(for: newsSchema, configurations: [modelConfiguration])
                NewsConfig.logger.info( "Success! NewsVerseModelContainer initialized with model container")
                
            } catch {
                NewsConfig.logger.error( "Failed to initialize NewsVerseModelContainer: \(error)")
                fatalError( "Failed to initialize NewsVerseModelContainer: \(error)")
            }
        } else {
            fatalError( "Failed to get app group url for NewsVerseModelContainer")
        }
    }
}
