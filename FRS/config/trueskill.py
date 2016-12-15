from FRS.config._cfg import ConfigValue, clamped, nonnegative, any_of, join, typed_cond, is_number

# See http://www.moserware.com/assets/computing-your-skill/The%20Math%20Behind%20TrueSkill.pdf
# for a good explanation of each parameter

# GENERAL DEFAULTS FOR "REASONABLE" RESULTS:
#   mu          = 25
#   sigma       = mu/3
#   beta        = sigma/2
#   tau         = sigma/100

MU = 1500           # Assumed Initial Skill
SIGMA = MU/3        # Assumed Initial Standard Deviation (Assumed Uncertainty,
BETA = SIGMA/2      # Assumed "Skill Chain Length", if Player 1 is BETA skill about Player 2, they are expected to win 80% of the time
TAU = SIGMA/100     # Dynamicity of Skills, tends to be directly proportional with volatility

nonegative_number = join(is_number, nonnegative)
zero_one_float = join(is_number, clamped(0, 1))

MU = ConfigValue(MU, condition=nonegative_number)                     # type: ConfigValue[float]
SIGMA = ConfigValue(SIGMA, condition=nonegative_number)               # type: ConfigValue[float]
BETA = ConfigValue(BETA, condition=nonegative_number)                 # type: ConfigValue[float]
TAU = ConfigValue(TAU, condition=nonegative_number)                   # type: ConfigValue[float]

# Likelihood of a Draw
DRAW_PROBABILITY = ConfigValue(0.1, condition=zero_one_float)         # type: ConfigValue[float]

# TODO Should we even acknowledge decay?
# ELO Decay Shape Parameter
# elo_mu = default_mu + (elo_mu - default_mu)*(1 - decay_alpha)^t
#
# The ELO Decay function after t iterations follows the above exponential decay function. This can be interpreted
# as how much a team's skill level decays from year to year.
DECAY_ALPHA = ConfigValue(0.45, condition=zero_one_float)             # type: ConfigValue[float]

TRUESKILL_BACKEND = ConfigValue("mpmath", condition=typed_cond(any_of(['mpmath', None]), str, type(None)))  # type: ConfigValue[str]
