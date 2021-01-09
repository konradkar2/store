from store.application.exceptions import InternalServerError


def endpoint(func):
    def check_for_exceptions(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
             return {"message": str(e)}, 400
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    return check_for_exceptions