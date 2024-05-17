import maya.api.OpenMaya as om
import maya.api.OpenMayaRender as omr
import maya.api.OpenMayaUI as omui

import maya.cmds as cmds


def maya_useNewAPI():
    """
    Tell Maya this plugin uses the Python API 2.0.
    """
    pass

class {{plugin_name}}Node(omui.M{{detail_name}}):
    # save to maya ascii format
    TYPE_NAME = "{{plugin_name}}Node"
    # save to binary format
    TYPE_ID = om.MTypeId(0x0007f7f7f)
    DRAW_CLASSFICATION ="drawdb/geometry/{{plugin_name}}"
    DRAW_REGISTRANT_ID = "{{plugin_name}}Node"
    
    def __init__(self):
        super({{plugin_name}}Node,self).__init__()
        
    @classmethod
    def creator(cls):
        return {{plugin_name}}Node()
    
    @classmethod
    def initialize(cls):
        pass

"""
HellowWorld node example
"""
class {{plugin_name}}DrawOverride(omr.MPxDrawOverride):
    
    NAME = "{{plugin_name}}DrawOverride"
    
    def __init__(self,obj):
        super({{plugin_name}}DrawOverride,self).__init__(obj,None,False)
    
    # has to be include for the MPxDrawOverride class
    def prepareForDraw(self,obj_path,camera_path,frame_context,old_data):
        pass
    
    def supportedDrawAPIs(self):
        # can be used in all graphic engine
        return omr.MRenderer.kAllDevices
    
    def hasUIDrawables(self):
        return True
    
    def addUIDrawables(self,obj_path,draw_manager,frame_context,data):
        draw_manager.beginDrawable()
        draw_manager.text2d(om.MPoint(100,100),"Hello World!")
        draw_manager.endDrawable()
        
    @classmethod
    def creator(cls,obj):
        return {{plugin_name}}DrawOverride(obj)
"""
HellowWorld node example
"""

def initializePlugin(plugin):
    """
    """
    vendor = "{{author}}"
    version = "{{version}}"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)
    try:
        plugin_fn.registerNode({{plugin_name}}Node.TYPE_NAME,
                               {{plugin_name}}Node.TYPE_ID,
                               {{plugin_name}}Node.creator,
                               {{plugin_name}}Node.initialize,
                               om.MPxNode.kLocatorNode,
                               {{plugin_name}}Node.DRAW_CLASSFICATION)
    except:
        om.MGlobal.displayError("Failed to register node: {0}".format({{plugin_name}}Node.TYPE_NAME))
    """
    HellowWorld node example
    """
    try:
        omr.MDrawRegistry.registerDrawOverrideCreator({{plugin_name}}Node.DRAW_CLASSFICATION,
                                                      {{plugin_name}}Node.DRAW_REGISTRANT_ID,
                                                      {{plugin_name}}DrawOverride.creator)
    except:
        om.MGlobal.displayError("Failed to register draw override: {0}".format({{plugin_name}}DrawOverride.NAME))
    """
    HellowWorld node example
    """
def uninitializePlugin(plugin):
    """
    """
    plugin_fn = om.MFnPlugin(plugin)
    
          
    try:
        omr.MDrawRegistry.deregisterDrawOverrideCreator({{plugin_name}}Node.DRAW_CLASSFICATION,
                                                      {{plugin_name}}Node.DRAW_REGISTRANT_ID)
    except:
        om.MGlobal.displayError("Failed to deregister draw override: {0}".format({{plugin_name}}DrawOverride.NAME))
    
    
    try:
        plugin_fn.deregisterNode({{plugin_name}}Node.TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to deregister node: {0}".format({{plugin_name}}Node.TYPE_NAME))

if __name__ == "__main__":
    # refresh the new scene
    cmds.file(new=True,force=True)
    """
    HellowWorld node example
    """
    plugin_name = "{{plugin_name}}Node.py"

    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))
    
    
    cmds.evalDeferred('cmds.createNode("{{plugin_name}}")')
    """
    HellowWorld node example
    """