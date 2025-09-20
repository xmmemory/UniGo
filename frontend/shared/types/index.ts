export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  phone_number: string;
  student_id: string;
  university: string;
  created_at: string;
}

export interface Trip {
  id: number;
  departure: string;
  destination: string;
  departure_time: string;
  price_per_person: number;
  available_seats: number;
  owner_id: number;
  owner_name?: string;
  created_at?: string;
}

export interface Booking {
  id: number;
  user_id: number;
  trip_id: number;
  booked_at: string;
  status: string;
  trip?: Trip;
}

export interface SecondHandItem {
  id: number;
  title: string;
  description: string;
  price: number;
  category: string;
  condition: string;
  owner_id: number;
  owner_name?: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface SecondHandItemCreate {
  title: string;
  description: string;
  price: number;
  category: string;
  condition: string;
}

export interface ErrandTask {
  id: number;
  title: string;
  description: string;
  reward: number;
  location: string;
  deadline: string;
  owner_id: number;
  owner_name?: string;
  assignee_id: number | null;
  assignee_name?: string | null;
  created_at: string;
  updated_at: string;
  status: 'open' | 'in_progress' | 'completed' | 'cancelled';
}

export interface ErrandTaskCreate {
  title: string;
  description: string;
  reward: number;
  location: string;
  deadline: string;
}