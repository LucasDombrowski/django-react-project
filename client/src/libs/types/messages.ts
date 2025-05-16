// Type definition for individual messages passed from Django
export interface DjangoMessage {
  text: string;
  level: string; // e.g., 'debug', 'info', 'success', 'warning', 'error'
} 