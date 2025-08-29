import SwiftUI

struct StaffView: View {
    @StateObject private var viewModel = StaffViewModel()
    @State private var showingAddStaff = false
    @State private var selectedStaff: Staff?
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Staff Overview
                    StaffOverviewCard(staff: viewModel.staffMembers)
                    
                    // Staff List
                    StaffListCard(staff: viewModel.staffMembers)
                    
                    // Assignments
                    AssignmentsCard(assignments: viewModel.assignments)
                    
                    // Performance Metrics
                    PerformanceCard(performance: viewModel.performance)
                }
                .padding()
            }
            .navigationTitle("Staff")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: { showingAddStaff = true }) {
                        Image(systemName: "plus")
                    }
                }
            }
            .sheet(isPresented: $showingAddStaff) {
                AddStaffView()
            }
            .sheet(item: $selectedStaff) { staff in
                StaffDetailView(staff: staff)
            }
        }
        .onAppear {
            Task {
                await viewModel.loadStaffData()
            }
        }
    }
}

struct StaffOverviewCard: View {
    let staff: [Staff]
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Staff Overview")
                .font(.headline)
            
            LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 12) {
                OverviewItem(title: "Total Staff", value: "\(staff.count)", icon: "person.2.fill")
                OverviewItem(title: "Active", value: "\(staff.filter { $0.isActive }.count)", icon: "checkmark.circle.fill")
                OverviewItem(title: "Teachers", value: "\(staff.filter { $0.role == .teacher }.count)", icon: "graduationcap.fill")
                OverviewItem(title: "Administrators", value: "\(staff.filter { $0.role == .administrator }.count)", icon: "person.badge.key.fill")
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 2, x: 0, y: 1)
    }
}

struct OverviewItem: View {
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

struct StaffListCard: View {
    let staff: [Staff]
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Staff Members")
                .font(.headline)
            
            if staff.isEmpty {
                Text("No staff members")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity, alignment: .center)
                    .padding()
            } else {
                ForEach(staff) { member in
                    StaffRow(staff: member)
                }
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 2, x: 0, y: 1)
    }
}

struct StaffRow: View {
    let staff: Staff
    
    var body: some View {
        HStack {
            // Staff Avatar
            AsyncImage(url: URL(string: staff.profileImage ?? "")) { image in
                image
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } placeholder: {
                Image(systemName: "person.circle.fill")
                    .foregroundColor(.gray)
            }
            .frame(width: 50, height: 50)
            .clipShape(Circle())
            
            VStack(alignment: .leading, spacing: 4) {
                Text("\(staff.firstName) \(staff.lastName)")
                    .font(.subheadline)
                    .fontWeight(.medium)
                
                Text(staff.role.displayName)
                    .font(.caption)
                    .foregroundColor(.secondary)
                
                Text(staff.department)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            VStack(alignment: .trailing, spacing: 4) {
                Text(staff.isActive ? "Active" : "Inactive")
                    .font(.caption)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 2)
                    .background(staff.isActive ? Color.green.opacity(0.2) : Color.gray.opacity(0.2))
                    .foregroundColor(staff.isActive ? .green : .gray)
                    .clipShape(Capsule())
                
                Text("\(staff.performanceScore)%")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
}

struct AssignmentsCard: View {
    let assignments: [StaffAssignment]
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Current Assignments")
                .font(.headline)
            
            if assignments.isEmpty {
                Text("No current assignments")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity, alignment: .center)
                    .padding()
            } else {
                ForEach(assignments.prefix(3)) { assignment in
                    AssignmentRow(assignment: assignment)
                }
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 2, x: 0, y: 1)
    }
}

struct AssignmentRow: View {
    let assignment: StaffAssignment
    
    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 2) {
                Text(assignment.title)
                    .font(.subheadline)
                    .fontWeight(.medium)
                
                Text(assignment.description)
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .lineLimit(2)
            }
            
            Spacer()
            
