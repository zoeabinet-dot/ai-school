import { io, Socket } from 'socket.io-client';
import { toast } from 'react-hot-toast';
import { 
  ChatMessage, 
  ChatRoom, 
  RealTimeUpdate, 
  WebSocketMessage,
  User,
  BehaviorEvent,
  Notification
} from '../types';

export interface WebSocketConfig {
  url: string;
  options?: {
    transports: string[];
    autoConnect: boolean;
    reconnection: boolean;
    reconnectionAttempts: number;
    reconnectionDelay: number;
  };
}

export interface MessageHandler {
  type: string;
  handler: (data: any) => void;
}

class WebSocketService {
  private socket: Socket | null = null;
  private messageHandlers: Map<string, (data: any) => void> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private isConnecting = false;

  constructor() {
    this.setupDefaultHandlers();
  }

  private setupDefaultHandlers() {
    // Default handlers for common events
    this.on('connect', () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
      toast.success('Real-time connection established');
    });

    this.on('disconnect', (reason: string) => {
      console.log('WebSocket disconnected:', reason);
      if (reason === 'io server disconnect') {
        // Server disconnected, try to reconnect
        this.reconnect();
      }
    });

    this.on('connect_error', (error: any) => {
      console.error('WebSocket connection error:', error);
      this.handleConnectionError();
    });

    this.on('reconnect_attempt', (attemptNumber: number) => {
      console.log(`Reconnection attempt ${attemptNumber}`);
      this.reconnectAttempts = attemptNumber;
    });

