import SwiftUI
import AVFoundation

struct AILessonView: View {
    @StateObject private var viewModel = AILessonViewModel()
    @State private var selectedLesson: AILesson?
    @State private var showingNewLesson = false
    
    var body: some View {
        NavigationView {
            VStack {
                // AI Lesson List
                List {
                    ForEach(viewModel.lessons) { lesson in
                        AILessonRowView(lesson: lesson)
                            .onTapGesture {
                                selectedLesson = lesson
                            }
                    }
                }
                .refreshable {
                    await viewModel.loadLessons()
                }
            }
            .navigationTitle("AI Lessons")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: { showingNewLesson = true }) {
                        Image(systemName: "plus")
                    }
                }
            }
            .sheet(isPresented: $showingNewLesson) {
                NewAILessonView()
            }
            .sheet(item: $selectedLesson) { lesson in
                AILessonDetailView(lesson: lesson)
            }
        }
        .onAppear {
            Task {
                await viewModel.loadLessons()
            }
        }
    }
}

struct AILessonRowView: View {
    let lesson: AILesson
    
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
                    Text(lesson.difficultyLevel.rawValue)
                        .font(.caption)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 2)
                        .background(difficultyColor(for: lesson.difficultyLevel))
                        .foregroundColor(.white)
                        .clipShape(Capsule())
                    
                    Text("\(lesson.estimatedDuration) min")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            
            Text(lesson.description)
                .font(.body)
                .foregroundColor(.secondary)
                .lineLimit(2)
            
            HStack {
                Text("AI Generated")
                    .font(.caption)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 2)
                    .background(Color.blue.opacity(0.2))
                    .foregroundColor(.blue)
                    .clipShape(Capsule())
                
                Spacer()
                
                if lesson.isCompleted {
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundColor(.green)
                }
            }
        }
        .padding(.vertical, 4)
    }
    
    private func difficultyColor(for level: DifficultyLevel) -> Color {
        switch level {
        case .beginner:
            return .green
        case .intermediate:
            return .orange
        case .advanced:
            return .red
        }
    }
}

struct AILessonDetailView: View {
    let lesson: AILesson
    @StateObject private var viewModel = AILessonDetailViewModel()
    @State private var showingConversation = false
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Lesson Header
                VStack(alignment: .leading, spacing: 12) {
                    Text(lesson.title)
                        .font(.title)
                        .fontWeight(.bold)
                    
                    Text(lesson.subject)
                        .font(.title2)
                        .foregroundColor(.secondary)
                    
                    Text(lesson.description)
                        .font(.body)
                        .foregroundColor(.secondary)
                    
                    HStack {
                        Label("\(lesson.estimatedDuration) min", systemImage: "clock")
                        Spacer()
                        Label(lesson.difficultyLevel.rawValue, systemImage: "star")
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
                
                // Start Lesson Button
                Button(action: {
                    showingConversation = true
                }) {
                    HStack {
                        Image(systemName: "play.circle.fill")
                        Text("Start AI Lesson")
                            .fontWeight(.semibold)
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                }
                .padding(.horizontal)
                
                // Lesson Materials
                if !lesson.materials.isEmpty {
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Lesson Materials")
                            .font(.headline)
                            .padding(.horizontal)
                        
                        ForEach(lesson.materials, id: \.self) { material in
                            HStack {
                                Image(systemName: "doc.text")
                                    .foregroundColor(.blue)
                                Text(material)
                                    .font(.body)
                                Spacer()
                            }
                            .padding(.horizontal)
                        }
                    }
                }
            }
        }
        .navigationTitle("AI Lesson")
        .navigationBarTitleDisplayMode(.inline)
        .sheet(isPresented: $showingConversation) {
            AIConversationView(lesson: lesson)
        }
    }
}

struct AIConversationView: View {
    let lesson: AILesson
    @StateObject private var viewModel = AIConversationViewModel()
    @State private var messageText = ""
    @State private var isRecording = false
    @Environment(\.dismiss) private var dismiss
    
    var body: some View {
        NavigationView {
            VStack {
                // Messages
                ScrollViewReader { proxy in
                    ScrollView {
                        LazyVStack(spacing: 12) {
                            ForEach(viewModel.messages) { message in
                                MessageBubble(message: message)
                                    .id(message.id)
                            }
                        }
                        .padding()
                    }
                    .onChange(of: viewModel.messages.count) { _ in
                        if let lastMessage = viewModel.messages.last {
                            withAnimation {
                                proxy.scrollTo(lastMessage.id, anchor: .bottom)
                            }
                        }
                    }
                }
                
                // Input Area
                HStack {
                    // Voice Recording Button
                    Button(action: {
                        if isRecording {
                            viewModel.stopRecording()
                        } else {
                            viewModel.startRecording()
                        }
                        isRecording.toggle()
                    }) {
                        Image(systemName: isRecording ? "stop.circle.fill" : "mic.circle.fill")
                            .font(.title2)
                            .foregroundColor(isRecording ? .red : .blue)
                    }
                    
                    // Text Input
                    TextField("Type your message...", text: $messageText)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                    
                    // Send Button
                    Button(action: {
                        guard !messageText.isEmpty else { return }
                        viewModel.sendMessage(messageText)
                        messageText = ""
                    }) {
                        Image(systemName: "paperplane.circle.fill")
                            .font(.title2)
                            .foregroundColor(.blue)
                    }
                    .disabled(messageText.isEmpty)
                }
                .padding()
            }
            .navigationTitle("AI Conversation")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
        }
        .onAppear {
            viewModel.startConversation(for: lesson)
        }
    }
}

