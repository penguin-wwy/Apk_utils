import os
import sys

def apktool_win(path, indir, outdir):
    bat = indir + '\\tool\\apktool.bat'
    info = os.popen(bat + " d " + path + " -o " + outdir)
    print(info.read())
