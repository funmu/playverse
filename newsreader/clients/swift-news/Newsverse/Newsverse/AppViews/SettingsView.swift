//
//  SettingsView.swift
//  Newsverse
//
//  Created by Murali Krishnan on 1/19/25.
//

import SwiftUI

struct SettingsView: View {
    
    @State private var contentSourceIndex: Int = -1
    @State private var contentTypeIndex: Int = 0
    
    @State private var sourceKeys: [String] = []
    @State private var sourceValues: [String] = []
    
    var body: some View {
        
        VStack {
            Text("SettingsView")
                .font(.title)
                .foregroundColor( .accentColor)
            
            NavigationView {
                Form {
                    // enable content type selector
                    Section( header: Text( "News Type")) {
                        Picker( selection: $contentTypeIndex, label: Text("")) {
                            Text( "Top Headlines").tag(0)
                            Text( "Everything").tag(1)
                        }.pickerStyle(SegmentedPickerStyle())
                    }
                    
                    // enable content source selector
                    Section( header: Text( "News Sources")) {
                        Picker( selection: $contentSourceIndex, label: Text("Get News from")) {
                            ForEach(sourceValues, id: \.self) { value in
                                Text(value)
                                    .foregroundColor( .accentColor)
                            }
                        }
                    }
                }
                .padding()
                .navigationBarTitle( "Settings")
            }
        }
        .onAppear() {
            self.sourceKeys = NewsConfig.shared.newsSources.contentSources.keys.sorted(by: <)
            self.sourceValues = NewsConfig.shared.newsSources.contentSources.values.sorted(by: <)
            
            // select the right source index
            if ( self.contentSourceIndex < 0) {
                if let index = self.sourceKeys.firstIndex(of: NewsConfig.shared.newsSources.contentSource) {
                    self.contentSourceIndex = index
                }
            } else {
                NewsConfig.shared.newsSources.contentSource = self.sourceKeys[ self.contentSourceIndex]
                NewsConfig.logger.info( "Updating News Content Source to \(NewsConfig.shared.newsSources.contentSource)")
            }
            
        }
        .onDisappear() {
            NewsConfig.shared.newsSources.contentType
            = (self.contentTypeIndex == 0)
            ? NewsConfig.shared.newsSources.displayContentType[0]
            : NewsConfig.shared.newsSources.displayContentType[1]
            NewsConfig.logger.info( "Updating News Content type to \(NewsConfig.shared.newsSources.contentType)")
        }
    }
}

#Preview {
    SettingsView()
}