            VStack(alignment: .trailing, spacing: 2) {
                Text(assignment.status.rawValue)
                    .font(.caption)
                    .padding(.horizontal, 6)
                    .padding(.vertical, 2)
                    .background(statusColor(for: assignment.status))
                    .foregroundColor(.white)
                    .clipShape(Capsule())
                
                Text(assignment.dueDate, style: .date)
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
    
    private func statusColor(for status: AssignmentStatus) -> Color {
        switch status {
        case .active:
            return .green
        case .completed:
            return .blue
        case .pending:
            return .orange
        case .overdue:
            return .red
        }
    }
}

struct PerformanceCard: View {
    let performance: StaffPerformance
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Performance Metrics")
                .font(.headline)
            
            LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 12) {
                PerformanceItem(title: "Average Score", value: "\(performance.averageScore)%", icon: "chart.line.uptrend.xyaxis")
                PerformanceItem(title: "Tasks Completed", value: "\(performance.tasksCompleted)", icon: "checkmark.circle.fill")
                PerformanceItem(title: "Student Satisfaction", value: "\(performance.studentSatisfaction)%", icon: "heart.fill")
                PerformanceItem(title: "Attendance", value: "\(performance.attendance)%", icon: "calendar")
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 2, x: 0, y: 1)
    }
}

struct PerformanceItem: View {
    let title: String
    let value: String
    let icon: String
    
    var body: some View {
        VStack(spacing: 4) {
            Image(systemName: icon)
                .foregroundColor(.green)
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

struct AddStaffView: View {
    @Environment(\.dismiss) private var dismiss
    @StateObject private var viewModel = AddStaffViewModel()
    
    var body: some View {
        NavigationView {
            Form {
                Section("Personal Information") {
                    TextField("First Name", text: $viewModel.firstName)
                    TextField("Last Name", text: $viewModel.lastName)
                    TextField("Email", text: $viewModel.email)
                        .keyboardType(.emailAddress)
                    TextField("Phone", text: $viewModel.phone)
                        .keyboardType(.phonePad)
                }
                
                Section("Professional Information") {
                    Picker("Role", selection: $viewModel.role) {
                        ForEach(StaffRole.allCases, id: \.self) { role in
                            Text(role.displayName).tag(role)
                        }
                    }
                    
                    TextField("Department", text: $viewModel.department)
                    TextField("Position", text: $viewModel.position)
                }
                
                Section("Employment") {
                    DatePicker("Hire Date", selection: $viewModel.hireDate, displayedComponents: .date)
                    Toggle("Active", isOn: $viewModel.isActive)
                }
            }
            .navigationTitle("Add Staff")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Save") {
                        Task {
                            await viewModel.saveStaff()
                            dismiss()
                        }
                    }
                    .disabled(!viewModel.isValid)
                }
            }
        }
    }
}

struct StaffDetailView: View {
    let staff: Staff
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            StaffInfoView(staff: staff)
                .tabItem {
                    Image(systemName: "person")
                    Text("Info")
                }
                .tag(0)
            
            StaffAssignmentsView(staff: staff)
                .tabItem {
                    Image(systemName: "list.bullet")
                    Text("Assignments")
                }
                .tag(1)
            
            StaffPerformanceView(staff: staff)
                .tabItem {
                    Image(systemName: "chart.bar")
                    Text("Performance")
                }
                .tag(2)
        }
        .navigationTitle("\(staff.firstName) \(staff.lastName)")
        .navigationBarTitleDisplayMode(.inline)
    }
}

