def __list_all_modules():
    from os.path import dirname, basename, isfile
    import glob

    path = glob.glob(dirname(__file__)

    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.py' in file:
                files.append(os.path.join(r, file))

    return files


ALL_MODULES = sorted(__list_all_modules())
print("Starting to load: %s", str(ALL_MODULES))
__all__ = ALL_MODULES + ["ALL_MODULES"]
