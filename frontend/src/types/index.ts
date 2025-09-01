// User and Authentication Types
export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  is_active: boolean;
  date_joined: string;
  last_login: string;
  profile_image?: string;
  phone_number?: string;
  date_of_birth?: string;
  gender?: Gender;
  address?: Address;
  preferences?: UserPreferences;
  permissions: Permission[];
  metadata?: Record<string, any>;
}

export enum UserRole {
  STUDENT = 'student',
  FAMILY = 'family',
  STAFF = 'staff',
  ADMIN = 'admin',
  AI_TEACHER = 'ai_teacher'
}

export enum Gender {
  MALE = 'male',
  FEMALE = 'female',
  OTHER = 'other',
  PREFER_NOT_TO_SAY = 'prefer_not_to_say'
}

export enum Permission {
  VIEW_STUDENTS = 'view_students',
  EDIT_STUDENTS = 'edit_students',
  DELETE_STUDENTS = 'delete_students',
  VIEW_ANALYTICS = 'view_analytics',
  EDIT_ANALYTICS = 'edit_analytics',
  VIEW_MONITORING = 'view_monitoring',
  EDIT_MONITORING = 'edit_monitoring',
  VIEW_FAMILIES = 'view_families',
  EDIT_FAMILIES = 'edit_families',
  VIEW_STAFF = 'view_staff',
  EDIT_STAFF = 'edit_staff',
  VIEW_LESSONS = 'view_lessons',
  EDIT_LESSONS = 'edit_lessons',
  VIEW_AI_LESSONS = 'view_ai_lessons',
  EDIT_AI_LESSONS = 'edit_ai_lessons',
  ADMIN_ACCESS = 'admin_access'
}

export interface Address {
  street: string;
  city: string;
  state: string;
  postal_code: string;
  country: string;
  coordinates?: Coordinates;
}

export interface Coordinates {
  latitude: number;
  longitude: number;
}

export interface UserPreferences {
  notifications: NotificationPreferences;
  privacy: PrivacyPreferences;
  accessibility: AccessibilityPreferences;
  theme: ThemePreference;
  language: string;
  timezone: string;
}

export interface NotificationPreferences {
  email: boolean;
  push: boolean;
  sms: boolean;
  academic_updates: boolean;
  behavioral_alerts: boolean;
  general_announcements: boolean;
}

export interface PrivacyPreferences {
  profile_visibility: ProfileVisibility;
  academic_record_visibility: AcademicRecordVisibility;
  data_sharing: DataSharingPreferences;
}

export enum ProfileVisibility {
  PUBLIC = 'public',
  PRIVATE = 'private',
  FRIENDS_ONLY = 'friends_only'
}

export enum AcademicRecordVisibility {
  PUBLIC = 'public',
  PRIVATE = 'private',
  FAMILY_ONLY = 'family_only',
  STAFF_ONLY = 'staff_only'
}

export interface DataSharingPreferences {
  analytics: boolean;
  research: boolean;
  third_party: boolean;
  ai_training: boolean;
}

export interface AccessibilityPreferences {
  color_blindness: ColorBlindnessType;
  font_size: 'small' | 'medium' | 'large';
  high_contrast: boolean;
  screen_reader: boolean;
}

export enum ColorBlindnessType {
  NONE = 'none',
  PROTANOPIA = 'protanopia',
  DEUTERANOPIA = 'deuteranopia',
  TRITANOPIA = 'tritanopia'
}

export enum ThemePreference {
  LIGHT = 'light',
  DARK = 'dark',
  SYSTEM = 'system'
}

// Authentication Types
export interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface LoginCredentials {
  email: string;
  password: string;
  role: UserRole;
}

export interface RegisterData {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  phone_number?: string;
  date_of_birth?: string;
  gender?: Gender;
}

export interface AuthResponse {
  user: User;
  access: string;
  refresh: string;
}

// Student Types
export interface Student {
  id: number;
  user: User;
  student_id: string;
  grade_level: number;
  enrollment_date: string;
  graduation_date?: string;
  academic_status: AcademicStatus;
  learning_style: LearningStyle;
  special_needs?: string[];
  emergency_contact: EmergencyContact;
  academic_records: AcademicRecord[];
  projects: StudentProject[];
  learning_sessions: LearningSession[];
  goals: StudentGoal[];
}

export enum AcademicStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  GRADUATED = 'graduated',
  SUSPENDED = 'suspended',
  TRANSFERRED = 'transferred'
}

export interface LearningStyle {
  visual: number;
  auditory: number;
  kinesthetic: number;
  reading: number;
  social: number;
}

export interface EmergencyContact {
  name: string;
  relationship: string;
  phone: string;
  email: string;
  address: Address;
}

