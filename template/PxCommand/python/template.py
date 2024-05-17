import maya.api.OpenMaya as om

import maya.cmds as cmds


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass



class {{plugin_name}}Command(om.M{{detail_name}}):

    COMMAND_NAME = "{{plugin_name}}Command"
    
    VERSION_FLAG = ["-v", "-version"]
    
    """
    translation command example
    """
    TRANSLATE_FLAG = ["-t", "-translation", (om.MSyntax.kDouble,om.MSyntax.kDouble,om.MSyntax.kDouble)]
    
    NAME_FLAG = ["-n","-name"]
    """
    translation command example
    """
    def __init__(self):
        super({{plugin_name}}Command, self).__init__()
        self.undoable = False
        
    def doIt(self, arg_list):
        
        try:
            arg_db = om.MArgDatabase(self.syntax(), arg_list)
        except:
            self.displayError("Error parsing arguments")
            raise
        
        """
        translation command example
        """
        selection_list = arg_db.getObjectList()

        self.selected_obj = selection_list.getDependNode(0)
        # check if the selection node is transform node or not
        if self.selected_obj.apiType() != om.MFn.kTransform:
            raise RuntimeError("This command requires a transform node")
        
        self.edit = arg_db.isEdit
        self.query = arg_db.isQuery
        
        self.translate = arg_db.isFlagSet({{plugin_name}}Command.TRANSLATE_FLAG[0])
        if self.translate:
            transform_fn = om.MFnTransform(self.selected_obj)
            #get translate in the current space, this is a translate state (undo)
            self.orig_translation = transform_fn.translation(om.MSpace.kTransform)
            
            if self.edit:
                self.new_translation = [arg_db.flagArgumentDouble({{plugin_name}}Command.TRANSLATE_FLAG[0],0),
                                        arg_db.flagArgumentDouble({{plugin_name}}Command.TRANSLATE_FLAG[0],1),
                                        arg_db.flagArgumentDouble({{plugin_name}}Command.TRANSLATE_FLAG[0],2)]
                
                self.undoable = True
            
        self.version = arg_db.isFlagSet({{plugin_name}}Command.VERSION_FLAG[0])
        """
        translation command example
        """
        self.redoIt()
            
    def undoIt(self):
        """
        translation command example
        """
        # will record each stack obj state
        transform_fn =  om.MFnTransform(self.selected_obj)
        # so it will always relate to that stack attr state value
        transform_fn.setTranslation(om.MVector(self.orig_translation),om.MSpace.kTransform)
        """
        translation command example
        """

    def redoIt(self):
        """
        translation command example
        """
        transform_fn = om.MFnTransform(self.selected_obj)
        if self.query:
            if self.translate:
                self.setResult(self.orig_translation)
            else:
                raise RuntimeError("Flag does not support query")
                
        elif self.edit:
            if self.translate:
                # convert to a vector type (c++ binding)
                transform_fn.setTranslation(om.MVector(self.new_translation),om.MSpace.kTransform)
            else:
                raise RuntimeError("Flag does not support edit")
        elif self.version:
            self.setResult("1.0.0")
        else:
            self.setResult(transform_fn.name())
        """
        translation command example
        """
    def isUndoable(self):
        return self.undoable

    @classmethod
    def creator(cls):
        return {{plugin_name}}Command()

    @classmethod
    def create_syntax(cls):

        syntax = om.MSyntax()
        syntax.enableEdit = True
        syntax.enableQuery = True
        """
        translation command example
        """
        # Add flags here
        # pointing to the args list ,optimized way
        syntax.addFlag(*cls.VERSION_FLAG)
        syntax.addFlag(*cls.TRANSLATE_FLAG)
        """
        translation command example
        """
        
        """
        translation command example
        """
        syntax.setObjectType(om.MSyntax.kSelectionList,1,1)
        syntax.useSelectionAsDefault(True)
        """
        translation command example
        """
     
        return syntax



def initializePlugin(plugin):
    """
    """
    vendor = "{{author}}"
    version = "{{version}}"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)
    try:
        plugin_fn.registerCommand({{plugin_name}}Command.COMMAND_NAME, {{plugin_name}}Command.creator, {{plugin_name}}Command.create_syntax)
    except:
        om.MGlobal.displayError("Failed to register command: {0}".format({{plugin_name}}Command.COMMAND_NAME))


def uninitializePlugin(plugin):
    """
    """
    plugin_fn = om.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand({{plugin_name}}Command.COMMAND_NAME)
    except:
        om.MGlobal.displayError("Failed to deregister command: {0}".format({{plugin_name}}Command.COMMAND_NAME))


if __name__ == "__main__":

    cmds.file(new=True, force=True)
    """
    translation command example
    """
    plugin_name = "{{plugin_name}}Command.py"
    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))
    
    cmds.evalDeferred('cmds.polyCube()')
    """
    translation command example
    """