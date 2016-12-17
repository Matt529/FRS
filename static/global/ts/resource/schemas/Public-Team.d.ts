export interface PublicTeam {
  /**
   * FRC assigned team number
   */
  team_number?: number;
  /**
   * Unique team id, always equal to the team_number.
   */
  id: number;
  resource_uri?: string;
  /**
   * Most specific team name, simply frc#### where #### is the team number
   */
  key?: string;
  /**
   * Long FRC Team Name (note, this can be VERY long, short_name or nickname is recommended)
   */
  name: string;
  /**
   * Team Nickname, e.g. Shaker Robotics or Cheesy Poofs
   */
  nickname: string;
  /**
   * URL redirecting to a viewable page of this resource.
   */
  frs_url: string;
  [k: string]: any;
}