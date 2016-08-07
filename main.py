import sys
import cmd
from apk_utils.core import *

from apk_utils.args import *

if __name__ == "__main__":
    resut = Args().getResult()
    Core(resut).analyze()