export interface AcademicRecord {
  id: number;
  student: number;
  subject: string;
  grade: string;
  score: number;
  semester: string;
  academic_year: string;
  teacher_notes?: string;
  created_at: string;
  updated_at: string;
}

export interface StudentProject {
  id: number;
  student: number;
  title: string;
  description: string;
  subject: string;
  project_type: ProjectType;
  status: ProjectStatus;
  start_date: string;
  due_date: string;
  completion_date?: string;
  grade?: string;
  feedback?: string;
  attachments: string[];
  created_at: string;
  updated_at: string;
}

export enum ProjectType {
  RESEARCH = 'research',
  PRESENTATION = 'presentation',
  EXPERIMENT = 'experiment',
  CREATIVE = 'creative',
  TECHNICAL = 'technical'
}

export enum ProjectStatus {
  NOT_STARTED = 'not_started',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  OVERDUE = 'overdue'
}

export interface LearningSession {
  id: number;
  student: number;
  session_type: SessionType;
  subject: string;
  duration: number;
  start_time: string;
  end_time: string;
  ai_teacher?: number;
  materials_used: string[];
  performance_score?: number;
  engagement_level: EngagementLevel;
  notes?: string;
  created_at: string;
}

export enum SessionType {
  AI_LESSON = 'ai_lesson',
  TRADITIONAL = 'traditional',
  GROUP = 'group',
  INDIVIDUAL = 'individual',
  ASSESSMENT = 'assessment'
}

export enum EngagementLevel {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  EXCELLENT = 'excellent'
}

export interface StudentGoal {
  id: number;
  student: number;
  title: string;
  description: string;
  goal_type: GoalType;
  target_date: string;
  status: GoalStatus;
  progress: number;
  milestones: GoalMilestone[];
  created_at: string;
  updated_at: string;
}

export enum GoalType {
  ACADEMIC = 'academic',
  BEHAVIORAL = 'behavioral',
  SOCIAL = 'social',
  PERSONAL = 'personal'
}

export enum GoalStatus {
  NOT_STARTED = 'not_started',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  OVERDUE = 'overdue'
}

export interface GoalMilestone {
  id: number;
  title: string;
  description: string;
  target_date: string;
  completed: boolean;
  completion_date?: string;
}

// AI Teacher Types
export interface AILesson {
  id: number;
  title: string;
  subject: string;
  grade_level: number;
  content: string;
  learning_objectives: string[];
  difficulty_level: DifficultyLevel;
  estimated_duration: number;
  ai_model_used: string;
  created_by: number;
  created_at: string;
  updated_at: string;
  tags: string[];
  metadata: Record<string, any>;
}

export enum DifficultyLevel {
  BEGINNER = 'beginner',
  INTERMEDIATE = 'intermediate',
  ADVANCED = 'advanced',
  EXPERT = 'expert'
}

export interface AIConversation {
  id: number;
  student: number;
  ai_teacher: number;
  subject: string;
  status: ConversationStatus;
  start_time: string;
  end_time?: string;
  messages: ConversationMessage[];
  summary?: string;
  created_at: string;
  updated_at: string;
}

export enum ConversationStatus {
  ACTIVE = 'active',
  PAUSED = 'paused',
  COMPLETED = 'completed',
  ARCHIVED = 'archived'
}

export interface ConversationMessage {
  id: number;
  conversation: number;
  sender_type: SenderType;
  sender_id: number;
  content: string;
  message_type: MessageType;
  timestamp: string;
  metadata?: Record<string, any>;
}

export enum SenderType {
  STUDENT = 'student',
  AI_TEACHER = 'ai_teacher',
  HUMAN_TEACHER = 'human_teacher'
}

export enum MessageType {
  TEXT = 'text',
  AUDIO = 'audio',
  IMAGE = 'image',
  VIDEO = 'video',
  FILE = 'file'
}

// Analytics Types
export interface LearningAnalytics {
  id: number;
  student: number;
  subject: string;
  time_period: string;
  metrics: AnalyticsMetrics;
  insights: string[];
  recommendations: string[];
  created_at: string;
  updated_at: string;
}

export interface AnalyticsMetrics {
  total_study_time: number;
  average_score: number;
  completion_rate: number;
  engagement_score: number;
  improvement_rate: number;
  attendance_rate: number;
  participation_score: number;
}

export interface PerformanceMetrics {
  id: number;
  student: number;
  subject: string;
  assessment_type: AssessmentType;
  score: number;
  max_score: number;
  percentage: number;
  grade: string;
  feedback: string;
  assessment_date: string;
  created_at: string;
}

