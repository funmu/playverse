//
//  NewsListView.swift
//  Newsverse
//
//  Created by Murali Krishnan on 1/19/25.
//

import SwiftUI
import SwiftData

struct NewsDetailView: View {
    
    let item: NewsItem
    
    var body: some View {
        VStack {
            Text( item.title)
                .foregroundColor( .accentColor)
                .font(.title)
                .padding( .top, 10)
            Text( item.url)
                .foregroundColor( .blue)
            Spacer()
            Text( item.description ?? "")
                .foregroundColor( .secondary)
        }
    }
}

struct NewsListView: View {
    
    @ObservedObject private var newsListModel = NewsListModel()

    var body: some View {
        NavigationView {
            List( newsListModel.newsItems, id: \.url) { item in
                NavigationLink {
                    // ToDo: add more elaborate view of news article
                    NewsDetailView( item: item)
                    Divider()
                } label: {
                    Text("\(item.title)")
                }
            }
#if os(macOS)
            .navigationSplitViewColumnWidth(min: 180, ideal: 200)
#endif
        }
        .onAppear() {
            self.newsListModel.fetchNewsItems(
                forSource: NewsConfig.shared.newsSources.contentSource,
                withType: NewsConfig.shared.newsSources.contentType
                )
        }
        .navigationTitle( NewsConfig.shared.newsSources.sourceTitle)
        .navigationBarTitle( NewsConfig.shared.newsSources.sourceTitle)
        .navigationBarTitleDisplayMode(.inline) // Display the title inline
    }
}

struct NewsListViewFromSavedData: View {
    @Environment(\.modelContext) private var modelContext
    @Query private var items: [Item]
    
    @ObservedObject private var newsListModel = NewsListModel()

    var body: some View {
        NavigationSplitView {
            List {
                ForEach(items) { item in
                    NavigationLink {
                        Text("Item at \(item.timestamp, format: Date.FormatStyle(date: .numeric, time: .standard))")
                    } label: {
                        Text(item.timestamp, format: Date.FormatStyle(date: .numeric, time: .standard))
                    }
                }
                .onDelete(perform: deleteItems)
            }
#if os(macOS)
            .navigationSplitViewColumnWidth(min: 180, ideal: 200)
#endif
            .toolbar {
#if os(iOS)
                ToolbarItem(placement: .navigationBarTrailing) {
                    EditButton()
                }
#endif
                ToolbarItem {
                    Button(action: addItem) {
                        Label("Add Item", systemImage: "plus")
                    }
                }
            }
        } detail: {
            Text("Select a News item")
                .navigationTitle("News") // Set the navigation title
                .navigationBarTitleDisplayMode(.inline) // Display the title inline
        }
    }

    private func addItem() {
        withAnimation {
            let newItem = Item(timestamp: Date())
            modelContext.insert(newItem)
        }
    }

    private func deleteItems(offsets: IndexSet) {
        withAnimation {
            for index in offsets {
                modelContext.delete(items[index])
            }
        }
    }
}
