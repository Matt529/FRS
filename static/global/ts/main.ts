
/// <reference path="./libs/jquery.d.ts"/>
/// <reference path="./libs/typeahead.d.ts"/>

interface ApiObj {
    id: number;
}

interface TeamObj extends ApiObj {
    team_number: number;
    nickname: string;
}

interface EventObj extends ApiObj {
    key: string;
    name: string;
}

const wsTokenizer = Bloodhound.tokenizers.whitespace;

function apiIdentity(apiObj: ApiObj) {
    return apiObj.id;
}

function getSearchEngines(): [Bloodhound<TeamObj>, Bloodhound<EventObj>] {

    let t: Bloodhound<TeamObj> = new Bloodhound<TeamObj>({
        initialize: false,
        datumTokenizer: (x: TeamObj) => {
            console.dir(x);
            return [x.team_number.toString(), ...wsTokenizer(x.nickname)];
        },
        queryTokenizer: wsTokenizer,
        identify: apiIdentity,
        remote: {
            // url: "/api/v1/team/?format=json",
            url: "/api/search?query=%QUERY&type=Team",
            wildcard: "%QUERY",
            transform: (x) => x.objects
        }
    });

    let e: Bloodhound<EventObj> = new Bloodhound<EventObj>({
        initialize: false,
        datumTokenizer: (x: EventObj) => [x.key, ...wsTokenizer(x.name)],
        queryTokenizer: wsTokenizer,
        identify: apiIdentity,
        remote: {
            // url: "/api/v1/team/?format=json",
            url: "/api/search?query=%QUERY&type=Event",
            wildcard: "%QUERY",
            transform: (x) => x.objects
        }
    });

    return [t, e];
}

let [teamEngine, eventEngine] = getSearchEngines();

$.when(teamEngine.initialize(), eventEngine.initialize()).done(() => {
    // When both engines are initialized
    $("#typeahead-wrapper").find(".typeahead").typeahead({
        highlight: true
    }, {
        name: "frc-teams",
        source: teamEngine,
        display: (x) => `${x.nickname} - ${x.team_number}`,
        templates: {
            header: "<h3>Teams</h3>"
        }
    }, {
        name: "frc-events",
        source: eventEngine,
        display: (x) => `${x.name} - ${x.key}`,
        templates: {
            header: "<h3>Events</h3>"
        }
    });
});