    this.on('reconnect_failed', () => {
      console.error('WebSocket reconnection failed');
      toast.error('Real-time connection lost. Please refresh the page.');
    });
  }

  connect(token?: string): Promise<void> {
    return new Promise((resolve, reject) => {
      if (this.socket?.connected) {
        resolve();
        return;
      }

      if (this.isConnecting) {
        reject(new Error('Connection already in progress'));
        return;
      }

      this.isConnecting = true;

      const config: WebSocketConfig = {
        url: process.env.REACT_APP_WS_URL || 'ws://localhost:8000/ws',
        options: {
          transports: ['websocket', 'polling'],
          autoConnect: false,
          reconnection: true,
          reconnectionAttempts: this.maxReconnectAttempts,
          reconnectionDelay: 1000,
        },
      };

      this.socket = io(config.url, {
        ...config.options,
        auth: {
          token: token || localStorage.getItem('access_token'),
        },
      });

      this.socket.on('connect', () => {
        this.isConnecting = false;
        resolve();
      });

      this.socket.on('connect_error', (error) => {
        this.isConnecting = false;
        reject(error);
      });

      this.socket.connect();
    });
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  private reconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      setTimeout(() => {
        this.socket?.connect();
      }, 1000 * (this.reconnectAttempts + 1));
    }
  }

  private handleConnectionError(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      toast.error('Connection lost. Attempting to reconnect...');
    } else {
      toast.error('Unable to establish real-time connection');
    }
  }

  // Event handling
  on(event: string, handler: (data: any) => void): void {
    this.messageHandlers.set(event, handler);
    if (this.socket) {
      this.socket.on(event, handler);
    }
  }

  off(event: string): void {
    const handler = this.messageHandlers.get(event);
    if (handler && this.socket) {
      this.socket.off(event, handler);
      this.messageHandlers.delete(event);
    }
  }

  emit(event: string, data?: any): void {
    if (this.socket?.connected) {
      this.socket.emit(event, data);
    } else {
      console.warn('WebSocket not connected, cannot emit event:', event);
    }
  }

  // Chat functionality
  joinChatRoom(roomId: string): void {
    this.emit('join_room', { room_id: roomId });
  }

  leaveChatRoom(roomId: string): void {
    this.emit('leave_room', { room_id: roomId });
  }

  sendMessage(roomId: string, message: Partial<ChatMessage>): void {
    this.emit('send_message', {
      room_id: roomId,
      content: message.content,
      message_type: message.message_type || 'text',
      metadata: message.metadata,
    });
  }

  // Real-time updates
  subscribeToStudentActivity(studentId: number): void {
    this.emit('subscribe_student_activity', { student_id: studentId });
  }

  unsubscribeFromStudentActivity(studentId: number): void {
    this.emit('unsubscribe_student_activity', { student_id: studentId });
  }

  subscribeToBehaviorAlerts(): void {
    this.emit('subscribe_behavior_alerts');
  }

  unsubscribeFromBehaviorAlerts(): void {
    this.emit('unsubscribe_behavior_alerts');
  }

  subscribeToPerformanceUpdates(): void {
    this.emit('subscribe_performance_updates');
  }

  unsubscribeFromPerformanceUpdates(): void {
    this.emit('unsubscribe_performance_updates');
  }

  subscribeToNotifications(): void {
    this.emit('subscribe_notifications');
  }

  unsubscribeFromNotifications(): void {
    this.emit('unsubscribe_notifications');
  }

  // AI/ML real-time features
  subscribeToAIModelUpdates(): void {
    this.emit('subscribe_ai_model_updates');
  }

  unsubscribeFromAIModelUpdates(): void {
    this.emit('unsubscribe_ai_model_updates');
  }

  requestAIPrediction(modelId: string, data: any): void {
    this.emit('request_ai_prediction', {
      model_id: modelId,
      data: data,
    });
  }

  // Monitoring real-time features
  startMonitoringSession(studentId: number, settings: any): void {
    this.emit('start_monitoring_session', {
      student_id: studentId,
      settings: settings,
    });
  }

  stopMonitoringSession(sessionId: number): void {
    this.emit('stop_monitoring_session', {
      session_id: sessionId,
    });
  }

  // Utility methods
  isConnected(): boolean {
    return this.socket?.connected || false;
  }

  getConnectionState(): string {
    if (!this.socket) return 'disconnected';
    return this.socket.connected ? 'connected' : 'connecting';
  }

  // Typed event handlers
  onChatMessage(handler: (message: ChatMessage) => void): void {
    this.on('chat_message', handler);
  }

  onBehaviorAlert(handler: (event: BehaviorEvent) => void): void {
    this.on('behavior_alert', handler);
  }

  onPerformanceUpdate(handler: (update: any) => void): void {
    this.on('performance_update', handler);
  }

  onNotification(handler: (notification: Notification) => void): void {
    this.on('notification', handler);
  }

  onAIModelUpdate(handler: (update: any) => void): void {
    this.on('ai_model_update', handler);
  }

  onAIPredictionResult(handler: (result: any) => void): void {
    this.on('ai_prediction_result', handler);
  }

  onMonitoringFrame(handler: (frame: any) => void): void {
    this.on('monitoring_frame', handler);
  }

  onMonitoringEvent(handler: (event: BehaviorEvent) => void): void {
    this.on('monitoring_event', handler);
  }

  // Room management
  getRooms(): Promise<string[]> {
    return new Promise((resolve, reject) => {
      if (!this.socket?.connected) {
        reject(new Error('WebSocket not connected'));
        return;
      }

      this.socket.emit('get_rooms');
      this.socket.once('rooms_list', (rooms: string[]) => {
        resolve(rooms);
      });
    });
  }

  getRoomParticipants(roomId: string): Promise<User[]> {
    return new Promise((resolve, reject) => {
      if (!this.socket?.connected) {
        reject(new Error('WebSocket not connected'));
        return;
      }

      this.socket.emit('get_room_participants', { room_id: roomId });
      this.socket.once('room_participants', (participants: User[]) => {
        resolve(participants);
      });
    });
  }

  // Presence management
  setPresence(status: 'online' | 'away' | 'busy' | 'offline'): void {
    this.emit('set_presence', { status });
  }

  // Typing indicators
  startTyping(roomId: string): void {
    this.emit('start_typing', { room_id: roomId });
  }

  stopTyping(roomId: string): void {
    this.emit('stop_typing', { room_id: roomId });
  }

  onTypingStart(handler: (data: { room_id: string; user: User }) => void): void {
    this.on('typing_start', handler);
  }

  onTypingStop(handler: (data: { room_id: string; user: User }) => void): void {
    this.on('typing_stop', handler);
  }

  // File sharing
  shareFile(roomId: string, file: File, onProgress?: (progress: number) => void): void {
    const reader = new FileReader();
    reader.onload = () => {
      this.emit('share_file', {
        room_id: roomId,
        file_name: file.name,
        file_type: file.type,
        file_size: file.size,
        file_data: reader.result,
      });
    };
    reader.readAsArrayBuffer(file);
  }

  onFileShared(handler: (data: any) => void): void {
    this.on('file_shared', handler);
  }

  // Error handling
  onError(handler: (error: any) => void): void {
    this.on('error', handler);
  }

  // Cleanup
  cleanup(): void {
    this.messageHandlers.clear();
    this.disconnect();
  }
}

// Create singleton instance
export const webSocketService = new WebSocketService();

// Export for use in other modules
export default webSocketService;