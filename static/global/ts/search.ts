/**
 * Created by Matthew Crocco on 12/10/2016.
 */

/// <reference path='./libs/lodash.d.ts' />
/// <reference path='./libs/pluralize.d.ts' />
/// <reference path='./existential.ts' />

// -- Interface Definitions

interface ApiObj {
    id: number;
}

interface TeamObj extends ApiObj {
    team_number: number;
    name: string;
    key: string;
    nickname: string;
}

interface EventObj extends ApiObj {
    key: string;
    name: string;
    short_name: string;
}

interface ApiResponse<T extends ApiObj> {
    objects: T[];
}

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
    remote?: Bloodhound.RemoteOptions<T>;
    resultLimit?: number;
    initializeNow?: boolean;
}

interface ResourceDatasetOpts<T> {
    engine: Bloodhound<T>;
    templates?: Twitter.Typeahead.Templates<T>;
    async?: boolean;
    displayLimit: number;
}

interface ResourceDatasetNoHandleOpts<T> extends ResourceDatasetOpts<T> {
    display(x: T): string;
}

// --

/**
 * FRS Search Module
 */
const SearchModule = (() => {
    
    class ResourceHandle {
        private resourceName: string;
        private displayFn: () => string;
        
        constructor(name: string, display?: () => string) {
            this.resourceName = name;
            this.displayFn = _.isNil(display) ? () => name : display;
        }
        
        name(): string {
            return this.resourceName;
        }
        
        display(): string {
            return this.displayFn();
        }
        
    }
    
    const wsTokenizer = Bloodhound.tokenizers.whitespace;
    
    function apiIdentity(apiObj: ApiObj) {
        return apiObj.id;
    }
    
    function ResourceSearchEngineForHandle<T extends ApiObj>(handle: ResourceHandle, opts: ResourceEngineOpts<T>): Bloodhound<T> {
        return ResourceSearchEngine(handle.name(), opts);
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
    
    function ResourceDatasetForHandle<T extends ApiObj>(handle: ResourceHandle, opts: ResourceDatasetOpts<T>): Twitter.Typeahead.Dataset<T> {
        opts = _.defaults(opts, {
            async: false,
            templates: {
                header: `<h3 class="frs-search-header">${handle.display()}</h3>`
            }
        });
        
        return {
            name: `frc-${handle.name()}`,
            source: opts.engine,
            async: opts.async,
            display: handle.display,
            limit: opts.displayLimit,
            templates: opts.templates
        };
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

    function getTeamEventEngines(resultLimit: number, initializeNow: boolean = true): [Bloodhound<TeamObj>, Bloodhound<EventObj>] {
        return [
            ResourceSearchEngine<TeamObj>('team', {
                datumTokenizer: (x: TeamObj) => {
                    return [...x.team_number.toString().split(''), ...wsTokenizer(x.nickname)];
                },
                queryTokenizer: wsTokenizer,
                resultLimit,
                initializeNow
            }),
            ResourceSearchEngine('event', {
                datumTokenizer: (x: EventObj) => {
                    let key = x.key;
                    let year = key.substr(0, 4);
                    return [...year.split(''), year, x.short_name, key, ...wsTokenizer(x.name)];
                },
                queryTokenizer: wsTokenizer,
                resultLimit,
                initializeNow
            })
        ];
    }
    
    function initializeTypeahead(jq: JQuery, options: TypeaheadInitOptions<any>) {
        options = _.defaults(options, {
            hint: true,
            highlight: true,
            minLength: 1
        });
        
        jq.typeahead({
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
        
        initializeTypeahead($(options.typeaheadWrapperId).find(options.typeaheadClassName), {
            datasets: [
                ResourceDataset('team', {
                    engine: teamEngine,
                    displayLimit: 10,
                    display: (x: TeamObj) => {
                        const num = x.team_number.toString().trim();
                        return `${_.padStart(num, 4, '\u00A0')} \u2015 ${x.nickname ? x.nickname : x.name ? x.name : x.key}`;
                    }
                }), ResourceDataset('event', {
                    engine: eventEngine,
                    displayLimit: 5,
                    display: (x: EventObj) => `${_.padEnd(x.key.substr(0, 4), 4, '\u00A0')} \u2015 ${_.pad(x.key.substr(4), 5, '\u00A0')} \u2015 ${x.name}`
                })
            ]
        });
    }
    
    return {
        initializeTeamEventSearch,
        initializeTypeahead,
        ResourceHandle,
        ResourceSearchEngine,
        ResourceSearchEngineForHandle,
        ResourceDataset,
        ResourceDatasetForHandle,
    };
})();
