# PythonToolboxDocumentation
Enables writing the Documentation for ESRI's PythonToolboxes WITHIN the PythonToolbox File (*.pyt)

## Disclaimer

This is a work in progress, written by an R User.

## Instructions:

Add Attributes to the Python Toolbox Class in `def __init__(self)`. For example, 
- self.purpose
- self.abstract
- self.credit
- self.tags 
- self.limits
- self.minScale
- self.maxScale

Enter all these attributes as characters strings except "self.tags", this must be a list of character strings.

For each Tool, you can add attributes to the parameters. E.g: `param1.dialogref`. For further examples see the sample toolbox.

Next, `import write_docs` in the beginning of your *.pyt file and run `write_docs.main(Toolbox,"SampleToolbox")` at the end of your *.pyt file. The second argument should contain the name of your *.pyt file without the extension. 