struct MessageBubble: View {
    let message: ConversationMessage
    
    var body: some View {
        HStack {
            if message.isFromUser {
                Spacer()
            }
            
            VStack(alignment: message.isFromUser ? .trailing : .leading, spacing: 4) {
                Text(message.content)
                    .padding(.horizontal, 16)
                    .padding(.vertical, 10)
                    .background(message.isFromUser ? Color.blue : Color.gray.opacity(0.2))
                    .foregroundColor(message.isFromUser ? .white : .primary)
                    .cornerRadius(16)
                
                Text(message.timestamp, style: .time)
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }
            
            if !message.isFromUser {
                Spacer()
            }
        }
    }
}

struct NewAILessonView: View {
    @Environment(\.dismiss) private var dismiss
    @StateObject private var viewModel = NewAILessonViewModel()
    
    var body: some View {
        NavigationView {
            Form {
                Section("Lesson Details") {
                    TextField("Title", text: $viewModel.title)
                    TextField("Subject", text: $viewModel.subject)
                    TextField("Description", text: $viewModel.description, axis: .vertical)
                        .lineLimit(3...6)
                }
                
                Section("Settings") {
                    Picker("Difficulty Level", selection: $viewModel.difficultyLevel) {
                        ForEach(DifficultyLevel.allCases, id: \.self) { level in
                            Text(level.rawValue).tag(level)
                        }
                    }
                    
                    HStack {
                        Text("Duration (minutes)")
                        Spacer()
                        TextField("Duration", value: $viewModel.duration, format: .number)
                            .keyboardType(.numberPad)
                            .multilineTextAlignment(.trailing)
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
            .navigationTitle("New AI Lesson")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Create") {
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

class AILessonViewModel: ObservableObject {
    @Published var lessons: [AILesson] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    func loadLessons() async {
        await MainActor.run {
            isLoading = true
        }
        
        do {
            let loadedLessons = try await NetworkService.shared.fetchAILessons()
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
}

class AILessonDetailViewModel: ObservableObject {
    @Published var lesson: AILesson?
    @Published var isLoading = false
    
    func loadLessonDetails(_ lesson: AILesson) async {
        await MainActor.run {
            isLoading = true
        }
        
        // Implementation for loading lesson details
        await MainActor.run {
            self.lesson = lesson
            self.isLoading = false
        }
    }
}

class AIConversationViewModel: ObservableObject {
    @Published var messages: [ConversationMessage] = []
    @Published var isRecording = false
    private var audioRecorder: AVAudioRecorder?
    
    func startConversation(for lesson: AILesson) {
        // Add initial AI message
        let welcomeMessage = ConversationMessage(
            id: UUID(),
            content: "Hello! I'm your AI teacher. I'm here to help you learn about \(lesson.subject). What would you like to know?",
            isFromUser: false,
            timestamp: Date()
        )
        messages.append(welcomeMessage)
    }
    
    func sendMessage(_ text: String) {
        let userMessage = ConversationMessage(
            id: UUID(),
            content: text,
            isFromUser: true,
            timestamp: Date()
        )
        messages.append(userMessage)
        
        // Simulate AI response
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            let aiResponse = ConversationMessage(
                id: UUID(),
                content: "Thank you for your question about '\(text)'. Let me help you understand this better...",
                isFromUser: false,
                timestamp: Date()
            )
            self.messages.append(aiResponse)
        }
    }
    
    func startRecording() {
        // Implementation for voice recording
        isRecording = true
    }
    
    func stopRecording() {
        // Implementation for stopping voice recording
        isRecording = false
    }
}

class NewAILessonViewModel: ObservableObject {
    @Published var title = ""
    @Published var subject = ""
    @Published var description = ""
    @Published var difficultyLevel = DifficultyLevel.beginner
    @Published var duration = 30
    @Published var objectives: [String] = [""]
    
    var isValid: Bool {
        !title.isEmpty && !subject.isEmpty && !description.isEmpty && !objectives.allSatisfy { $0.isEmpty }
    }
    
    func createLesson() async {
        // Implementation for creating new AI lesson
    }
}

// MARK: - Models

struct AILesson: Identifiable, Codable {
    let id: UUID
    let title: String
    let subject: String
    let description: String
    let difficultyLevel: DifficultyLevel
    let estimatedDuration: Int
    let learningObjectives: [String]
    let materials: [String]
    let isCompleted: Bool
    let createdAt: Date
}

struct ConversationMessage: Identifiable {
    let id: UUID
    let content: String
    let isFromUser: Bool
    let timestamp: Date
}

enum DifficultyLevel: String, CaseIterable, Codable {
    case beginner = "Beginner"
    case intermediate = "Intermediate"
    case advanced = "Advanced"
}

#Preview {
    AILessonView()
}