import arcpy

import write_docs
import importlib
importlib.reload(write_docs)



class Toolbox(object):
    def __init__(self):
        self.label = "ProjectASTRAPythonToolbox"
        self.alias = "ProjectASTRAPythonToolbox"
        # custom attributes.. wasn't here originally:
        self.purpose = "A nice multiline description, with some *bold* and _italic_ text just " + \
		               "to show how its done."
        self.abstract = "*More* information on [https://github.com/ratnanil/PythonToolboxDocumentation](Github)" + \
                        
        self.credit = "Authors: Nils Ratnaweera"

        self.tags = ["Some","nice","tags"]

        self.limits = "No limits"

        self.minScale = ""
        self.maxScale = ""

        # List of tool classes associated with this toolbox
        self.tools = [sampletool]


##################################################################################################
# Sampletool  ####################################################################################
##################################################################################################


class sampletool(object):
    def __init__(self):
        self.label = "00 Sampletool"
        self.description = "A nice multiline description " + \
                           "to show how its done "
        self.canRunInBackground = False
        self.category = "A Category"

        param1 = arcpy.Parameter(
            displayName="param1",
            name="param1",
            datatype="GPFeatureLayer"
        )

        param1.dialogref = "Dialog reference"

        self.parameters = [param1]

        ## Some Additional Metadata than can be stored for documentation

        self.tags = ["tag1", "tag2", "tag3"]

        self.limits = "Describe the limits of this tool"

        self.credit = "Give credit to Authors, Papers etc."

        self.minScale = ""
        self.maxScale = ""

        self.codeexamples = [
            [
                "The Title of my First Example",
                "This is the description of my first exmple",
                "def some_nice_pythoncode(text):"
                "    print(text) # notice the twoliner without backslash"
            ],
            [
                "The Title of my Second Example",
                "This is the description of my second exmple",
                "def more_pythoncode(text):"
                "    print(text)"
            ],
        ]



    def getParameterInfo(self):
        return self.parameters

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):


    return


write_docs.main(Toolbox, "ASTRA_ArcpyToolbox")
