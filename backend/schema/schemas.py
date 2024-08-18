def individual_serial(spirit) -> dict:
    return {
        "_id" : str(spirit["_id"]),
        "spirit_name": spirit["spirit_name"],
        "spirit_price": spirit["spirit_price"],
        "spirit_stock": spirit["spirit_stock"],
        "spirit_category": spirit["spirit_category"],
        "Date": spirit["Date"]
    }

def list_serial(spirits) -> list:
    return[individual_serial(spirit) for spirit in spirits]