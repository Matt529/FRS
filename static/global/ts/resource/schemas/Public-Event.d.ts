export interface PublicEvent {
  /**
   * Unicode string data. Ex: "Hello World"
   */
  event_code?: string;
  /**
   * Integer data. Ex: 2673
   */
  event_type: number;
  /**
   * Unicode string data. Ex: "Hello World"
   */
  short_name: string;
  /**
   * Unicode string data. Ex: "Hello World"
   */
  website: string;
  /**
   * Unicode string data. Ex: "Hello World"
   */
  name?: string;
  /**
   * Unicode string data. Ex: "Hello World"
   */
  resource_uri?: string;
  /**
   * Unicode string data. Ex: "Hello World"
   */
  location: string;
  /**
   * Unicode string data. Ex: "Hello World"
   */
  timezone: string;
  /**
   * Unicode string data. Ex: "Hello World"
   */
  venue_address: string;
  /**
   * A date as a string. Ex: "2010-11-10"
   */
  end_date: any;
  /**
   * Integer data. Ex: 2673
   */
  event_district: number;
  /**
   * Integer data. Ex: 2673
   */
  id: number;
  /**
   * Boolean data. Ex: True
   */
  official?: boolean;
  /**
   * Integer data. Ex: 2673
   */
  year?: number;
  /**
   * Unicode string data. Ex: "Hello World"
   */
  key?: string;
  [k: string]: any;
}