export enum AssessmentType {
  QUIZ = 'quiz',
  TEST = 'test',
  EXAM = 'exam',
  PROJECT = 'project',
  PRESENTATION = 'presentation',
  ASSIGNMENT = 'assignment'
}

// Monitoring Types
export interface WebcamSession {
  id: number;
  student: number;
  start_time: string;
  end_time?: string;
  status: SessionStatus;
  privacy_settings: PrivacySettings;
  frames_analyzed: number;
  behavior_events: BehaviorEvent[];
  created_at: string;
}

export enum SessionStatus {
  ACTIVE = 'active',
  PAUSED = 'paused',
  COMPLETED = 'completed',
  ERROR = 'error'
}

export interface PrivacySettings {
  recording_enabled: boolean;
  face_detection: boolean;
  emotion_analysis: boolean;
  behavior_tracking: boolean;
  data_retention_days: number;
  consent_given: boolean;
  consent_date: string;
}

export interface BehaviorEvent {
  id: number;
  session: number;
  event_type: BehaviorEventType;
  timestamp: string;
  confidence: number;
  description: string;
  severity: AlertSeverity;
  metadata: Record<string, any>;
}

export enum BehaviorEventType {
  ATTENTION_LOSS = 'attention_loss',
  DISTRACTION = 'distraction',
  FRUSTRATION = 'frustration',
  ENGAGEMENT = 'engagement',
  SLEEPINESS = 'sleepiness',
  STRESS = 'stress'
}

export enum AlertSeverity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

// Family Types
export interface Family {
  id: number;
  family_name: string;
  primary_contact: User;
  members: FamilyMember[];
  students: FamilyStudent[];
  communications: FamilyCommunication[];
  notifications: FamilyNotification[];
  created_at: string;
  updated_at: string;
}

export interface FamilyMember {
  id: number;
  family: number;
  user: User;
  relationship: string;
  is_primary_contact: boolean;
  can_view_academic_records: boolean;
  can_receive_notifications: boolean;
  created_at: string;
}

export interface FamilyStudent {
  id: number;
  family: number;
  student: number;
  relationship: string;
  is_primary_guardian: boolean;
  created_at: string;
}

export interface FamilyCommunication {
  id: number;
  family: number;
  type: string;
  message: string;
  sent_at: string;
  metadata?: Record<string, any>;
}

export interface FamilyNotification {
  id: number;
  family: number;
  title: string;
  message: string;
  read: boolean;
  created_at: string;
}

// Staff Types
export interface Staff {
  id: number;
  user: User;
  employee_id: string;
  department: string;
  position: string;
  hire_date: string;
  salary?: number;
  supervisor?: number;
  assignments: StaffAssignment[];
  schedule: StaffSchedule[];
  performance: StaffPerformance[];
  created_at: string;
  updated_at: string;
}

export interface StaffAssignment {
  id: number;
  staff: number;
  assignment_type: AssignmentType;
  subject?: string;
  grade_level?: number;
  start_date: string;
  end_date?: string;
  status: AssignmentStatus;
  created_at: string;
}

export enum AssignmentType {
  TEACHING = 'teaching',
  ADMINISTRATION = 'administration',
  COUNSELING = 'counseling',
  SUPPORT = 'support'
}

export enum AssignmentStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  PENDING = 'pending',
  COMPLETED = 'completed'
}

export interface StaffSchedule {
  id: number;
  staff: number;
  day: string;
  start_time: string;
  end_time: string;
}

export interface StaffPerformance {
  id: number;
  staff: number;
  period: string;
  rating: number;
  notes?: string;
}