struct StaffInfoView: View {
    let staff: Staff
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Staff Header
                HStack {
                    AsyncImage(url: URL(string: staff.profileImage ?? "")) { image in
                        image
                            .resizable()
                            .aspectRatio(contentMode: .fill)
                    } placeholder: {
                        Image(systemName: "person.circle.fill")
                            .foregroundColor(.gray)
                    }
                    .frame(width: 80, height: 80)
                    .clipShape(Circle())
                    
                    VStack(alignment: .leading) {
                        Text("\(staff.firstName) \(staff.lastName)")
                            .font(.title2)
                            .fontWeight(.bold)
                        
                        Text(staff.role.displayName)
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                        
                        Text(staff.department)
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    
                    Spacer()
                }
                .padding()
                
                // Professional Information
                VStack(alignment: .leading, spacing: 15) {
                    Text("Professional Information")
                        .font(.headline)
                        .padding(.horizontal)
                    
                    InfoRow(title: "Position", value: staff.position)
                    InfoRow(title: "Department", value: staff.department)
                    InfoRow(title: "Email", value: staff.email)
                    InfoRow(title: "Phone", value: staff.phone)
                    InfoRow(title: "Status", value: staff.isActive ? "Active" : "Inactive")
                }
            }
        }
    }
}

struct StaffAssignmentsView: View {
    let staff: Staff
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text("Current Assignments")
                    .font(.headline)
                    .padding()
                
                // Placeholder for assignments
                Text("Assignments will be displayed here")
                    .foregroundColor(.secondary)
                    .padding()
            }
        }
    }
}

struct StaffPerformanceView: View {
    let staff: Staff
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text("Performance Metrics")
                    .font(.headline)
                    .padding()
                
                // Placeholder for performance metrics
                Text("Performance metrics will be displayed here")
                    .foregroundColor(.secondary)
                    .padding()
            }
        }
    }
}

// MARK: - View Models

class StaffViewModel: ObservableObject {
    @Published var staffMembers: [Staff] = []
    @Published var assignments: [StaffAssignment] = []
    @Published var performance = StaffPerformance()
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    func loadStaffData() async {
        await MainActor.run {
            isLoading = true
        }
        
        do {
            let staffData = try await NetworkService.shared.fetchStaffData()
            await MainActor.run {
                self.updateStaffData(with: staffData)
                self.isLoading = false
            }
        } catch {
            await MainActor.run {
                self.errorMessage = error.localizedDescription
                self.isLoading = false
            }
        }
    }
    
    private func updateStaffData(with data: StaffData) {
        self.staffMembers = data.staff
        self.assignments = data.assignments
        self.performance = data.performance
    }
}

class AddStaffViewModel: ObservableObject {
    @Published var firstName = ""
    @Published var lastName = ""
    @Published var email = ""
    @Published var phone = ""
    @Published var role = StaffRole.teacher
    @Published var department = ""
    @Published var position = ""
    @Published var hireDate = Date()
    @Published var isActive = true
    
    var isValid: Bool {
        !firstName.isEmpty && !lastName.isEmpty && !email.isEmpty
    }
    
    func saveStaff() async {
        // Implementation for saving staff
    }
}

// MARK: - Models

struct Staff: Identifiable, Codable {
    let id: UUID
    let firstName: String
    let lastName: String
    let email: String
    let phone: String
    let role: StaffRole
    let department: String
    let position: String
    let profileImage: String?
    let isActive: Bool
    let performanceScore: Int
    let hireDate: Date
}

struct StaffAssignment: Identifiable {
    let id: UUID
    let title: String
    let description: String
    let status: AssignmentStatus
    let dueDate: Date
    let assignedTo: UUID
}

struct StaffPerformance {
    let averageScore: Int
    let tasksCompleted: Int
    let studentSatisfaction: Int
    let attendance: Int
}

struct StaffData {
    let staff: [Staff]
    let assignments: [StaffAssignment]
    let performance: StaffPerformance
}

enum StaffRole: String, CaseIterable, Codable {
    case teacher = "teacher"
    case administrator = "administrator"
    case support = "support"
    case specialist = "specialist"
    
    var displayName: String {
        switch self {
        case .teacher: return "Teacher"
        case .administrator: return "Administrator"
        case .support: return "Support Staff"
        case .specialist: return "Specialist"
        }
    }
}

enum AssignmentStatus: String, CaseIterable {
    case active = "Active"
    case completed = "Completed"
    case pending = "Pending"
    case overdue = "Overdue"
}

#Preview {
    StaffView()
}