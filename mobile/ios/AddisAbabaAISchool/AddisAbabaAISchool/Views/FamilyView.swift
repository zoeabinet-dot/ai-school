import SwiftUI

struct FamilyView: View {
    @StateObject private var viewModel = FamilyViewModel()
    @State private var showingAddFamily = false
    @State private var selectedFamily: Family?
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Family Overview
                    FamilyOverviewCard(family: viewModel.currentFamily)
                    
                    // Family Members
                    FamilyMembersCard(members: viewModel.familyMembers)
                    
                    // Student Connections
                    StudentConnectionsCard(students: viewModel.connectedStudents)
                    
                    // Recent Communications
                    CommunicationsCard(communications: viewModel.recentCommunications)
                    
                    // Family Activities
                    ActivitiesCard(activities: viewModel.recentActivities)
                }
                .padding()
            }
            .navigationTitle("Family")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: { showingAddFamily = true }) {
                        Image(systemName: "plus")
                    }
                }
            }
            .sheet(isPresented: $showingAddFamily) {
                AddFamilyView()
            }
            .sheet(item: $selectedFamily) { family in
                FamilyDetailView(family: family)
            }
        }
        .onAppear {
            Task {
                await viewModel.loadFamilyData()
            }
        }
    }
}

struct FamilyOverviewCard: View {
    let family: Family?
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                VStack(alignment: .leading) {
                    Text("Family Overview")
                        .font(.headline)
                    Text(family?.name ?? "No family selected")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
                
                if let family = family {
                    Text("\(family.memberCount) members")
                        .font(.caption)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 2)
                        .background(Color.blue.opacity(0.2))
                        .foregroundColor(.blue)
                        .clipShape(Capsule())
                }
            }
            
            if let family = family {
                HStack {
                    Label("\(family.studentCount) students", systemImage: "graduationcap")
                    Spacer()
                    Label("\(family.activeMembers) active", systemImage: "person.2")
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

struct FamilyMembersCard: View {
    let members: [FamilyMember]
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Family Members")
                .font(.headline)
            
            if members.isEmpty {
                Text("No family members")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity, alignment: .center)
                    .padding()
            } else {
                ForEach(members) { member in
                    FamilyMemberRow(member: member)
                }
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 2, x: 0, y: 1)
    }
}

struct FamilyMemberRow: View {
    let member: FamilyMember
    
