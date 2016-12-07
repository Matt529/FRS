from FRS.settings import SUPPORTED_YEARS


def supported_years(request):
    return {'SUPPORTED_YEARS': SUPPORTED_YEARS}
