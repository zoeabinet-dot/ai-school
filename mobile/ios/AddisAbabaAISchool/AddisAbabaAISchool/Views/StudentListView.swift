import SwiftUI

struct StudentListView: View {
    @StateObject private var viewModel = StudentListViewModel()
    @State private var searchText = ""
    @State private var showingAddStudent = false
    @State private var selectedStudent: Student?
    
    var body: some View {
        NavigationView {
            VStack {
                // Search Bar
                SearchBar(text: $searchText)
                    .padding(.horizontal)
                
                // Student List
                List {
                    ForEach(viewModel.filteredStudents(searchText: searchText)) { student in
                        StudentRowView(student: student)
                            .onTapGesture {
                                selectedStudent = student
                            }
                    }
                    .onDelete(perform: deleteStudent)
                }
                .refreshable {
                    await viewModel.loadStudents()
                }
            }
            .navigationTitle("Students")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: { showingAddStudent = true }) {
                        Image(systemName: "plus")
                    }
                }
            }
            .sheet(isPresented: $showingAddStudent) {
                AddStudentView()
            }
            .sheet(item: $selectedStudent) { student in
                StudentDetailView(student: student)
            }
        }
        .onAppear {
            Task {
                await viewModel.loadStudents()
            }
        }
    }
    
    private func deleteStudent(offsets: IndexSet) {
        viewModel.deleteStudents(at: offsets)
    }
}

struct StudentRowView: View {
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
            .frame(width: 50, height: 50)
            .clipShape(Circle())
            
            VStack(alignment: .leading, spacing: 4) {
                Text("\(student.firstName) \(student.lastName)")
                    .font(.headline)
                    .foregroundColor(.primary)
                
                Text(student.grade)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                
                HStack {
                    Text("Age: \(student.age)")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    
                    Spacer()
                    
                    Text(student.status.rawValue)
                        .font(.caption)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 2)
                        .background(statusColor(for: student.status))
                        .foregroundColor(.white)
                        .clipShape(Capsule())
                }
            }
            
            Spacer()
            
            Image(systemName: "chevron.right")
                .foregroundColor(.gray)
        }
        .padding(.vertical, 4)
    }
    
    private func statusColor(for status: StudentStatus) -> Color {
        switch status {
        case .active:
            return .green
        case .inactive:
            return .red
        case .pending:
            return .orange
        }
    }
}

struct SearchBar: View {
    @Binding var text: String
    
    var body: some View {
        HStack {
            Image(systemName: "magnifyingglass")
                .foregroundColor(.gray)
            
            TextField("Search students...", text: $text)
                .textFieldStyle(RoundedBorderTextFieldStyle())
        }
    }
}

class StudentListViewModel: ObservableObject {
    @Published var students: [Student] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    func loadStudents() async {
        await MainActor.run {
            isLoading = true
        }
        
        do {
            let loadedStudents = try await NetworkService.shared.fetchStudents()
            await MainActor.run {
                self.students = loadedStudents
                self.isLoading = false
            }
        } catch {
            await MainActor.run {
                self.errorMessage = error.localizedDescription
                self.isLoading = false
            }
        }
    }
    
    func filteredStudents(searchText: String) -> [Student] {
        if searchText.isEmpty {
            return students
        }
        return students.filter { student in
            student.firstName.localizedCaseInsensitiveContains(searchText) ||
            student.lastName.localizedCaseInsensitiveContains(searchText) ||
            student.grade.localizedCaseInsensitiveContains(searchText)
        }
    }
    
    func deleteStudents(at offsets: IndexSet) {
        // Implementation for deleting students
        students.remove(atOffsets: offsets)
    }
}

struct AddStudentView: View {
    @Environment(\.dismiss) private var dismiss
    @StateObject private var viewModel = AddStudentViewModel()
    
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
                
                Section("Academic Information") {
                    TextField("Grade", text: $viewModel.grade)
                    TextField("Age", text: $viewModel.age)
                        .keyboardType(.numberPad)
                }
                
                Section("Address") {
                    TextField("Address", text: $viewModel.address)
                    TextField("City", text: $viewModel.city)
                }
            }
            .navigationTitle("Add Student")
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
                            await viewModel.saveStudent()
                            dismiss()
                        }
                    }
                    .disabled(!viewModel.isValid)
                }
            }
        }
    }
}

class AddStudentViewModel: ObservableObject {
    @Published var firstName = ""
    @Published var lastName = ""
    @Published var email = ""
    @Published var phone = ""
    @Published var grade = ""
    @Published var age = ""
    @Published var address = ""
    @Published var city = ""
    
    var isValid: Bool {
        !firstName.isEmpty && !lastName.isEmpty && !email.isEmpty
    }
    
    func saveStudent() async {
        // Implementation for saving student
    }
}

struct StudentDetailView: View {
    let student: Student
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            StudentInfoView(student: student)
                .tabItem {
                    Image(systemName: "person")
                    Text("Info")
                }
                .tag(0)
            
            StudentAcademicView(student: student)
                .tabItem {
                    Image(systemName: "book")
                    Text("Academic")
                }
                .tag(1)
            
            StudentProjectsView(student: student)
                .tabItem {
                    Image(systemName: "folder")
                    Text("Projects")
                }
                .tag(2)
        }
        .navigationTitle("\(student.firstName) \(student.lastName)")
        .navigationBarTitleDisplayMode(.inline)
    }
}

struct StudentInfoView: View {
    let student: Student
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Profile Header
                HStack {
                    AsyncImage(url: URL(string: student.profileImage ?? "")) { image in
                        image
                            .resizable()
                            .aspectRatio(contentMode: .fill)
                    } placeholder: {
                        Image(systemName: "person.circle.fill")
                            .foregroundColor(.gray)
                    }
                    .frame(width: 100, height: 100)
                    .clipShape(Circle())
                    
                    VStack(alignment: .leading) {
                        Text("\(student.firstName) \(student.lastName)")
                            .font(.title2)
                            .fontWeight(.bold)
                        
                        Text(student.grade)
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                        
                        Text("Age: \(student.age)")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    
                    Spacer()
                }
                .padding()
                
                // Personal Information
                VStack(alignment: .leading, spacing: 15) {
                    Text("Personal Information")
                        .font(.headline)
                        .padding(.horizontal)
                    
                    InfoRow(title: "Email", value: student.email)
                    InfoRow(title: "Phone", value: student.phone)
                    InfoRow(title: "Address", value: student.address)
                    InfoRow(title: "City", value: student.city)
                    InfoRow(title: "Status", value: student.status.rawValue)
                }
            }
        }
    }
}

struct InfoRow: View {
    let title: String
    let value: String
    
    var body: some View {
        HStack {
            Text(title)
                .font(.subheadline)
                .foregroundColor(.secondary)
                .frame(width: 80, alignment: .leading)
            
            Text(value)
                .font(.subheadline)
            
            Spacer()
        }
        .padding(.horizontal)
    }
}

struct StudentAcademicView: View {
    let student: Student
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text("Academic Records")
                    .font(.headline)
                    .padding()
                
                // Placeholder for academic records
                Text("Academic records will be displayed here")
                    .foregroundColor(.secondary)
                    .padding()
            }
        }
    }
}

struct StudentProjectsView: View {
    let student: Student
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text("Student Projects")
                    .font(.headline)
                    .padding()
                
                // Placeholder for student projects
                Text("Student projects will be displayed here")
                    .foregroundColor(.secondary)
                    .padding()
            }
        }
    }
}

#Preview {
    StudentListView()
}