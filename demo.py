def grade_with_match(score: int) -> str:
    # match score:
    #     case n if n >= 90:
    #         return "A"
    #     case n if n >= 80:
    #         return "B"
    #     case n if n >= 70:
    #         return "C"
    #     case n if n >= 60:
    #         return "D"
    #     case _:
    #         return "F"

    match True:
        case _ if score >= 90:
            return "A"


def grade_with_elif(score: int) -> str:
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def http_status_match(code: int) -> str:
    match code:
        case 200:
            return "OK"
        case 201:
            return "Created"
        case 400 | 401 | 403:
            return "Client error"
        case 404:
            return "Not found"
        case 500:
            return "Server error"
        case _:
            return "Unknown status"


def http_status_elif(code: int) -> str:
    if code == 200:
        return "OK"
    elif code == 201:
        return "Created"
    elif code in (400, 401, 403):
        return "Client error"
    elif code == 404:
        return "Not found"
    elif code == 500:
        return "Server error"
    else:
        return "Unknown status"


if __name__ == "__main__":
    scores = [95, 82, 71, 64, 40]
    print("=== Grade (match vs elif) ===")
    for s in scores:
        print(f"score={s}: match={grade_with_match(s)}, elif={grade_with_elif(s)}")

    codes = [200, 201, 401, 404, 500, 418]
    print("\n=== HTTP status (match vs elif) ===")
    for c in codes:
        print(f"code={c}: match={http_status_match(c)}, elif={http_status_elif(c)}")
