import SwiftUI
import Charts

struct DashboardView: View {
    @StateObject private var userManager = UserManager.shared
    @State private var selectedTimeRange: TimeRange = .week
    @State private var isLoading = false
    @State private var dashboardData: DashboardData?
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Header
                    VStack(alignment: .leading, spacing: 10) {
                        HStack {
                            VStack(alignment: .leading, spacing: 5) {
                                Text("Welcome back,")
                                    .font(.title2)
                                    .foregroundColor(.secondary)
                                
                                Text(userManager.currentUser?.firstName ?? "User")
                                    .font(.largeTitle)
                                    .fontWeight(.bold)
                            }
                            
                            Spacer()
                            
                            // Profile Image
                            Circle()
                                .fill(Color.blue.gradient)
                                .frame(width: 60, height: 60)
                                .overlay(
                                    Text(String(userManager.currentUser?.firstName?.prefix(1) ?? "U"))
                                        .font(.title2)
                                        .fontWeight(.bold)
                                        .foregroundColor(.white)
                                )
                        }
                        
                        // Time Range Picker
                        Picker("Time Range", selection: $selectedTimeRange) {
                            ForEach(TimeRange.allCases, id: \.self) { range in
                                Text(range.displayName).tag(range)
                            }
                        }
                        .pickerStyle(SegmentedPickerStyle())
                    }
                    .padding(.horizontal)
                    
                    // Quick Stats
                    LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 15) {
                        QuickStatCard(
                            title: "Total Students",
                            value: "\(dashboardData?.totalStudents ?? 0)",
                            icon: "person.3.fill",
                            color: .blue
                        )
                        
                        QuickStatCard(
                            title: "Active Lessons",
                            value: "\(dashboardData?.activeLessons ?? 0)",
                            icon: "book.fill",
                            color: .green
                        )
                        
                        QuickStatCard(
                            title: "AI Sessions",
                            value: "\(dashboardData?.aiSessions ?? 0)",
                            icon: "brain.head.profile",
                            color: .purple
                        )
                        
                        QuickStatCard(
                            title: "Attendance",
                            value: "\(dashboardData?.attendanceRate ?? 0)%",
                            icon: "checkmark.circle.fill",
                            color: .orange
                        )
                    }
                    .padding(.horizontal)
                    
                    // Role-Based Content
                    switch userManager.currentUser?.role {
                    case .admin:
                        AdminDashboardContent(dashboardData: dashboardData)
                    case .staff:
                        StaffDashboardContent(dashboardData: dashboardData)
                    case .student:
                        StudentDashboardContent(dashboardData: dashboardData)
                    case .family:
                        FamilyDashboardContent(dashboardData: dashboardData)
                    default:
                        EmptyView()
                    }
                    
                    // Recent Activity
                    RecentActivityView(activities: dashboardData?.recentActivities ?? [])
                        .padding(.horizontal)
                    
                    // Performance Chart
                    if let performanceData = dashboardData?.performanceData {
                        PerformanceChartView(data: performanceData, timeRange: selectedTimeRange)
                            .padding(.horizontal)
                    }
                }
                .padding(.vertical)
            }
            .navigationTitle("Dashboard")
            .navigationBarTitleDisplayMode(.large)
            .refreshable {
                await loadDashboardData()
            }
        }
        .onAppear {
            Task {
                await loadDashboardData()
            }
        }
        .onChange(of: selectedTimeRange) { _ in
            Task {
                await loadDashboardData()
            }
        }
    }
    
    private func loadDashboardData() async {
        isLoading = true
        
        // Simulate API call
        try? await Task.sleep(nanoseconds: 1_000_000_000)
        
        // Mock data - in real app, this would come from API
        dashboardData = DashboardData.mockData(for: userManager.currentUser?.role ?? .student)
        
        isLoading = false
    }
}

