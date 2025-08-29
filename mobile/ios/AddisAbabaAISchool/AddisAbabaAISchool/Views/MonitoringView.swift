import SwiftUI
import AVFoundation

struct MonitoringView: View {
    @StateObject private var viewModel = MonitoringViewModel()
    @State private var showingPrivacySettings = false
    @State private var showingAlertSettings = false
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Monitoring Status
                    MonitoringStatusCard(viewModel: viewModel)
                    
                    // Privacy Controls
                    PrivacyControlsCard(viewModel: viewModel)
                    
                    // Recent Sessions
                    RecentSessionsCard(sessions: viewModel.recentSessions)
                    
                    // Behavior Analytics
                    BehaviorAnalyticsCard(analytics: viewModel.behaviorAnalytics)
                    
                    // Alerts
                    AlertsCard(alerts: viewModel.recentAlerts)
                }
                .padding()
            }
            .navigationTitle("Monitoring")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Menu {
                        Button("Privacy Settings") {
                            showingPrivacySettings = true
                        }
                        Button("Alert Settings") {
                            showingAlertSettings = true
                        }
                    } label: {
                        Image(systemName: "ellipsis.circle")
                    }
                }
            }
            .sheet(isPresented: $showingPrivacySettings) {
                PrivacySettingsView()
            }
            .sheet(isPresented: $showingAlertSettings) {
                AlertSettingsView()
            }
        }
        .onAppear {
            viewModel.startMonitoring()
        }
        .onDisappear {
            viewModel.stopMonitoring()
        }
    }
}

struct MonitoringStatusCard: View {
    @ObservedObject var viewModel: MonitoringViewModel
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: viewModel.isMonitoringActive ? "video.fill" : "video.slash")
                    .foregroundColor(viewModel.isMonitoringActive ? .green : .red)
                    .font(.title2)
                
                VStack(alignment: .leading) {
                    Text("Monitoring Status")
                        .font(.headline)
                    Text(viewModel.isMonitoringActive ? "Active" : "Inactive")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
                
                Button(action: {
                    viewModel.toggleMonitoring()
                }) {
                    Text(viewModel.isMonitoringActive ? "Stop" : "Start")
                        .font(.subheadline)
                        .fontWeight(.medium)
                        .padding(.horizontal, 16)
                        .padding(.vertical, 8)
                        .background(viewModel.isMonitoringActive ? Color.red : Color.green)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }
            }
            
            if viewModel.isMonitoringActive {
                HStack {
                    Label("Session Duration: \(viewModel.sessionDuration)", systemImage: "clock")
                    Spacer()
                    Label("Frames Analyzed: \(viewModel.framesAnalyzed)", systemImage: "eye")
                }
                .font(.caption)
                .foregroundColor(.secondary)
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 2, x: 0, y: 1)
    }
}

struct PrivacyControlsCard: View {
    @ObservedObject var viewModel: MonitoringViewModel
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Privacy Controls")
                .font(.headline)
            
            VStack(spacing: 8) {
                Toggle("Enable Face Detection", isOn: $viewModel.faceDetectionEnabled)
                Toggle("Enable Behavior Analysis", isOn: $viewModel.behaviorAnalysisEnabled)
                Toggle("Enable Recording", isOn: $viewModel.recordingEnabled)
                Toggle("Enable Alerts", isOn: $viewModel.alertsEnabled)
            }
            
            Text("Your privacy is important. You can control what data is collected and analyzed.")
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 2, x: 0, y: 1)
    }
}

struct RecentSessionsCard: View {
    let sessions: [MonitoringSession]
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Recent Sessions")
                .font(.headline)
            
            if sessions.isEmpty {
                Text("No recent sessions")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity, alignment: .center)
                    .padding()
            } else {
                ForEach(sessions.prefix(3)) { session in
                    SessionRow(session: session)
                }
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 2, x: 0, y: 1)
    }
}

struct SessionRow: View {
    let session: MonitoringSession
    
