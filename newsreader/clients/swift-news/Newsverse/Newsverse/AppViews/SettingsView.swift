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
    
    let sourceKeys = NewsConfig.shared.newsSources.contentSources.map{ $0.key}

    let sourceValues = NewsConfig.shared.newsSources.contentSources.map{ $0.value}
    
    var body: some View {
                    
        NavigationView {
            Form {
                // enable content type selector
                Section( header: Text( "News Type")) {
                    Picker( selection: $contentTypeIndex,
                            label: Text("")
                            ) {
                        Text( "Top Headlines").tag(0)
                        Text( "Everything").tag(1)
                    }.pickerStyle(SegmentedPickerStyle())
                }
                
                // enable content source selector type 2
                Section( header: Text( "News Sources")) {
                    Picker( selection: $contentSourceIndex,
                            label: Text("Get News from")) {
                        ForEach(sourceValues.indices, id: \.self) { index in
                            Text(sourceValues[index])
                        }
                    }
                }
            }
            .padding()
            .navigationBarTitle( "Settings")
            .navigationBarTitleDisplayMode( .inline)
        }
        .onAppear() {
            
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
            
            if ( self.contentSourceIndex >= 0) {
                NewsConfig.shared.newsSources.contentSource = self.sourceKeys[ self.contentSourceIndex]
                NewsConfig.logger.info( "Updating News Content Source to \(NewsConfig.shared.newsSources.contentSource)")
            }
            
            // Save the information in user defaults for the future
            NewsConfig.shared.newsSources.save()
        }
    }
}

struct ShowSettingsButton: View {
    @State private var fSettingsScreen: Bool = false
    
    var body: some View {
        Button { fSettingsScreen = true }
        label: {
            Image(systemName: "gear")
                .font(.title3)
                .foregroundColor( .accentColor)
        }
        .sheet(isPresented: $fSettingsScreen) {
            SettingsView()
                .presentationDragIndicator(.visible)
        }
    }
}

#Preview {
    ShowSettingsButton()
    SettingsView()
}
