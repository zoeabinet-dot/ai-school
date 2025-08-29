import SwiftUI

struct ContentView: View {
    @StateObject private var userManager = UserManager.shared
    @State private var isAuthenticated = false
    
    var body: some View {
        Group {
            if isAuthenticated {
                MainTabView()
            } else {
                LoginView()
            }
        }
        .onAppear {
            checkAuthenticationStatus()
        }
        .onReceive(userManager.$isAuthenticated) { authenticated in
            isAuthenticated = authenticated
        }
    }
    
    private func checkAuthenticationStatus() {
        isAuthenticated = userManager.isAuthenticated
    }
}

struct MainTabView: View {
    var body: some View {
        TabView {
            DashboardView()
                .tabItem {
                    Image(systemName: "house.fill")
                    Text("Dashboard")
                }
            
            StudentListView()
                .tabItem {
                    Image(systemName: "person.3.fill")
                    Text("Students")
                }
            
            AILessonView()
                .tabItem {
                    Image(systemName: "brain.head.profile")
                    Text("AI Lessons")
                }
            
            AnalyticsView()
                .tabItem {
                    Image(systemName: "chart.bar.fill")
                    Text("Analytics")
                }
            
            MonitoringView()
                .tabItem {
                    Image(systemName: "camera.fill")
                    Text("Monitoring")
                }
            
            FamilyView()
                .tabItem {
                    Image(systemName: "house.2.fill")
                    Text("Families")
                }
            
            StaffView()
                .tabItem {
                    Image(systemName: "person.badge.plus")
                    Text("Staff")
                }
            
            LessonsView()
                .tabItem {
                    Image(systemName: "book.fill")
                    Text("Lessons")
                }
        }
        .accentColor(.blue)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}