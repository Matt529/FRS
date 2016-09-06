import os

from django.http import JsonResponse

from FRS.settings import LOG_PATH, FILE_NUM


class ApiResponse(JsonResponse):
    def __init__(self, *args, **kwargs):
        super(ApiResponse, self).__init__(args, kwargs)
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)

        with open(LOG_PATH + 'log_{0}.csv'.format(FILE_NUM), mode='a+', encoding='utf-8') as log_file:
            log_file.write('{0},'.format(i) for i in args)
            log_file.write('\n')