    var body: some View {
        HStack {
            // Member Avatar
            AsyncImage(url: URL(string: member.profileImage ?? "")) { image in
                image
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } placeholder: {
                Image(systemName: "person.circle.fill")
                    .foregroundColor(.gray)
            }
            .frame(width: 40, height: 40)
            .clipShape(Circle())
            
            VStack(alignment: .leading, spacing: 2) {
                Text("\(member.firstName) \(member.lastName)")
                    .font(.subheadline)
                    .fontWeight(.medium)
                
                Text(member.relationship.rawValue)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            VStack(alignment: .trailing, spacing: 2) {
                Text(member.isActive ? "Active" : "Inactive")
                    .font(.caption)
                    .padding(.horizontal, 6)
                    .padding(.vertical, 2)
                    .background(member.isActive ? Color.green.opacity(0.2) : Color.gray.opacity(0.2))
                    .foregroundColor(member.isActive ? .green : .gray)
                    .clipShape(Capsule())
                
                Text(member.lastActive, style: .relative)
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
}

struct StudentConnectionsCard: View {
    let students: [Student]
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Connected Students")
                .font(.headline)
            
            if students.isEmpty {
                Text("No students connected")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity, alignment: .center)
                    .padding()
            } else {
                ForEach(students) { student in
                    StudentConnectionRow(student: student)
                }
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 2, x: 0, y: 1)
    }
}

struct StudentConnectionRow: View {
    let student: Student
    
    var body: some View {
        HStack {
            // Student Avatar
            AsyncImage(url: URL(string: student.profileImage ?? "")) { image in
                image
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } placeholder: {
                Image(systemName: "person.circle.fill")
                    .foregroundColor(.gray)
            }
            .frame(width: 40, height: 40)
            .clipShape(Circle())
            
            VStack(alignment: .leading, spacing: 2) {
                Text("\(student.firstName) \(student.lastName)")
                    .font(.subheadline)
                    .fontWeight(.medium)
                
                Text("Grade \(student.grade)")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            VStack(alignment: .trailing, spacing: 2) {
                Text("\(student.averageScore)%")
                    .font(.subheadline)
                    .fontWeight(.semibold)
                
                Text("Average Score")
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
}

struct CommunicationsCard: View {
    let communications: [FamilyCommunication]
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Recent Communications")
                .font(.headline)
            
            if communications.isEmpty {
                Text("No recent communications")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity, alignment: .center)
                    .padding()
            } else {
                ForEach(communications.prefix(3)) { communication in
                    CommunicationRow(communication: communication)
                }
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 2, x: 0, y: 1)
    }
}

struct CommunicationRow: View {
    let communication: FamilyCommunication
    
    var body: some View {
        HStack {
            Image(systemName: communication.type.icon)
                .foregroundColor(communication.type.color)
                .frame(width: 24, height: 24)
            
            VStack(alignment: .leading, spacing: 2) {
                Text(communication.title)
                    .font(.subheadline)
                    .fontWeight(.medium)
                
                Text(communication.description)
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .lineLimit(2)
            }
            
            Spacer()
            
            Text(communication.date, style: .relative)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding(.vertical, 4)
    }
}

struct ActivitiesCard: View {
    let activities: [FamilyActivity]
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Recent Activities")
                .font(.headline)
            
            if activities.isEmpty {
                Text("No recent activities")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity, alignment: .center)
                    .padding()
            } else {
                ForEach(activities.prefix(3)) { activity in
                    ActivityRow(activity: activity)
                }
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 2, x: 0, y: 1)
    }
}

struct ActivityRow: View {
    let activity: FamilyActivity
    
    var body: some View {
        HStack {
            Image(systemName: activity.icon)
                .foregroundColor(.blue)
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
            
            Text(activity.date, style: .relative)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding(.vertical, 4)
    }
}

struct AddFamilyView: View {
    @Environment(\.dismiss) private var dismiss
    @StateObject private var viewModel = AddFamilyViewModel()
    
    var body: some View {
        NavigationView {
            Form {
                Section("Family Information") {
                    TextField("Family Name", text: $viewModel.familyName)
                    TextField("Address", text: $viewModel.address)
                    TextField("Phone", text: $viewModel.phone)
                        .keyboardType(.phonePad)
                    TextField("Email", text: $viewModel.email)
                        .keyboardType(.emailAddress)
                }
                
                Section("Primary Contact") {
                    TextField("Primary Contact Name", text: $viewModel.primaryContactName)
                    TextField("Primary Contact Phone", text: $viewModel.primaryContactPhone)
                        .keyboardType(.phonePad)
                    TextField("Primary Contact Email", text: $viewModel.primaryContactEmail)
                        .keyboardType(.emailAddress)
                }
            }
            .navigationTitle("Add Family")
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
                            await viewModel.saveFamily()
                            dismiss()
                        }
                    }
                    .disabled(!viewModel.isValid)
                }
            }
        }
    }
}

struct FamilyDetailView: View {
    let family: Family
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            FamilyInfoView(family: family)
                .tabItem {
                    Image(systemName: "person.3")
                    Text("Info")
                }
                .tag(0)
            
            FamilyMembersView(family: family)
                .tabItem {
                    Image(systemName: "person.2")
                    Text("Members")
                }
                .tag(1)
            
            FamilyStudentsView(family: family)
                .tabItem {
                    Image(systemName: "graduationcap")
                    Text("Students")
                }
                .tag(2)
        }
        .navigationTitle(family.name)
        .navigationBarTitleDisplayMode(.inline)
    }
}

struct FamilyInfoView: View {
    let family: Family
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Family Header
                VStack(alignment: .leading, spacing: 12) {
                    Text(family.name)
                        .font(.title2)
                        .fontWeight(.bold)
                    
                    HStack {
                        Label("\(family.memberCount) members", systemImage: "person.2")
                        Spacer()
                        Label("\(family.studentCount) students", systemImage: "graduationcap")
                    }
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                }
                .padding()
                
