def result_ok(message="", content=None):
    return {"ok": True, "message": message, "content": content}


def result_error(message="", content=None):
    return {"ok": False, "message": message, "content": content}
