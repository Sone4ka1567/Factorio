def result_ok(message=""):
    return {"ok": True, "message": message}


def result_error(message=""):
    return {"ok": False, "message": message}