    var body: some View {
        HStack {
            VStack(alignment: .leading) {
                Text(session.title)
                    .font(.subheadline)
                    .fontWeight(.medium)
                
                Text(session.duration)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            VStack(alignment: .trailing) {
                Text(session.status.rawValue)
                    .font(.caption)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 2)
                    .background(statusColor(for: session.status))
                    .foregroundColor(.white)
                    .clipShape(Capsule())
                
                Text(session.date, style: .time)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
    
    private func statusColor(for status: SessionStatus) -> Color {
        switch status {
        case .active:
            return .green
        case .completed:
            return .blue
        case .interrupted:
            return .orange
        }
    }
}

struct BehaviorAnalyticsCard: View {
    let analytics: BehaviorAnalytics
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Behavior Analytics")
                .font(.headline)
            
            LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 12) {
                AnalyticsItem(title: "Attention Score", value: "\(analytics.attentionScore)%", icon: "eye.fill")
                AnalyticsItem(title: "Engagement", value: "\(analytics.engagementScore)%", icon: "brain.head.profile")
                AnalyticsItem(title: "Focus Time", value: "\(analytics.focusTime)min", icon: "clock.fill")
                AnalyticsItem(title: "Distractions", value: "\(analytics.distractions)", icon: "exclamationmark.triangle")
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 2, x: 0, y: 1)
    }
}

struct AnalyticsItem: View {
    let title: String
    let value: String
    let icon: String
    
    var body: some View {
        VStack(spacing: 4) {
            Image(systemName: icon)
                .foregroundColor(.blue)
                .font(.title3)
            
            Text(value)
                .font(.headline)
                .fontWeight(.semibold)
            
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 8)
    }
}

struct AlertsCard: View {
    let alerts: [MonitoringAlert]
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Recent Alerts")
                .font(.headline)
            
            if alerts.isEmpty {
                Text("No recent alerts")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity, alignment: .center)
                    .padding()
            } else {
                ForEach(alerts.prefix(3)) { alert in
                    AlertRow(alert: alert)
                }
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 2, x: 0, y: 1)
    }
}

struct AlertRow: View {
    let alert: MonitoringAlert
    
    var body: some View {
        HStack {
            Image(systemName: alert.icon)
                .foregroundColor(alert.severity.color)
                .frame(width: 24, height: 24)
            
            VStack(alignment: .leading, spacing: 2) {
                Text(alert.title)
                    .font(.subheadline)
                    .fontWeight(.medium)
                
                Text(alert.description)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            Text(alert.timeAgo)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding(.vertical, 4)
    }
}

struct PrivacySettingsView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var dataRetentionDays = 30
    @State private var allowDataSharing = false
    @State private var allowAnalytics = true
    
    var body: some View {
        NavigationView {
            Form {
                Section("Data Retention") {
                    HStack {
                        Text("Keep data for")
                        Spacer()
                        TextField("Days", value: $dataRetentionDays, format: .number)
                            .keyboardType(.numberPad)
                            .multilineTextAlignment(.trailing)
                        Text("days")
                    }
                }
                
                Section("Data Sharing") {
                    Toggle("Allow data sharing for research", isOn: $allowDataSharing)
                    Toggle("Allow analytics", isOn: $allowAnalytics)
                }
                
                Section("Data Export") {
                    Button("Export my data") {
                        // Implementation for data export
                    }
                    
                    Button("Delete all data") {
                        // Implementation for data deletion
                    }
                    .foregroundColor(.red)
                }
            }
            .navigationTitle("Privacy Settings")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
        }
    }
}

struct AlertSettingsView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var attentionAlerts = true
    @State private var behaviorAlerts = true
    @State private var technicalAlerts = false
    
    var body: some View {
        NavigationView {
            Form {
                Section("Alert Types") {
                    Toggle("Attention alerts", isOn: $attentionAlerts)
                    Toggle("Behavior alerts", isOn: $behaviorAlerts)
                    Toggle("Technical alerts", isOn: $technicalAlerts)
                }
                
                Section("Notification Settings") {
                    Toggle("Push notifications", isOn: .constant(true))
                    Toggle("Email notifications", isOn: .constant(false))
                    Toggle("Sound alerts", isOn: .constant(true))
                }
            }
            .navigationTitle("Alert Settings")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
        }
    }
}

// MARK: - View Models

class MonitoringViewModel: ObservableObject {
    @Published var isMonitoringActive = false
    @Published var sessionDuration = "00:00"
    @Published var framesAnalyzed = 0
    @Published var faceDetectionEnabled = true
    @Published var behaviorAnalysisEnabled = true
    @Published var recordingEnabled = false
    @Published var alertsEnabled = true
    @Published var recentSessions: [MonitoringSession] = []
    @Published var behaviorAnalytics = BehaviorAnalytics()
    @Published var recentAlerts: [MonitoringAlert] = []
    
    private var timer: Timer?
    private var sessionStartTime: Date?
    
    func startMonitoring() {
        isMonitoringActive = true
        sessionStartTime = Date()
        startTimer()
        loadMonitoringData()
    }
    
    func stopMonitoring() {
        isMonitoringActive = false
        stopTimer()
        saveSession()
    }
    
    func toggleMonitoring() {
        if isMonitoringActive {
            stopMonitoring()
        } else {
            startMonitoring()
        }
    }
    
    private func startTimer() {
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
            self.updateSessionDuration()
        }
    }
    
    private func stopTimer() {
        timer?.invalidate()
        timer = nil
    }
    
    private func updateSessionDuration() {
        guard let startTime = sessionStartTime else { return }
        let duration = Date().timeIntervalSince(startTime)
        let minutes = Int(duration) / 60
        let seconds = Int(duration) % 60
        sessionDuration = String(format: "%02d:%02d", minutes, seconds)
        framesAnalyzed += 1
    }
    
    private func loadMonitoringData() {
        // Load recent sessions, analytics, and alerts
        recentSessions = [
            MonitoringSession(title: "Study Session", duration: "45 min", status: .completed, date: Date()),
            MonitoringSession(title: "AI Lesson", duration: "30 min", status: .completed, date: Date().addingTimeInterval(-3600)),
            MonitoringSession(title: "Homework", duration: "20 min", status: .interrupted, date: Date().addingTimeInterval(-7200))
        ]
        
        behaviorAnalytics = BehaviorAnalytics(
            attentionScore: 85,
            engagementScore: 78,
            focusTime: 45,
            distractions: 3
        )
        
        recentAlerts = [
            MonitoringAlert(title: "Low Attention", description: "Attention level dropped below 60%", severity: .warning, icon: "eye.slash", timeAgo: "5 min ago"),
            MonitoringAlert(title: "Distraction Detected", description: "Multiple distractions detected", severity: .info, icon: "exclamationmark.triangle", timeAgo: "15 min ago")
        ]
    }
    
    private func saveSession() {
        // Save session data
    }
}

// MARK: - Models

struct MonitoringSession: Identifiable {
    let id = UUID()
    let title: String
    let duration: String
    let status: SessionStatus
    let date: Date
}

struct BehaviorAnalytics {
    let attentionScore: Int
    let engagementScore: Int
    let focusTime: Int
    let distractions: Int
}

struct MonitoringAlert: Identifiable {
    let id = UUID()
    let title: String
    let description: String
    let severity: AlertSeverity
    let icon: String
    let timeAgo: String
}

enum SessionStatus: String, CaseIterable {
    case active = "Active"
    case completed = "Completed"
    case interrupted = "Interrupted"
}

enum AlertSeverity: CaseIterable {
    case info, warning, critical
    
    var color: Color {
        switch self {
        case .info:
            return .blue
        case .warning:
            return .orange
        case .critical:
            return .red
        }
    }
}

#Preview {
    MonitoringView()
}