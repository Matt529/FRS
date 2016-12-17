from FRS.config._cfg import ConfigValue, is_type

class names:
    PUBLIC_TEAMS = ConfigValue('teampub', condition=is_type(str))       # type: ConfigValue[str]
    PUBLIC_EVENTS = ConfigValue('eventpub', condition=is_type(str))     # type: ConfigValue[str]
    
class schemas:
    PUBLIC_TEAMS_SCHEMA = ConfigValue('PublicTeam', condition=is_type(str))     # type: ConfigValue[str]
    PUBLIC_EVENTS_SCHEMA = ConfigValue('PublicEvent', condition=is_type(str))   # type: ConfigValue[str]
