/**
 * Created by Matthew Crocco on 12/17/2016.
 */

import {PublicTeam} from "./schemas/Public-Team";
import {PublicEvent} from "./schemas/Public-Event";
export * from './schemas/Public-Event';
export * from './schemas/Public-Team';

export interface ApiResponse<T> {
    objects: T[];
}

export type ApiObj = PublicTeam | PublicEvent
