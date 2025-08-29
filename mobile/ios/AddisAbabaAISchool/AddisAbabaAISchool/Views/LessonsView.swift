import SwiftUI

struct LessonsView: View {
    @StateObject private var viewModel = LessonsViewModel()
    @State private var showingAddLesson = false
    @State private var selectedLesson: Lesson?
    @State private var selectedFilter: LessonFilter = .all
    
    var body: some View {
        NavigationView {
            VStack {
                // Filter Picker
                Picker("Filter", selection: $selectedFilter) {
                    ForEach(LessonFilter.allCases, id: \.self) { filter in
                        Text(filter.displayName).tag(filter)
                    }
                }
                .pickerStyle(SegmentedPickerStyle())
                .padding(.horizontal)
                
                // Lessons List
                List {
                    ForEach(viewModel.filteredLessons(filter: selectedFilter)) { lesson in
                        LessonRowView(lesson: lesson)
                            .onTapGesture {
                                selectedLesson = lesson
                            }
                    }
                }
                .refreshable {
                    await viewModel.loadLessons()
                }
            }
            .navigationTitle("Lessons")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: { showingAddLesson = true }) {
                        Image(systemName: "plus")
                    }
                }
            }
            .sheet(isPresented: $showingAddLesson) {
                AddLessonView()
            }
            .sheet(item: $selectedLesson) { lesson in
                LessonDetailView(lesson: lesson)
            }
        }
        .onAppear {
            Task {
                await viewModel.loadLessons()
            }
        }
    }
}

struct LessonRowView: View {
    let lesson: Lesson
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                VStack(alignment: .leading) {
                    Text(lesson.title)
                        .font(.headline)
                        .foregroundColor(.primary)
                    
                    Text(lesson.subject)
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
                
                VStack(alignment: .trailing) {
                    Text(lesson.grade)
                        .font(.caption)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 2)
                        .background(Color.blue.opacity(0.2))
                        .foregroundColor(.blue)
                        .clipShape(Capsule())
                    
                    Text("\(lesson.duration) min")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            
            Text(lesson.description)
                .font(.body)
                .foregroundColor(.secondary)
                .lineLimit(2)
            
            HStack {
                Text(lesson.status.rawValue)
                    .font(.caption)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 2)
                    .background(statusColor(for: lesson.status))
                    .foregroundColor(.white)
                    .clipShape(Capsule())
                
                Spacer()
                
                HStack(spacing: 4) {
                    Image(systemName: "person")
                        .font(.caption)
                    Text("\(lesson.enrolledStudents)")
                        .font(.caption)
                }
                .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
    
    private func statusColor(for status: LessonStatus) -> Color {
        switch status {
        case .active:
            return .green
        case .completed:
            return .blue
        case .upcoming:
            return .orange
        case .cancelled:
            return .red
        }
    }
}

struct LessonDetailView: View {
    let lesson: Lesson
    @StateObject private var viewModel = LessonDetailViewModel()
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            LessonInfoView(lesson: lesson)
                .tabItem {
                    Image(systemName: "info.circle")
                    Text("Info")
                }
                .tag(0)
            
            LessonMaterialsView(lesson: lesson)
                .tabItem {
                    Image(systemName: "doc.text")
                    Text("Materials")
                }
                .tag(1)
            
            LessonStudentsView(lesson: lesson)
                .tabItem {
                    Image(systemName: "person.3")
                    Text("Students")
                }
                .tag(2)
            
            LessonProgressView(lesson: lesson)
                .tabItem {
                    Image(systemName: "chart.bar")
                    Text("Progress")
                }
                .tag(3)
        }
        .navigationTitle(lesson.title)
        .navigationBarTitleDisplayMode(.inline)
        .onAppear {
            viewModel.loadLessonDetails(lesson)
        }
    }
}

struct LessonInfoView: View {
    let lesson: Lesson
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Lesson Header
                VStack(alignment: .leading, spacing: 12) {
                    Text(lesson.title)
                        .font(.title2)
                        .fontWeight(.bold)
                    
                    Text(lesson.subject)
                        .font(.title3)
                        .foregroundColor(.secondary)
                    
                    Text(lesson.description)
                        .font(.body)
                        .foregroundColor(.secondary)
                    
                    HStack {
                        Label("\(lesson.duration) min", systemImage: "clock")
                        Spacer()
                        Label(lesson.grade, systemImage: "graduationcap")
                        Spacer()
                        Label(lesson.status.rawValue, systemImage: "circle.fill")
                            .foregroundColor(statusColor(for: lesson.status))
                    }
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                }
                .padding()
                
