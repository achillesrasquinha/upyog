# def test_read(tmpdir):
#     import upyog as upy

#     directory = tmpdir.mkdir("tmp")
#     tempfile  = directory.join("foobar.txt")
#     tempfile.write("foobar")

#     assert tempfile.read() == upy.read(tempfile)
#     assert tempfile.read() == upy.read(str(tempfile))

#     tempfile  = directory.join("barfoo.txt")
#     tempfile.write(\
#         """
#         foobar
#         \n
#         barfoo
#         """
#     )

#     content = tempfile.read()
#     assert upy.strip(content) == upy.read(str(tempfile))
#     assert content == upy.read(str(tempfile), clean = False)


# @ejectable(deps = ["is_list_like", "safe_decode", "read"])
# def load_json(path, *args, **kwargs):
#     import json, os.path as osp
#     import collections

#     object_hook = kwargs.pop("object_hook", None)

#     if is_list_like(path) or isinstance(path, collections.Mapping):
#         return path

#     path = safe_decode(path)

#     if isinstance(path, str):
#         if osp.isfile(path):
#             content = read(path, *args, **kwargs)
#         else:
#             content = path
#     else:
#         content = read(path, *args, **kwargs)

#     data = json.loads(content, object_hook = object_hook)

#     return data

def test_upyog_load_json(tmpdir):
    import upyog as upy, json
    
    directory = tmpdir.mkdir("tmp")
    tempfile  = directory.join("foobar.json")

    data = {
        "a": {
            "b": {
                "c": 1
            }
        }
    }

    assert upy.load_json(data) == data

    tempfile.write(json.dumps(data))

    assert upy.load_json(tempfile) == data
    assert upy.load_json(str(tempfile)) == data

    assert upy.load_json(r'{"a":{"b":{"c":1}}}') == data

    object_hook = lambda x: x
    assert upy.load_json(tempfile, object_hook = object_hook) == data