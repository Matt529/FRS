export interface PublicEvent {
  year?: number;
  event_code?: string;
  event_district: number;
  timezone: string;
  location: string;
  official?: boolean;
  key?: string;
  short_name: string;
  id: number;
  venue_address: string;
  resource_uri?: string;
  event_type: number;
  name?: string;
  website: string;
  end_date: any;
  [k: string]: any;
}