// Lesson Types
export interface Lesson {
  id: number;
  title: string;
  subject: string;
  grade_level: number;
  description: string;
  learning_objectives: string[];
  content: string;
  materials: LessonMaterial[];
  assessments: LessonAssessment[];
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface LessonMaterial {
  id: number;
  lesson: number;
  title: string;
  material_type: MaterialType;
  file_url: string;
  description?: string;
  created_at: string;
}

export enum MaterialType {
  DOCUMENT = 'document',
  VIDEO = 'video',
  AUDIO = 'audio',
  IMAGE = 'image',
  INTERACTIVE = 'interactive'
}

export interface LessonAssessment {
  id: number;
  lesson: number;
  title: string;
  assessment_type: AssessmentType;
  questions: AssessmentQuestion[];
  total_points: number;
  time_limit?: number;
  created_at: string;
}

export interface AssessmentQuestion {
  id: number;
  assessment: number;
  question_text: string;
  question_type: QuestionType;
  options?: string[];
  correct_answer?: string;
  points: number;
  created_at: string;
}

export enum QuestionType {
  MULTIPLE_CHOICE = 'multiple_choice',
  TRUE_FALSE = 'true_false',
  SHORT_ANSWER = 'short_answer',
  ESSAY = 'essay',
  MATCHING = 'matching'
}

// API Response Types
export interface ApiResponse<T> {
  data: T;
  message: string;
  success: boolean;
  errors?: string[];
}

export interface PaginatedResponse<T> {
  results: T[];
  count: number;
  next?: string;
  previous?: string;
}

// Dashboard Types
export interface DashboardData {
  user: User;
  quickStats: QuickStats;
  recentActivity: ActivityItem[];
  performanceData: PerformanceData;
  notifications: Notification[];
  upcomingEvents: Event[];
}

export interface QuickStats {
  totalStudents: number;
  activeLessons: number;
  aiSessions: number;
  attendance: number;
}

export interface ActivityItem {
  id: number;
  type: ActivityType;
  title: string;
  description: string;
  timestamp: string;
  user: User;
  metadata?: Record<string, any>;
}

export enum ActivityType {
  LOGIN = 'login',
  LESSON_COMPLETED = 'lesson_completed',
  ASSESSMENT_TAKEN = 'assessment_taken',
  PROJECT_SUBMITTED = 'project_submitted',
  GOAL_ACHIEVED = 'goal_achieved',
  BEHAVIOR_ALERT = 'behavior_alert'
}

export interface PerformanceData {
  labels: string[];
  datasets: PerformanceDataset[];
}

export interface PerformanceDataset {
  label: string;
  data: number[];
  borderColor: string;
  backgroundColor: string;
}

export interface Notification {
  id: number;
  user: number;
  title: string;
  message: string;
  type: NotificationType;
  read: boolean;
  created_at: string;
  action_url?: string;
}

export enum NotificationType {
  INFO = 'info',
  SUCCESS = 'success',
  WARNING = 'warning',
  ERROR = 'error',
  ALERT = 'alert'
}

export interface Event {
  id: number;
  title: string;
  description: string;
  start_date: string;
  end_date: string;
  event_type: EventType;
  location?: string;
  attendees: number[];
  created_at: string;
}

export enum EventType {
  CLASS = 'class',
  MEETING = 'meeting',
  EXAM = 'exam',
  HOLIDAY = 'holiday',
  ACTIVITY = 'activity'
}

// Real-time Communication Types
export interface ChatMessage {
  id: string;
  sender: User;
  content: string;
  message_type: MessageType;
  timestamp: string;
  read: boolean;
  metadata?: Record<string, any>;
}

export interface ChatRoom {
  id: string;
  name: string;
  participants: User[];
  messages: ChatMessage[];
  last_message?: ChatMessage;
  unread_count: number;
  created_at: string;
  updated_at: string;
}

// AI/ML Types
export interface AIModel {
  id: string;
  name: string;
  type: ModelType;
  version: string;
  status: ModelStatus;
  accuracy: number;
  last_updated: string;
  metadata: Record<string, any>;
}

export enum ModelType {
  PERFORMANCE_PREDICTION = 'performance_prediction',
  EMOTION_RECOGNITION = 'emotion_recognition',
  CONTENT_GENERATION = 'content_generation',
  RISK_ASSESSMENT = 'risk_assessment',
  ADAPTIVE_LEARNING = 'adaptive_learning'
}

export enum ModelStatus {
  TRAINING = 'training',
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  ERROR = 'error'
}

export interface PredictionResult {
  model_id: string;
  prediction: any;
  confidence: number;
  timestamp: string;
  metadata: Record<string, any>;
}

// Error Types
export interface ApiError {
  message: string;
  code: string;
  details?: Record<string, any>;
  timestamp: string;
}

// Form Types
export interface FormField {
  name: string;
  label: string;
  type: 'text' | 'email' | 'password' | 'number' | 'select' | 'textarea' | 'checkbox' | 'radio' | 'date' | 'file';
  required: boolean;
  options?: { value: string; label: string }[];
  validation?: {
    min?: number;
    max?: number;
    pattern?: string;
    message?: string;
  };
}

export interface FormData {
  [key: string]: any;
}

// UI Types
export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
}

export interface LoadingState {
  isLoading: boolean;
  error: string | null;
  data: any;
}

export interface PaginationState {
  page: number;
  pageSize: number;
  total: number;
  totalPages: number;
}

// WebSocket Types
export interface WebSocketMessage {
  type: string;
  data: any;
  timestamp: string;
  user_id?: number;
}

export interface RealTimeUpdate {
  type: 'student_activity' | 'behavior_alert' | 'performance_update' | 'notification';
  data: any;
  timestamp: string;
}