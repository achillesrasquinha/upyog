import traceback as tb

from upyog.model.base import BaseObject
from upyog.util.eject import ejectable

@ejectable(deps = ["BaseObject"])
class Response(BaseObject):
    class Type:
        OK = {
            "code": 200,
            "message": "OK"
        }
        INTERNAL_SERVER_ERROR = {
            "code": 500,
            "message": "Internal Server Error"
        }

    def __init__(self, code = 200, body = None, error = None,
            debug = True):
        """
            code:  HTTP status code.
            body:  response body.
            error: error message.
            debug: run in debug mode.
        """
        self.code  = code
        self.body  = body
        self.error = error

        self.debug = debug

    def set_error(self, type_, err):
        self.code  = type_["code"]
        self.data  = None

        self.error = { "type": type_["message"],
            "error": str(err)
        }

        if self.debug:
            # log traceback only in debug mode.
            self.error["traceback"] = tb.format_exc()

    def set_data(self, data):
        self.code  = Response.Type.OK["code"]
        self.error = None
        self.body  = data

    def json(self):
        data = {
            "statusCode": self.code
        }

        if self.error:
            data["error"] = self.error
        else:
            if self.body:
                data["data"] = self.body

        return data