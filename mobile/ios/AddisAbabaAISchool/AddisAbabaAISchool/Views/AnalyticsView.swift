import SwiftUI
import Charts

struct AnalyticsView: View {
    @StateObject private var viewModel = AnalyticsViewModel()
    @State private var selectedTimeRange: TimeRange = .week
    @State private var selectedMetric: AnalyticsMetric = .performance
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Time Range Picker
                    Picker("Time Range", selection: $selectedTimeRange) {
                        ForEach(TimeRange.allCases, id: \.self) { range in
                            Text(range.displayName).tag(range)
                        }
                    }
                    .pickerStyle(SegmentedPickerStyle())
                    .padding(.horizontal)
                    
                    // Metric Picker
                    Picker("Metric", selection: $selectedMetric) {
                        ForEach(AnalyticsMetric.allCases, id: \.self) { metric in
                            Text(metric.displayName).tag(metric)
                        }
                    }
                    .pickerStyle(SegmentedPickerStyle())
                    .padding(.horizontal)
                    
                    // Performance Chart
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Performance Overview")
                            .font(.headline)
                            .padding(.horizontal)
                        
                        ChartView(data: viewModel.chartData, metric: selectedMetric)
                            .frame(height: 200)
                            .padding(.horizontal)
                    }
                    
                    // Key Metrics Grid
                    LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 16) {
                        MetricCard(
                            title: "Average Score",
                            value: "\(viewModel.averageScore)%",
                            change: "+5.2%",
                            isPositive: true,
                            icon: "chart.line.uptrend.xyaxis"
                        )
                        
                        MetricCard(
                            title: "Completion Rate",
                            value: "\(viewModel.completionRate)%",
                            change: "+2.1%",
                            isPositive: true,
                            icon: "checkmark.circle.fill"
                        )
                        
                        MetricCard(
                            title: "Study Time",
                            value: "\(viewModel.studyTime)h",
                            change: "-0.5h",
                            isPositive: false,
                            icon: "clock.fill"
                        )
                        
                        MetricCard(
                            title: "AI Sessions",
                            value: "\(viewModel.aiSessions)",
                            change: "+12",
                            isPositive: true,
                            icon: "brain.head.profile"
                        )
                    }
                    .padding(.horizontal)
                    
                    // Subject Performance
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Subject Performance")
                            .font(.headline)
                            .padding(.horizontal)
                        
                        ForEach(viewModel.subjectPerformance, id: \.subject) { performance in
                            SubjectPerformanceRow(performance: performance)
                        }
                    }
                    
                    // Recent Activity
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Recent Activity")
                            .font(.headline)
                            .padding(.horizontal)
                        
                        ForEach(viewModel.recentActivity, id: \.id) { activity in
                            ActivityRow(activity: activity)
                        }
                    }
                }
            }
            .navigationTitle("Analytics")
            .navigationBarTitleDisplayMode(.large)
            .refreshable {
                await viewModel.loadAnalytics()
            }
        }
        .onAppear {
            Task {
                await viewModel.loadAnalytics()
            }
        }
        .onChange(of: selectedTimeRange) { _ in
            Task {
                await viewModel.loadAnalytics()
            }
        }
        .onChange(of: selectedMetric) { _ in
            Task {
                await viewModel.loadAnalytics()
            }
        }
    }
}

struct ChartView: View {
    let data: [ChartDataPoint]
    let metric: AnalyticsMetric
    
    var body: some View {
        Chart(data) { point in
            LineMark(
                x: .value("Date", point.date),
                y: .value("Value", point.value)
            )
            .foregroundStyle(Color.blue)
            .interpolationMethod(.catmullRom)
            
            AreaMark(
                x: .value("Date", point.date),
                y: .value("Value", point.value)
            )
            .foregroundStyle(Color.blue.opacity(0.1))
            .interpolationMethod(.catmullRom)
        }
        .chartXAxis {
            AxisMarks(values: .automatic) { value in
                AxisGridLine()
                AxisValueLabel(format: .dateTime.month().day())
            }
        }
        .chartYAxis {
            AxisMarks { value in
                AxisGridLine()
                AxisValueLabel()
            }
        }
    }
}

