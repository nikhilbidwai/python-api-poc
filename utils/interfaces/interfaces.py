import requests
from config.interface_config import BACKEND_URL, DEFAULT_HEADERS
from utils.logger.logger import api_logger as logger


def get(api_uri,params=None, backend_url=BACKEND_URL):
    logger.info("Invoking API: " + backend_url + api_uri)
    response = requests.get(backend_url + api_uri)
    logger.info("Received Status Code: " + str(response.status_code))
    logger.debug(response.json())
    return response


def put(api_uri, data, backend_url=BACKEND_URL):
    logger.info("Invoking API: " + backend_url + api_uri)

    response = requests.put(backend_url + api_uri,
                            data=data,
                            headers=DEFAULT_HEADERS)

    logger.info("Received Status Code: " + str(response.status_code))
    logger.debug(response.json())
    return response


