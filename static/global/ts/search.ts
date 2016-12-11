/**
 * Created by Matthew Crocco on 12/10/2016.
 */

/// <reference path='./libs/lodash.d.ts' />

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
}

interface ApiResponse<T extends ApiObj> {
    objects: T[];
}

const SearchModule = (() => {

    const wsTokenizer = Bloodhound.tokenizers.whitespace;

    function apiIdentity(apiObj: ApiObj) {
        return apiObj.id;
    }

    function getSearchEngines(): [Bloodhound<TeamObj>, Bloodhound<EventObj>] {

        let t: Bloodhound<TeamObj> = new Bloodhound<TeamObj>({
            initialize: false,
            datumTokenizer: (x: TeamObj) => {
                console.dir(x);
                return [...x.team_number.toString().split(''), ...wsTokenizer(x.nickname)];
            },
            queryTokenizer: wsTokenizer,
            identify: apiIdentity,
            remote: {
                url: '/api/v1/team/search/?query=%QUERY&limit=20',
                wildcard: '%QUERY',
                rateLimitBy: 'throttle',
                rateLimitWait: 100,
                transform: (x: ApiResponse<TeamObj>) => x.objects
            }
        });

        let e: Bloodhound<EventObj> = new Bloodhound<EventObj>({
            initialize: false,
            datumTokenizer: (x: EventObj) => {
                let key = x.key;
                let year = key.substr(0, 4);
                return [...year.split(''), key, ...wsTokenizer(x.name)];
            },
            queryTokenizer: (x: string) => {
                let words = wsTokenizer(x);
                let result = [];
                for (let word of words) {
                    if (/(\d){4}(.*)/g.test(word)) {
                        result.push(word.substr(0, 4), word.substr(4));
                    } else {
                        result.push(word);
                    }
                }
                console.dir(result);

                return result;
            },
            identify: apiIdentity,
            remote: {
                url: '/api/v1/event/search/?query=%QUERY&limit=20',
                wildcard: '%QUERY',
                rateLimitBy: 'throttle',
                rateLimitWait: 100,
                transform: (x: ApiResponse<EventObj>) => x.objects
            }
        });

        return [t, e];
    }

    function initialize(wrapper: string = '#typeahead-wrapper', className: string = '.typeahead') {
        let [teamEngine, eventEngine] = getSearchEngines();

        $.when<any>(teamEngine.initialize(), eventEngine.initialize()).done(() => {
            // When both engines are initialized
            $(wrapper).find(className).typeahead<any>({
                classNames: {
                    input: 'frs-search-input',
                    hint: 'frs-search-hint',
                    suggestion: 'frs-search-result',
                    menu: 'frs-search-menu',
                    dataset: 'frs-search-dataset'
                },
                highlight: true,
                hint: true,
                minLength: 1
            }, {
                name: 'frc-teams',
                source: teamEngine,
                display: (x: TeamObj) => `${x.team_number} - ${x.nickname ? x.nickname : x.name ? x.name : x.key}`,
                async: true,
                limit: 10,
                templates: {
                    header: '<h3 class="frs-search-header">Teams</h3>'
                }
            }, {
                name: 'frc-events',
                source: eventEngine,
                display: (x: EventObj) => `${_.padEnd(x.key, 9)} - ${x.name}`,
                async: true,
                limit: 5,
                templates: {
                    header: '<h3 class="frs-search-header">Events</h3>'
                }
            });
        });
    }

    return {
        getSearchEngines,
        initialize
    };
})();
