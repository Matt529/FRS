export interface PublicTeam {
  awards_count?: number;
  team_number?: number;
  rookie_year: number;
  location: string;
  /**
   * A list of the years a team was active
   */
  active_years?: number[];
  longest_event_winstreak?: number;
  match_wins_count?: number;
  match_losses_count?: number;
  event_wins_count?: number;
  /**
   * Team website
   */
  website: string;
  blue_banners_count?: number;
  name: string;
  match_winrate?: number;
  elo_mu?: number;
  match_ties_count?: number;
  region: string;
  key?: string;
  country_name: string;
  id: number;
  event_winrate?: number;
  active_event_winstreak?: number;
  motto: string;
  nickname: string;
  resource_uri?: string;
  locality: string;
  elo_sigma?: number;
  event_attended_count?: number;
  [k: string]: any;
}