                // Contact Information
                VStack(alignment: .leading, spacing: 15) {
                    Text("Contact Information")
                        .font(.headline)
                        .padding(.horizontal)
                    
                    InfoRow(title: "Address", value: family.address)
                    InfoRow(title: "Phone", value: family.phone)
                    InfoRow(title: "Email", value: family.email)
                }
            }
        }
    }
}

struct FamilyMembersView: View {
    let family: Family
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text("Family Members")
                    .font(.headline)
                    .padding()
                
                // Placeholder for family members
                Text("Family members will be displayed here")
                    .foregroundColor(.secondary)
                    .padding()
            }
        }
    }
}

struct FamilyStudentsView: View {
    let family: Family
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text("Connected Students")
                    .font(.headline)
                    .padding()
                
                // Placeholder for connected students
                Text("Connected students will be displayed here")
                    .foregroundColor(.secondary)
                    .padding()
            }
        }
    }
}

// MARK: - View Models

class FamilyViewModel: ObservableObject {
    @Published var currentFamily: Family?
    @Published var familyMembers: [FamilyMember] = []
    @Published var connectedStudents: [Student] = []
    @Published var recentCommunications: [FamilyCommunication] = []
    @Published var recentActivities: [FamilyActivity] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    func loadFamilyData() async {
        await MainActor.run {
            isLoading = true
        }
        
        do {
            let familyData = try await NetworkService.shared.fetchFamilyData()
            await MainActor.run {
                self.updateFamilyData(with: familyData)
                self.isLoading = false
            }
        } catch {
            await MainActor.run {
                self.errorMessage = error.localizedDescription
                self.isLoading = false
            }
        }
    }
    
    private func updateFamilyData(with data: FamilyData) {
        self.currentFamily = data.family
        self.familyMembers = data.members
        self.connectedStudents = data.students
        self.recentCommunications = data.communications
        self.recentActivities = data.activities
    }
}

class AddFamilyViewModel: ObservableObject {
    @Published var familyName = ""
    @Published var address = ""
    @Published var phone = ""
    @Published var email = ""
    @Published var primaryContactName = ""
    @Published var primaryContactPhone = ""
    @Published var primaryContactEmail = ""
    
    var isValid: Bool {
        !familyName.isEmpty && !primaryContactName.isEmpty && !primaryContactPhone.isEmpty
    }
    
    func saveFamily() async {
        // Implementation for saving family
    }
}

// MARK: - Models

struct Family: Identifiable, Codable {
    let id: UUID
    let name: String
    let address: String
    let phone: String
    let email: String
    let memberCount: Int
    let studentCount: Int
    let activeMembers: Int
}

struct FamilyMember: Identifiable, Codable {
    let id: UUID
    let firstName: String
    let lastName: String
    let relationship: FamilyRelationship
    let profileImage: String?
    let isActive: Bool
    let lastActive: Date
}

struct FamilyCommunication: Identifiable {
    let id: UUID
    let title: String
    let description: String
    let type: CommunicationType
    let date: Date
}

struct FamilyActivity: Identifiable {
    let id: UUID
    let title: String
    let description: String
    let icon: String
    let date: Date
}

struct FamilyData {
    let family: Family
    let members: [FamilyMember]
    let students: [Student]
    let communications: [FamilyCommunication]
    let activities: [FamilyActivity]
}

enum FamilyRelationship: String, CaseIterable, Codable {
    case parent = "Parent"
    case guardian = "Guardian"
    case sibling = "Sibling"
    case other = "Other"
}

enum CommunicationType: CaseIterable {
    case message, notification, report, alert
    
    var icon: String {
        switch self {
        case .message: return "message"
        case .notification: return "bell"
        case .report: return "doc.text"
        case .alert: return "exclamationmark.triangle"
        }
    }
    
    var color: Color {
        switch self {
        case .message: return .blue
        case .notification: return .orange
        case .report: return .green
        case .alert: return .red
        }
    }
}

#Preview {
    FamilyView()
}