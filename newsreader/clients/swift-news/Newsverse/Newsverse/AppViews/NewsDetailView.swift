//
//  NewsDetailView.swift
//  Newsverse
//
//  Created by Murali Krishnan on 1/19/25.
//

import SwiftUI
import WebKit

struct NewsImageView: View {
    
    let imageURL: String

    var body: some View {
        AsyncImage(url: URL(string: imageURL)) { image in
            image
                .resizable()
                .scaledToFit()
                .frame(width: 300)
                .cornerRadius(10)
        } placeholder: {
            Rectangle()
                .fill(Color.yellow.opacity(0.1))
                .frame(width: 300, height: 100)
                .cornerRadius(10)
        }
        .frame(maxHeight: .infinity)
    }
}

struct NewsWebView: UIViewRepresentable {
    let url: URL

    func makeUIView(context: Context) -> WKWebView {
        let webView = WKWebView()
        webView.load(URLRequest(url: url))
        return webView
    }

    func updateUIView(_ webView: WKWebView, context: Context) {}
}

struct NewsDetailView: View {
    
    let item: NewsItem
    
    var body: some View {
        VStack {
            
            // ToDo: Add image to the display
            Text( item.title)
                .foregroundColor( .accentColor)
                .font(.title3)
                .padding( .top, 10)
            
            if let imageURL = item.urlToImage {
                
                NewsImageView( imageURL: imageURL)
            }

            NavigationLink(
                destination: NewsWebView(url: URL(string: item.url)!))
            {
                Text( item.url)
                    .foregroundColor( .blue)
            }
            Spacer()
            Text( item.description ?? "")
                .foregroundColor( .secondary)
        }
    }
}


#Preview {
    
    var newsItem = NewsItem(
        title: "The Morning After: What to expect at CES 2025",
        description: "The holidays haven’t even kicked off, but we’re already looking to next year when, almost immediately, some of the Engadget team will head to Las Vegas for tech’s biggest annual conference. The pitches from companies, both legit and unhinged, are already fill…",
        url: "https://www.engadget.com/general/the-morning-after-engadget-newsletter-121528225.html",
        urlToImage: "https://s.yimg.com/os/creatr-uploaded-images/2024-01/f23d3740-ae32-11ee-8d1b-20ed137b8e8c",
        author: "Mat Smith",
        publishedAt: "2024-12-17T12:15:28Z"
        // newsItem.source = "engadget"
        )
    
//    NewsWebView(url: URL(string: "https://www.cnn.com")!)
    NewsDetailView( item: newsItem)
}
