import datetime
import xml.etree.cElementTree as ET
import re


def md_links_html(text):
    # Takes a [a](b) pattern and returns a html version
    return re.sub(r"\[([^\]]+)\]\(([^\)]+)\)", r"<a href='\1'>\2</a>", text)


def md_bold_html(text):
    # Takes words wrapped in * and makes it html-style.
    return re.sub(r"\*([^\*]+)\*",r"<SPAN STYLE='font-weight:bold;'>\1</SPAN>", text)


def md_italic_html(text):
    # Takes words wrapped in _ and makes it html-style. Technically, not correct Markdown
    return re.sub(r"_([^_]+)_", r"<SPAN STYLE='font-weight:italic;'>\1</SPAN>", text)


def md_html_all(text):
    text = md_italic_html(text)
    text = md_bold_html(text)
    text = md_links_html(text)
    text = "<DIV STYLE='text-align:Left;'><DIV><P>"+text+"</P></DIV></DIV>"
    return text


def getattr_if(obj, attribute, alternative="", html=False):
    if hasattr(obj, attribute):
        out = getattr(obj, attribute)
        if html:
            out = md_html_all(out)
    else:
        out = alternative
    return out


def write_tool_doc(pythontoolbox, filename):
    toolbox_tools = pythontoolbox().tools
    toolbox_alias = pythontoolbox().alias

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    now = datetime.datetime.now().strftime("%H:%M:%S")

    for tool_i in toolbox_tools:
        metadata = ET.Element("metadata")
        esri = ET.SubElement(metadata, "Esri")
        ET.SubElement(esri, "CreaDate").text = today
        ET.SubElement(esri, "CreaTime").text = now             # *
        ET.SubElement(esri, "ArcGISFormat").text = ""         # *
        ET.SubElement(esri, "SyncOnce").text = ""            # *
        ET.SubElement(esri, "ModDate").text = today              # *
        ET.SubElement(esri, "ModTime").text = today              # *
        scaleRange = ET.SubElement(esri, "scaleRange")
        ET.SubElement(scaleRange, "minScale").text = getattr_if(tool_i(), "maxScale")
        ET.SubElement(scaleRange, "maxScale").text = getattr_if(tool_i(), "maxScale")

        tool_name = tool_i.__name__
        tool_label = tool_i().label
        tool_description = getattr_if(tool_i(), "description", html=True)
        # tool_canRunInBackground = tool_i().canRunInBackground = False
        tool_category = getattr_if(tool_i(),"category")

        tool = ET.SubElement(metadata,
                             "tool",
                             xmlns="",
                             name=tool_name,
                             displayname=tool_label,
                             toolboxalias=toolbox_alias)
        ET.SubElement(tool, "arcToolboxHelpPath").text = "c:\\program files\\arcgis\\pro\\Resources\\Help\\gp"

        parameters = ET.SubElement(tool, "parameters")

        for param_i in tool_i().parameters:
            param_displayName = param_i.displayName
            param_name = param_i.name
            param_datatype = param_i.datatype
            param_parameterType = param_i.parameterType
            param_direction = param_i.direction
            param_value = param_i.value

            param = ET.SubElement(parameters,
                                  "param",
                                  name=param_name,
                                  displayname=param_displayName,
                                  type=param_parameterType,
                                  direction=param_direction,
                                  datatype=param_datatype,
                                  expression=param_name)

            ET.SubElement(param, "dialogReference").text = getattr_if(param_i, "dialogref", html=True)
            ET.SubElement(param, "pythonReference").text = getattr_if(param_i, "pythonref", html=True)

        ET.SubElement(tool,"summary").text = tool_description
        ET.SubElement(tool,"usage").text = getattr_if(tool_i(), "usage",html=True)
        scriptExamples = ET.SubElement(tool,"scriptExamples")

        codeexamples = getattr_if(tool_i(),"codeexamples")
        for examples in codeexamples:
            scriptExample = ET.SubElement(scriptExamples, "scriptExample")
            ET.SubElement(scriptExample, "title").text = examples[0]
            ET.SubElement(scriptExample, "para").text = md_html_all(examples[1])
            ET.SubElement(scriptExample,"code").text = examples[2]

        dataIdInfo = ET.SubElement(metadata, "dataIdInfo")
        idCitation = ET.SubElement(dataIdInfo, "idCitation")
        ET.SubElement(idCitation, "resTitle").text = toolbox_alias+" ("+tool_category+")"

        ET.SubElement(dataIdInfo, "idCredit").text = getattr_if(tool_i(), "credit")
        searchKeys = ET.SubElement(dataIdInfo, "searchKeys")
        tags = getattr_if(tool_i(),"tags")
        for tag in tags:
            ET.SubElement(searchKeys, "keyword").text = tag

        resConst = ET.SubElement(dataIdInfo, "resConst")
        Consts = ET.SubElement(resConst, "Consts")
        ET.SubElement(Consts, "useLimit").text = getattr_if(tool_i(),"limits", html=True)

        distInfo = ET.SubElement(metadata, "distInfo")
        distributor = ET.SubElement(distInfo, "distributor")
        distorFormat = ET.SubElement(distributor, "distorFormat")
        ET.SubElement(distorFormat, "formatName").text = "ArcToolbox Tool"

        mdHrLv = ET.SubElement(metadata, "mdHrLv")
        ET.SubElement(mdHrLv, "ScopeCd ", value = "005")
        ET.SubElement(metadata, "mdDateSt",Sync="TRUE").text = today

        tree = ET.ElementTree(metadata)
        outname = filename+"."+tool_name+".pyt.xml"
        tree.write(outname)
        print(outname+" done")