                // Learning Objectives
                VStack(alignment: .leading, spacing: 12) {
                    Text("Learning Objectives")
                        .font(.headline)
                        .padding(.horizontal)
                    
                    ForEach(lesson.learningObjectives, id: \.self) { objective in
                        HStack {
                            Image(systemName: "checkmark.circle")
                                .foregroundColor(.green)
                            Text(objective)
                                .font(.body)
                            Spacer()
                        }
                        .padding(.horizontal)
                    }
                }
                
                // Schedule Information
                VStack(alignment: .leading, spacing: 15) {
                    Text("Schedule")
                        .font(.headline)
                        .padding(.horizontal)
                    
                    InfoRow(title: "Start Date", value: lesson.startDate, style: .date)
                    InfoRow(title: "End Date", value: lesson.endDate, style: .date)
                    InfoRow(title: "Schedule", value: lesson.schedule)
                    InfoRow(title: "Location", value: lesson.location)
                }
            }
        }
    }
    
    private func statusColor(for status: LessonStatus) -> Color {
        switch status {
        case .active:
            return .green
        case .completed:
            return .blue
        case .upcoming:
            return .orange
        case .cancelled:
            return .red
        }
    }
}

struct LessonMaterialsView: View {
    let lesson: Lesson
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text("Lesson Materials")
                    .font(.headline)
                    .padding()
                
                if lesson.materials.isEmpty {
                    Text("No materials available")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                        .frame(maxWidth: .infinity, alignment: .center)
                        .padding()
                } else {
                    ForEach(lesson.materials, id: \.self) { material in
                        MaterialRow(material: material)
                    }
                }
            }
        }
    }
}

struct MaterialRow: View {
    let material: String
    
    var body: some View {
        HStack {
            Image(systemName: "doc.text")
                .foregroundColor(.blue)
                .frame(width: 24, height: 24)
            
            VStack(alignment: .leading, spacing: 2) {
                Text(material)
                    .font(.subheadline)
                    .fontWeight(.medium)
                
                Text("Document")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            Button("Download") {
                // Implementation for downloading material
            }
            .font(.caption)
            .foregroundColor(.blue)
        }
        .padding(.horizontal)
        .padding(.vertical, 8)
    }
}

struct LessonStudentsView: View {
    let lesson: Lesson
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text("Enrolled Students")
                    .font(.headline)
                    .padding()
                
                // Placeholder for enrolled students
                Text("\(lesson.enrolledStudents) students enrolled")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity, alignment: .center)
                    .padding()
            }
        }
    }
}

struct LessonProgressView: View {
    let lesson: Lesson
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text("Lesson Progress")
                    .font(.headline)
                    .padding()
                
                // Progress Overview
                VStack(spacing: 16) {
                    ProgressCard(title: "Completion", value: 75, total: 100, icon: "checkmark.circle.fill")
                    ProgressCard(title: "Attendance", value: 85, total: 100, icon: "person.2.fill")
                    ProgressCard(title: "Engagement", value: 90, total: 100, icon: "brain.head.profile")
                }
                .padding(.horizontal)
            }
        }
    }
}

struct ProgressCard: View {
    let title: String
    let value: Int
    let total: Int
    let icon: String
    
    var progress: Double {
        Double(value) / Double(total)
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Image(systemName: icon)
                    .foregroundColor(.blue)
                
                Text(title)
                    .font(.subheadline)
                    .fontWeight(.medium)
                
                Spacer()
                
                Text("\(value)%")
                    .font(.subheadline)
                    .fontWeight(.semibold)
            }
            
            ProgressView(value: progress)
                .progressViewStyle(LinearProgressViewStyle(tint: .blue))
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(8)
        .shadow(color: .black.opacity(0.1), radius: 1, x: 0, y: 1)
    }
}

struct AddLessonView: View {
    @Environment(\.dismiss) private var dismiss
    @StateObject private var viewModel = AddLessonViewModel()
    
