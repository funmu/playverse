//
//  NewsListView.swift
//  Newsverse
//
//  Created by Murali Krishnan on 1/19/25.
//

import SwiftUI
import SwiftData


struct NewsListView: View {
    
    @ObservedObject private var newsListModel = NewsListModel()
    @ObservedObject private var newsSources = NewsConfig.shared.newsSources
    
    private var newsSourceToFetch:String { return newsSources.contentSource }
    private var newsTypeToFetch:String { return newsSources.contentType }

    var body: some View {
        VStack {
//            HStack{
//                Text( NewsConfig.shared.newsSources.sourceTitle)
//                    .font( .title2)
//                    .foregroundColor(.accentColor)
//                    .padding(.leading, 20)
//                Spacer()
//            }
//            Text( "News Source: \(newsSourceToFetch)")
//            Text( "News Type: \(newsTypeToFetch)")
            
            NavigationView {
                List( newsListModel.newsItems, id: \.url) { item in
                    NavigationLink {
                        // ToDo: add more elaborate view of news article
                        NewsDetailView( item: item)
                        Divider()
                    } label: {
                        Text("\(item.title)")
                    }
                    .padding(.leading, -10)
                    .padding(.trailing, -10)
                }
                .onAppear() {
                    NewsConfig.logger.info( "ListView: onAppear() called ... ")
                    self.newsListModel.fetchNewsItems(
                        forSource: newsSources.contentSource,
                        withType: newsSources.contentType
                    )
                }
                .onChange(of: self.newsSourceToFetch) { _, _ in // Observe changes and recalc
                    NewsConfig.logger.info( "ListView: onChange() for newsSource called ... ")
                    self.newsListModel.fetchNewsItems(
                        forSource: newsSources.contentSource,
                        withType: newsSources.contentType
                    )
                }
                .onChange(of: self.newsTypeToFetch) { _, _ in // Observe changes and recalc
                    NewsConfig.logger.info( "ListView: onChange() for newsType called ... ")
                    self.newsListModel.fetchNewsItems(
                        forSource: self.newsSourceToFetch,
                        withType: self.newsTypeToFetch
                    )
                }
//                .toolbar {
//                    ToolbarItem(placement: .navigationBarTrailing) {
//                        ShowSettingsButton()
//                    }
//                }
                .navigationBarTitle( newsSources.sourceTitle + " (\(newsListModel.newsItems.count))")
                .navigationBarTitleDisplayMode(.inline) // Display the title inline
#if os(macOS)
                .navigationSplitViewColumnWidth(min: 180, ideal: 200)
#endif
            }

        }
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

#Preview {
    NewsListView()
        .modelContainer(for: Item.self, inMemory: true)
        .environment(\.colorScheme, .dark)
}
