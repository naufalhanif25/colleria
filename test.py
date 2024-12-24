import os
import getpath

path = os.path.abspath("temp/")
path = getpath.base("temp/")

print(path)