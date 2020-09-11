from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import traceback


async def api_validation_exception(request: Request, exc: RequestValidationError):
    print(traceback.print_exc())
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "title": "Validation error occurred",
            "details": str(exc.errors()),
            "body": str(exc.body)
        },
        headers={
            "x-request-id": request.state.request_id
        }
    )


# general exception
async def handle_general_exception(request: Request, exc: HTTPException):
    # HTTPException is an based on Exception
    # for general debug , or batter you can write this to log file
    # print(exc.detail)
    print(traceback.print_exc())
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "title": "Internal server error",
            "details": str(exc)
        },
        headers={
            "x-request-id": request.state.request_id
        }
    )


#TODO: Exception Handlers for validation. Below is not working
exception_handlers = {
    Exception: handle_general_exception,
    RequestValidationError: api_validation_exception
}


error_responses = {
    404: {"title": "Not found"},
    403: {"title": "Forbidden"}
}