def write_meta_doc(pythontoolbox, filename):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    now = datetime.datetime.now().strftime("%H:%M:%S")

    metadata = ET.Element("metadata")
    esri = ET.SubElement(metadata, "Esri")
    ET.SubElement(esri, "CreaDate").text = today
    ET.SubElement(esri, "CreaTime").text = now
    ET.SubElement(esri, "ArcGISFormat").text = "1.0"
    ET.SubElement(esri, "SyncOnce").text = "TRUE"
    ET.SubElement(esri, "ModDate").text = today
    ET.SubElement(esri, "ModTime").text = now

    toolbox_toolbox = pythontoolbox()

    scaleRange = ET.SubElement(esri, "scaleRange")
    ET.SubElement(scaleRange, "minScale").text = getattr_if(toolbox_toolbox, "minScale")
    ET.SubElement(scaleRange, "maxScale").text = getattr_if(toolbox_toolbox, "maxScale")

    toolbox_alias = toolbox_toolbox.alias
    # / code repetition! resolve

    toolbox = ET.SubElement(metadata,
                            "toolbox",
                            name=filename,
                            alias=toolbox_alias)

    ET.SubElement(toolbox, "arcToolboxHelpPath").text = "c:\\program files\\arcgis\\pro\\Resources\\Help\\gp"
    ET.SubElement(toolbox, "toolsets")

    # code repetition! resolve
    dataIdInfo = ET.SubElement(metadata, "dataIdInfo")
    idCitation = ET.SubElement(dataIdInfo, "idCitation")
    ET.SubElement(idCitation, "resTitle").text = toolbox_alias
    # / code repetition! resolve

    ET.SubElement(dataIdInfo, "idPurp").text = getattr_if(toolbox_toolbox, "purpose", html=True)

    ET.SubElement(dataIdInfo, "idAbs").text = getattr_if(toolbox_toolbox, "abstract", html=True)
    # code repetition! resolve
    ET.SubElement(dataIdInfo, "idCitation")

    ET.SubElement(dataIdInfo, "idCredit").text = getattr_if(toolbox_toolbox,"credit")

    searchKeys = ET.SubElement(dataIdInfo, "searchKeys")

    tags = getattr_if(toolbox_toolbox,"tags")
    for tag in tags:
        ET.SubElement(searchKeys, "keyword").text = tag

    resConst = ET.SubElement(dataIdInfo, "resConst")
    Consts = ET.SubElement(resConst, "Consts")
    ET.SubElement(Consts, "useLimit").text = getattr_if(toolbox_toolbox,"limits", html=True)

    distInfo = ET.SubElement(metadata, "distInfo")
    distributor = ET.SubElement(distInfo, "distributor")
    distorFormat = ET.SubElement(distributor, "distorFormat")
    ET.SubElement(distorFormat, "formatName").text = "ArcToolbox Tool"

    mdHrLv = ET.SubElement(metadata, "mdHrLv")
    ET.SubElement(mdHrLv, "ScopeCd ", value="")
    ET.SubElement(metadata, "mdDateSt", Sync="TRUE").text = today
    # / code repetition! resolve

    tree = ET.ElementTree(metadata)
    outname = filename+".pyt.xml"
    tree.write(outname)
    print(outname+" done")


def main(pythontoolbox, filename):
    write_tool_doc(pythontoolbox, filename)
    write_meta_doc(pythontoolbox, filename)
