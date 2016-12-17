/**
 * Created by Matthew Crocco on 12/10/2016.
 */


import {ApiObj, PublicTeam, PublicEvent, ApiResponse} from './resource/resources';

import * as _ from 'lodash';
import * as pluralize from 'pluralize';
import * as Bloodhound from 'corejs-typeahead/dist/bloodhound.js';

type RemoteOptions<T> = Bloodhound.RemoteOptions<T>;
type Templates<T> = Twitter.Typeahead.Templates<T>;

interface InitOptions {
    resultLimit: number;
    typeaheadWrapperId?: string;
    typeaheadClassName?: string;
}

interface TypeaheadInitOptions<T> {
    hint?: boolean;
    highlight?: boolean;
    minLength?: number;
    datasets: Twitter.Typeahead.Dataset<T>[];
}

interface ResourceEngineOpts<T> extends Bloodhound.BloodhoundOptions<T> {
    datumTokenizer: (datum: T) => string[];
    queryTokenizer: (query: string) => string[];
    remote?: RemoteOptions<T>;
    resultLimit?: number;
    initializeNow?: boolean;
}

interface ResourceDatasetOpts<T> {
    engine: Bloodhound<T>;
    templates?: Templates<T>;
    async?: boolean;
    displayLimit: number;
}

interface ResourceDatasetNoHandleOpts<T> extends ResourceDatasetOpts<T> {
    display(x: T): string;
}

const wsTokenizer = Bloodhound.tokenizers.whitespace;

function apiIdentity(apiObj: ApiObj) {
    return apiObj.id;
}

function ResourceSearchEngine<T extends ApiObj>(resourceName: string, opts: ResourceEngineOpts<T>): Bloodhound<T> {
    opts = _.defaults(opts, {
        resultLimit: 30,
        initializeNow: true,
        identify: apiIdentity,
        indexRemote: true,
    });
    
    opts.remote = _.assign(opts.remote, {
        url: `/api/v1/${resourceName}/search/?query=%QUERY&limit=${opts.resultLimit}`,
        wildcard: '%QUERY',
    });
    
    opts.remote = _.defaults(opts.remote, {
        rateLimitBy: 'debounce',
        rateLimitWait: 300,
        transform: (x: ApiResponse<T>) => x.objects
    });
    
    return new Bloodhound<T>(opts);
}

function ResourceDataset<T extends ApiObj>(resourceName: string, opts: ResourceDatasetNoHandleOpts<T>): Twitter.Typeahead.Dataset<T> {
    opts = _.defaults(opts, {
        async: false,
        templates: {
            header: `<h3 class="frs-search-header">${pluralize(_.capitalize(resourceName))}</h3>`
        }
    });
    
    return {
        name: `frc-${resourceName}`,
        source: opts.engine,
        async: opts.async,
        display: opts.display,
        limit: opts.displayLimit,
        templates: opts.templates
    };
}

function getTeamEventEngines(resultLimit: number, initializeNow: boolean = true): [Bloodhound<PublicTeam>, Bloodhound<PublicEvent>] {
    return [
        ResourceSearchEngine<PublicTeam>('teampub', {
            datumTokenizer: (x: PublicTeam) => {
                return [...x.team_number.toString().split(''), ...wsTokenizer(x.nickname)];
            },
            queryTokenizer: wsTokenizer,
            resultLimit,
            initializeNow,
            remote: {
                transform: (x: ApiResponse<PublicTeam>) => x.objects
            }
        }),
        ResourceSearchEngine<PublicEvent>('eventpub', {
            datumTokenizer: (x: PublicEvent): string[] => {
                let key = x.key;
                let year = key.substr(0, 4);
                return [...year.split(''), year, x.short_name, key, ...wsTokenizer(x.name)];
            },
            queryTokenizer: wsTokenizer,
            resultLimit,
            initializeNow,
            remote: {
                transform: (x: ApiResponse<PublicEvent>) => x.objects
            }
        })
    ];
}

function initializeTypeahead(jq: JQuery, options: TypeaheadInitOptions<any>): JQuery {
    options = _.defaults(options, {
        hint: true,
        highlight: true,
        minLength: 1
    });
    
    return jq.typeahead({
        classNames: {
            input: 'frs-search-input',
            hint: 'frs-search-hint',
            suggestion: 'frs-search-result',
            menu: 'frs-search-menu',
            dataset: 'frs-search-dataset'
        },
        highlight: options.highlight,
        hint: options.hint,
        minLength: options.minLength
    }, options.datasets);
}

function initializeTeamEventSearch(options: InitOptions) {
    options = _.defaults(options, {
        typeaheadWrapperId: '#typeahead-wrapper',
        typeaheadClassName: '.typeahead'
    });

    let [teamEngine, eventEngine] = getTeamEventEngines(options.resultLimit, true);
    let jq: JQuery;
    
    (jq = initializeTypeahead($(options.typeaheadWrapperId).find(options.typeaheadClassName), {
        datasets: [
            ResourceDataset('team', {
                engine: teamEngine,
                displayLimit: 10,
                display: (x: PublicTeam) => {
                    const num = x.team_number.toString().trim();
                    return `${_.padStart(num, 4, '\u00A0')} \u2015 ${x.nickname ? x.nickname : x.name ? x.name : x.key}`;
                }
            }), ResourceDataset('event', {
                engine: eventEngine,
                displayLimit: 5,
                display: (x: PublicEvent) => `${_.padEnd(x.key.substr(0, 4), 4, '\u00A0')} \u2015 ${_.pad(x.key.substr(4), 5, '\u00A0')} \u2015 ${x.name}`
            })
        ]
    })).bind('typeahead:select', <any>((jqeObj: JQueryEventObject, suggestion: ApiObj) => window.location.replace(suggestion.frs_url)));
}

export {
    initializeTypeahead,
    initializeTeamEventSearch,
    ResourceDataset,
    ResourceSearchEngine
};
