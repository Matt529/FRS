import traceback

class ProcessExceptionMiddleware(object):
    def process_exception(self, request, exception):
        print(exception)
        traceback.print_exc()
        
