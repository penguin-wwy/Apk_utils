import argparse
import sys

class Args:
    def __init__(self, arguments=None):
        self.__args = None
        custom_arguments_provided = True
        self.result = {}

        # If no custom arguments are provided, use the program arguments
        if not arguments:
          arguments = sys.argv[1:]
          custom_arguments_provided = False


        self.__parse(arguments, custom_arguments_provided)

    def __parse(self, arguments, custom_arguments_provided=False):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description="""i don't know what should i say!!!
""",
                                         epilog="""examples:
        main.py""")

        parser.add_argument("-n", "--filename",    type=str, metavar="<filename>",     help="apk file's full path")
        parser.add_argument("-c", "--console",     action="store_true",                help="Terminal")
        parser.add_argument("-a", "--androidmanifest", action="store_true",           help="AndroidManifest")
        parser.add_argument("-d", "--dex",          type=str, metavar="dex file",       help="Dex file")
        parser.add_argument("-o", "--out",          type=str, metavar="<out dir>",      help="output dir-name")

        self.__args = parser.parse_args(arguments)

        if not custom_arguments_provided and not self.__args.filename and not self.__args.console:
            print("[Error] Need a apk filename (--filename or --console)")
            sys.exit(-1)

        self.result["filePath"] = self.__args.filename

        if self.__args.console:
            self.result["console"] = True
        else:
            self.result["console"] = False

        if self.__args.out:
            self.result["outDir"] = self.__args.out
        else:
            self.result["outDir"] = "tmp_file"

        if self.__args.androidmanifest:
            self.result["androidmanifest"] = True
        else:
            self.result["androidmanifest"] = False

        if self.__args.dex:
            self.result["dex"] = True
        else:
            self.result["dex"] = False

    def getResult(self):
        return self.result