    var body: some View {
        NavigationView {
            Form {
                Section("Lesson Details") {
                    TextField("Title", text: $viewModel.title)
                    TextField("Subject", text: $viewModel.subject)
                    TextField("Description", text: $viewModel.description, axis: .vertical)
                        .lineLimit(3...6)
                    TextField("Grade", text: $viewModel.grade)
                }
                
                Section("Schedule") {
                    DatePicker("Start Date", selection: $viewModel.startDate, displayedComponents: .date)
                    DatePicker("End Date", selection: $viewModel.endDate, displayedComponents: .date)
                    TextField("Schedule", text: $viewModel.schedule)
                    TextField("Location", text: $viewModel.location)
                }
                
                Section("Settings") {
                    HStack {
                        Text("Duration (minutes)")
                        Spacer()
                        TextField("Duration", value: $viewModel.duration, format: .number)
                            .keyboardType(.numberPad)
                            .multilineTextAlignment(.trailing)
                    }
                    
                    Picker("Status", selection: $viewModel.status) {
                        ForEach(LessonStatus.allCases, id: \.self) { status in
                            Text(status.rawValue).tag(status)
                        }
                    }
                }
                
                Section("Learning Objectives") {
                    ForEach(viewModel.objectives.indices, id: \.self) { index in
                        TextField("Objective \(index + 1)", text: $viewModel.objectives[index])
                    }
                    .onDelete(perform: deleteObjective)
                    
                    Button("Add Objective") {
                        viewModel.objectives.append("")
                    }
                }
            }
            .navigationTitle("Add Lesson")
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
                            await viewModel.createLesson()
                            dismiss()
                        }
                    }
                    .disabled(!viewModel.isValid)
                }
            }
        }
    }
    
    private func deleteObjective(offsets: IndexSet) {
        viewModel.objectives.remove(atOffsets: offsets)
    }
}

// MARK: - View Models

class LessonsViewModel: ObservableObject {
    @Published var lessons: [Lesson] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    func loadLessons() async {
        await MainActor.run {
            isLoading = true
        }
        
        do {
            let loadedLessons = try await NetworkService.shared.fetchLessons()
            await MainActor.run {
                self.lessons = loadedLessons
                self.isLoading = false
            }
        } catch {
            await MainActor.run {
                self.errorMessage = error.localizedDescription
                self.isLoading = false
            }
        }
    }
    
    func filteredLessons(filter: LessonFilter) -> [Lesson] {
        switch filter {
        case .all:
            return lessons
        case .active:
            return lessons.filter { $0.status == .active }
        case .completed:
            return lessons.filter { $0.status == .completed }
        case .upcoming:
            return lessons.filter { $0.status == .upcoming }
        }
    }
}

class LessonDetailViewModel: ObservableObject {
    @Published var lesson: Lesson?
    @Published var isLoading = false
    
    func loadLessonDetails(_ lesson: Lesson) {
        self.lesson = lesson
    }
}

class AddLessonViewModel: ObservableObject {
    @Published var title = ""
    @Published var subject = ""
    @Published var description = ""
    @Published var grade = ""
    @Published var startDate = Date()
    @Published var endDate = Date().addingTimeInterval(86400 * 7) // 7 days later
    @Published var schedule = ""
    @Published var location = ""
    @Published var duration = 60
    @Published var status = LessonStatus.upcoming
    @Published var objectives: [String] = [""]
    
    var isValid: Bool {
        !title.isEmpty && !subject.isEmpty && !description.isEmpty && !grade.isEmpty
    }
    
    func createLesson() async {
        // Implementation for creating lesson
    }
}

// MARK: - Models

struct Lesson: Identifiable, Codable {
    let id: UUID
    let title: String
    let subject: String
    let description: String
    let grade: String
    let duration: Int
    let startDate: Date
    let endDate: Date
    let schedule: String
    let location: String
    let status: LessonStatus
    let learningObjectives: [String]
    let materials: [String]
    let enrolledStudents: Int
    let createdAt: Date
}

enum LessonStatus: String, CaseIterable, Codable {
    case active = "Active"
    case completed = "Completed"
    case upcoming = "Upcoming"
    case cancelled = "Cancelled"
}

enum LessonFilter: CaseIterable {
    case all, active, completed, upcoming
    
    var displayName: String {
        switch self {
        case .all: return "All"
        case .active: return "Active"
        case .completed: return "Completed"
        case .upcoming: return "Upcoming"
        }
    }
}

#Preview {
    LessonsView()
}