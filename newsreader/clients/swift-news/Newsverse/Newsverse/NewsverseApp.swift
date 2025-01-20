//
//  NewsverseApp.swift
//  Newsverse
//
//  Created by Murali Krishnan on 1/19/25.
//

import SwiftUI
import SwiftData

#if os(iOS)
import UIKit

class NewsverseAppDelegate: NSObject, UIApplicationDelegate {
      
    // handle the app startup event
    func application(_ application: UIApplication,
                     didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey : Any]? = nil
        ) -> Bool {
        
        NewsConfig.logger.log("NewsverseAppDelegate: didFinishLaunchingWithOptions")

        return true
    }
  
    // handle the app cleanup event
    func applicationWillTerminate( _ application: UIApplication) {

        Task {
            NewsConfig.logger.log("NewsverseAppDelegate: applicationWillTerminate")
        }
    }
}
#endif

struct MainContentView: View {
    var body: some View {
        VStack {
            Text("Newsverse")
                .font(.title)
                .foregroundColor( .accentColor)
            TabView {
                NewsListView()
                    .foregroundColor( .accentColor)
                    .tabItem {
                        Image(systemName: "list.bullet")
                        Text("News")
                    }
                SettingsView()
                    .foregroundColor( .accentColor)
                    .tabItem {
                        Image( systemName: "gear")
                        Text("Settings")
                    }
            }
        }
    }
}


@main
struct NewsverseApp: App {
    
#if os(iOS)
    // register app delegate for global app events
    @UIApplicationDelegateAdaptor(NewsverseAppDelegate.self) var delegate
#endif
    /*
    var sharedModelContainer: ModelContainer = {
        let schema = Schema([
            Item.self,
        ])
        let modelConfiguration = ModelConfiguration(schema: schema, isStoredInMemoryOnly: false)

        do {
            return try ModelContainer(for: schema, configurations: [modelConfiguration])
        } catch {
            fatalError("Could not create ModelContainer: \(error)")
        }
    }()
    */
    
    // set up global structures of interest here
    init() {
        
    }

    var body: some Scene {
        WindowGroup {
            MainContentView()
                .preferredColorScheme(.dark)
        }
//        .modelContainer(NewsVerseModelContainer.shared.container)
    }
}

#Preview {
    MainContentView()
//        .modelContainer(for: Item.self, inMemory: true)
        .environment(\.colorScheme, .dark)
}
