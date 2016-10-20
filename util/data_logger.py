import inspect
import os
from FRS.settings import LOG_PATH


def log_bad_data(item: str, reason: str) -> None:
    path = os.path.join(LOG_PATH, 'bad_data.tsv')
    file_origin = inspect.stack()[1][1]
    function_origin = inspect.stack()[1][3]
    with open(path, 'a+') as file:
        file.write('{0}\t{1}\t{2}\t{3}\n'.format(file_origin, function_origin, item, reason))
        file.flush()
