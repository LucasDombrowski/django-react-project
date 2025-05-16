export interface Player {
  id: number;
  first_name: string;
  last_name: string;
  nickname: string;
  role: string;
  photo_url: string | null;
  // birth_date was removed by user preference
} 