// MARK: - Quick Stat Card
struct QuickStatCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: icon)
                    .font(.title2)
                    .foregroundColor(color)
                
                Spacer()
            }
            
            Text(value)
                .font(.title)
                .fontWeight(.bold)
                .foregroundColor(.primary)
            
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 5, x: 0, y: 2)
    }
}

// MARK: - Admin Dashboard Content
struct AdminDashboardContent: View {
    let dashboardData: DashboardData?
    
    var body: some View {
        VStack(alignment: .leading, spacing: 15) {
            Text("Administrative Overview")
                .font(.headline)
                .padding(.horizontal)
            
            LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 15) {
                AdminStatCard(
                    title: "Total Staff",
                    value: "\(dashboardData?.totalStaff ?? 0)",
                    icon: "person.badge.plus",
                    color: .indigo
                )
                
                AdminStatCard(
                    title: "Total Families",
                    value: "\(dashboardData?.totalFamilies ?? 0)",
                    icon: "house.2.fill",
                    color: .teal
                )
            }
            .padding(.horizontal)
        }
    }
}

// MARK: - Staff Dashboard Content
struct StaffDashboardContent: View {
    let dashboardData: DashboardData?
    
    var body: some View {
        VStack(alignment: .leading, spacing: 15) {
            Text("Teaching Overview")
                .font(.headline)
                .padding(.horizontal)
            
            LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 15) {
                StaffStatCard(
                    title: "My Classes",
                    value: "\(dashboardData?.myClasses ?? 0)",
                    icon: "graduationcap.fill",
                    color: .green
                )
                
                StaffStatCard(
                    title: "Pending Tasks",
                    value: "\(dashboardData?.pendingTasks ?? 0)",
                    icon: "list.clipboard.fill",
                    color: .red
                )
            }
            .padding(.horizontal)
        }
    }
}

// MARK: - Student Dashboard Content
struct StudentDashboardContent: View {
    let dashboardData: DashboardData?
    
    var body: some View {
        VStack(alignment: .leading, spacing: 15) {
            Text("Learning Progress")
                .font(.headline)
                .padding(.horizontal)
            
            LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 15) {
                StudentStatCard(
                    title: "Current Grade",
                    value: "\(dashboardData?.currentGrade ?? "A")",
                    icon: "star.fill",
                    color: .yellow
                )
                
                StudentStatCard(
                    title: "Lessons Completed",
                    value: "\(dashboardData?.lessonsCompleted ?? 0)",
                    icon: "checkmark.circle.fill",
                    color: .green
                )
            }
            .padding(.horizontal)
        }
    }
}

// MARK: - Family Dashboard Content
struct FamilyDashboardContent: View {
    let dashboardData: DashboardData?
    
    var body: some View {
        VStack(alignment: .leading, spacing: 15) {
            Text("Family Overview")
                .font(.headline)
                .padding(.horizontal)
            
            LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 15) {
                FamilyStatCard(
                    title: "Children",
                    value: "\(dashboardData?.childrenCount ?? 0)",
                    icon: "person.2.fill",
                    color: .pink
                )
                
                FamilyStatCard(
                    title: "Messages",
                    value: "\(dashboardData?.unreadMessages ?? 0)",
                    icon: "message.fill",
                    color: .blue
                )
            }
            .padding(.horizontal)
        }
    }
}

// MARK: - Supporting Views
struct AdminStatCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color
    
    var body: some View {
        QuickStatCard(title: title, value: value, icon: icon, color: color)
    }
}

struct StaffStatCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color
    
    var body: some View {
        QuickStatCard(title: title, value: value, icon: icon, color: color)
    }
}

struct StudentStatCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color
    
    var body: some View {
        QuickStatCard(title: title, value: value, icon: icon, color: color)
    }
}

struct FamilyStatCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color
    
    var body: some View {
        QuickStatCard(title: title, value: value, icon: icon, color: color)
    }
}

struct DashboardView_Previews: PreviewProvider {
    static var previews: some View {
        DashboardView()
    }
}