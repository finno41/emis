def store_jsons(data):
    if data["resourceType"] == "Bundle":
        resource_types = [entry["resource"]["resourceType"] for entry in data["entry"]]
        return resource_types
