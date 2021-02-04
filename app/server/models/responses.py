"""Responses Model"""
def response_model(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message
    }
    
def error_reponse_model(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }