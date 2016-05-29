`addteams [--team=X]`

`team` is an optional argument taking an integer for a team number (e.g.
`2791`). This command populates the local db with a row for a
`TBAW.models.Team` object with the given team number, if provided. If
not provided, populates the db with all team numbers (1-6000+).

---

`addevents [--key=X]`

`key` is an optional argument taking a string (e.g. `2016nyro`). This
command populates the local db with a row for a `TBAW.models.Event`
object with the given event key, if provided. If not provided, populates
the db with all the events in 2016. Other years to come in future.
This must be run **after** all teams in the event are located in the
db. (To create all events, this command takes roughly 15 minutes to
fully execute.)