struct MetricCard: View {
    let title: String
    let value: String
    let change: String
    let isPositive: Bool
    let icon: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Image(systemName: icon)
                    .foregroundColor(.blue)
                Spacer()
                Text(change)
                    .font(.caption)
                    .foregroundColor(isPositive ? .green : .red)
            }
            
            Text(value)
                .font(.title2)
                .fontWeight(.bold)
            
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 2, x: 0, y: 1)
    }
}

struct SubjectPerformanceRow: View {
    let performance: SubjectPerformance
    
    var body: some View {
        HStack {
            VStack(alignment: .leading) {
                Text(performance.subject)
                    .font(.subheadline)
                    .fontWeight(.medium)
                
                Text("\(performance.lessonsCompleted) lessons completed")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            VStack(alignment: .trailing) {
                Text("\(performance.averageScore)%")
                    .font(.subheadline)
                    .fontWeight(.semibold)
                
                ProgressView(value: Double(performance.averageScore) / 100.0)
                    .frame(width: 60)
            }
        }
        .padding(.horizontal)
        .padding(.vertical, 8)
    }
}

struct ActivityRow: View {
    let activity: ActivityItem
    
    var body: some View {
        HStack {
            Image(systemName: activity.icon)
                .foregroundColor(activity.color)
                .frame(width: 24, height: 24)
            
            VStack(alignment: .leading, spacing: 2) {
                Text(activity.title)
                    .font(.subheadline)
                    .fontWeight(.medium)
                
                Text(activity.description)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            Text(activity.timeAgo)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding(.horizontal)
        .padding(.vertical, 8)
    }
}

// MARK: - View Models

class AnalyticsViewModel: ObservableObject {
    @Published var chartData: [ChartDataPoint] = []
    @Published var averageScore: Int = 0
    @Published var completionRate: Int = 0
    @Published var studyTime: Int = 0
    @Published var aiSessions: Int = 0
    @Published var subjectPerformance: [SubjectPerformance] = []
    @Published var recentActivity: [ActivityItem] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    func loadAnalytics() async {
        await MainActor.run {
            isLoading = true
        }
        
        do {
            let analytics = try await NetworkService.shared.fetchAnalytics()
            await MainActor.run {
                self.updateAnalytics(with: analytics)
                self.isLoading = false
            }
        } catch {
            await MainActor.run {
                self.errorMessage = error.localizedDescription
                self.isLoading = false
            }
        }
    }
    
    private func updateAnalytics(with analytics: AnalyticsData) {
        // Update chart data
        self.chartData = analytics.chartData
        
        // Update metrics
        self.averageScore = analytics.averageScore
        self.completionRate = analytics.completionRate
        self.studyTime = analytics.studyTime
        self.aiSessions = analytics.aiSessions
        
        // Update subject performance
        self.subjectPerformance = analytics.subjectPerformance
        
        // Update recent activity
        self.recentActivity = analytics.recentActivity
    }
}

// MARK: - Models

struct ChartDataPoint: Identifiable {
    let id = UUID()
    let date: Date
    let value: Double
}

struct SubjectPerformance {
    let subject: String
    let averageScore: Int
    let lessonsCompleted: Int
}

struct ActivityItem: Identifiable {
    let id = UUID()
    let title: String
    let description: String
    let icon: String
    let color: Color
    let timeAgo: String
}

struct AnalyticsData {
    let chartData: [ChartDataPoint]
    let averageScore: Int
    let completionRate: Int
    let studyTime: Int
    let aiSessions: Int
    let subjectPerformance: [SubjectPerformance]
    let recentActivity: [ActivityItem]
}

enum TimeRange: CaseIterable {
    case week, month, quarter, year
    
    var displayName: String {
        switch self {
        case .week: return "Week"
        case .month: return "Month"
        case .quarter: return "Quarter"
        case .year: return "Year"
        }
    }
}

enum AnalyticsMetric: CaseIterable {
    case performance, engagement, completion, time
    
    var displayName: String {
        switch self {
        case .performance: return "Performance"
        case .engagement: return "Engagement"
        case .completion: return "Completion"
        case .time: return "Time"
        }
    }
}

#Preview {
    AnalyticsView()
}