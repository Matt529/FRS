from config._cfg import ConfigValue, typed_cond, any_of, clamped, nonnegative

OPERATOR = ConfigValue('OR', condition=typed_cond(any_of(['AND', 'OR']), str))      # type: ConfigValue[str]
FUZZY_MIN_SIM = ConfigValue(0.2, condition=typed_cond(clamped(0, 1), float))        # type: ConfigValue[float]

CONN_TIMEOUT = ConfigValue(60*5, condition=typed_cond(nonnegative, int))            # type: ConfigValue[int]
BATCH_SIZE = ConfigValue(2000, condition=typed_cond(nonnegative, int))              # type: ConfigValue[int]
