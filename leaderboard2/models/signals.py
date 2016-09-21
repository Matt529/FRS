from FRS.settings import LEADERBOARD_COUNT


def team_leaderboard_changed(action, instance, **kwargs):
    if action == "post_add":
        print("before: ", list(instance.teams.order_by(instance.field)))
        if instance.teams.count() > LEADERBOARD_COUNT:
            instance.teams.remove(instance.teams.order_by(instance.field).last())
        print(" after: ", list(instance.teams.order_by(instance.field)))
