__author__ = 'Charlie'
import win32api as w

filer = "E:\Program Files\Pycharm\Projects\\Life.tax"

# w.WriteProfileVal(section, entry, value, filer)
# where section will be folder, entry will be item/subfolder, value will be description and filer is registry file

current = ""

for i in range(10):
    w.WriteProfileVal("Section 1", "entry %d" % i, i, filer)

for i in range(10):
    for j in range(10):
        w.RegEnumKey("Section 1", i)