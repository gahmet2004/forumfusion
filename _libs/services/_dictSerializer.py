def serialize(d : dict) -> str:
    response = ""
    for key in d:
        response += f"{key}:{type(d[key]).__name__}:{d[key]}/"
    return response
def deserialize(s : str) -> dict:
    deserialize = s.split('/')
    deserialize = deserialize[0:(len(deserialize) - 1)]
    response = dict()
    for line in deserialize:
        line = line.split(':')
        if (line[1].__eq__('int')):
            response[line[0]] = int(line[2])
        else:
            response[line[0]] = line[2]
    return response
def listIdSerialize(data : list) -> str:
    return ','.join(data)
def listIdDeserialize(data : str) -> list:
    data = data.split(',')
    for node in data:
        node = int(node)
    return data