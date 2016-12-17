export interface PublicEvent {
  /**
   * Shortened event name (e.g. Finger Lakes)
   */
  short_name: string;
  resource_uri?: string;
  /**
   * Full event name (e.g. Finger Lakes Regional)
   */
  name?: string;
  /**
   * Unique database id
   */
  id: number;
  /**
   * Unique event key, often of the form ###w where #### is the year and w is the event code
   */
  key?: string;
  /**
   * URL redirecting to a viewable page of this resource.
   */
  frs_url: string;
  [k: string]: any;
}