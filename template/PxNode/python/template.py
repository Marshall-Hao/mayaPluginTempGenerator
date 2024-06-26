import maya.api.OpenMaya as om

import maya.cmds as cmds


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


class {{plugin_name}}Node(om.MPxNode):

    TYPE_NAME = "{{plugin_name}}Node"
    TYPE_ID = om.MTypeId(0x0007F7F9)
    
    distance_obj = None
    radius_obj = None
    
    rotation_obj = None

    def __init__(self):
        super({{plugin_name}}Node, self).__init__()

    def compute(self, plug, data):
        """
        Rolling node example
        """
        if plug == self.rotation_obj:
            distance = data.inputValue({{plugin_name}}Node.distance_obj).asDouble()
            radius = data.inputValue({{plugin_name}}Node.radius_obj).asDouble()
                
            # handle edge condition
            if radius == 0:
                rotation = 0
            else:
                rotation = distance / radius
            
            rotation_data_handle = data.outputValue({{plugin_name}}Node.rotation_obj)
            rotation_data_handle.setDouble(rotation)
            
            data.setClean(plug)
        """
        Rolling node example
        """
    @classmethod
    def creator(cls):
        return {{plugin_name}}Node()

    @classmethod
    def initialize(cls):
        # normal numerical attr
        """
        Rolling node example
        """
        numeric_attr = om.MFnNumericAttribute()
        
        cls.distance_obj = numeric_attr.create("distance","dist",om.MFnNumericData.kDouble,0.0)
        numeric_attr.readable = False
        numeric_attr.keyable = True

        cls.radius_obj = numeric_attr.create("radius","rad",om.MFnNumericData.kDouble,0.0)
        numeric_attr.readable = False
        numeric_attr.keyable = True
        
        # special  unit
        unit_attr = om.MFnUnitAttribute()
        cls.rotation_obj = unit_attr.create("rotation","rot",om.MFnUnitAttribute.kAngle,0.0)
        unit_attr.writable = False
        
        cls.addAttribute(cls.distance_obj)
        cls.addAttribute(cls.radius_obj)
        cls.addAttribute(cls.rotation_obj)
        
        cls.attributeAffects(cls.distance_obj,cls.rotation_obj)
        cls.attributeAffects(cls.radius_obj,cls.rotation_obj)
        
        """
        Rolling node example
        """
def initializePlugin(plugin):
    """
    Entry point for a plugin.
    """
    vendor = "{{author}}"
    version = "{{version}}"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)
    try:
        plugin_fn.registerNode({{plugin_name}}Node.TYPE_NAME,              # name of the node
                               {{plugin_name}}Node.TYPE_ID,                # unique id that identifies node
                               {{plugin_name}}Node.creator,                # function/method that returns new instance of class
                               {{plugin_name}}Node.initialize,             # function/method that will initialize all attributes of node
                               om.MPxNode.kDependNode)             # type of node to be registered
    except:
        om.MGlobal.displayError("Failed to register node: {0}".format({{plugin_name}}Node.TYPE_NAME))

def uninitializePlugin(plugin):
    """
    Exit point for a plugin.
    """
    # always remember deregister
    plugin_fn = om.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterNode({{plugin_name}}Node.TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to unregister node: {0}".format({{plugin_name}}Node.TYPE_NAME))


if __name__ == "__main__":
    """
    For Development Only
    """

    # Any code required before unloading the plug-in (e.g. creating a new scene)
    cmds.file(new=True, force=True)
    """
    Rolling node example
    """
    # Reload the plugin
    plugin_name = "{{plugin_name}}Node.py"

    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))
    """
    Rolling node example
    """

