`addteams [--team=X]`

`team` is an optional argument taking an integer for a team number (e.g.
`2791`). This command populates the local db with a row for a
`TBAW.models.Team` object with the given team number, if provided. If
not provided, populates the db with all team numbers (1-6000+). Takes
20+ minutes to perform all team creations.

---

`addevents [--key=X]`

`key` is an optional argument taking a string (e.g. `2016nyro`). This
command populates the local db with a row for a `TBAW.models.Event`
object with the given event key, if provided. If not provided, populates
the db with all the events in 2016. Other years to come in future.
This must be run **after** all teams in the event are located in the
db. (To create all events, this command takes roughly 15-20 minutes to
fully execute.)

---

`addmatches [--event=X]`

`event` is an optional argument taking a string (e.g. `2016nyro`). This
command populates the local db with rows for `TBAW.models.Match` objects
in the given event. If not provided, **all matches from 2016** will be
added to the database. **This can take up to several hours to execute.**

---

`testleaderboard`

This command prints leaderboard statistics to the console. For non-HTML/
view based testing. May take a few seconds to gather statistics.
