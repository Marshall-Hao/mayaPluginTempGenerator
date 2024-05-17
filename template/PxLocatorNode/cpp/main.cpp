#include <maya/MDrawRegistry.h>
#include <maya/MFnPlugin.h>
#include <maya/MGlobal.h>

#include "{{plugin_name}}Node.h"


MStatus initializePlugin(MObject pluginObj)
{
    const char* vendor = "{{arthor}}";
    const char* version = "{{version}}";
    const char* requiredApiVersion = "Any";

    MStatus status;

    MFnPlugin pluginFn(pluginObj, vendor, version, requiredApiVersion, &status);
    if (!status)
    {
        MGlobal::displayError("Failed to initialize plugin: " + status.errorString());
        return(status);
    }

    MString drawDbClassification = {{plugin_name}}Node::GetDrawDbClassification();

    status = pluginFn.registerNode({{plugin_name}}Node::GetTypeName(),
        {{plugin_name}}Node::GetTypeId(),
        {{plugin_name}}Node::Creator,
        {{plugin_name}}Node::Initialize,
        {{plugin_name}}Node::kLocatorNode,
        &drawDbClassification);
    if (!status)
    {
        MGlobal::displayError("Failed to register hello world node.");
        return(status);
    }
    //-----------------------------------------------------------------------------
    // HelloWorld node example
    //----------------------------------------------------------------------------- 
    status = MHWRender::MDrawRegistry::registerDrawOverrideCreator({{plugin_name}}Node::GetDrawDbClassification(), {{plugin_name}}Node::GetDrawRegistrationId(), {{plugin_name}}DrawOverride::Creator);
    if (!status)
    {
        MGlobal::displayError("Failed to register hello world draw override.");
        return(status);
    }
    //-----------------------------------------------------------------------------
    // HelloWorld node example
    //----------------------------------------------------------------------------- 
    return(status);
}

MStatus uninitializePlugin(MObject pluginObj)
{
    MStatus status;

    MFnPlugin pluginFn(pluginObj);

    status = MHWRender::MDrawRegistry::deregisterDrawOverrideCreator({{plugin_name}}Node::GetDrawDbClassification(), {{plugin_name}}Node::GetDrawRegistrationId());
    if (!status)
    {
        MGlobal::displayError("Failed to deregister hello world draw override.");
        return(status);
    }

    status = pluginFn.deregisterNode({{plugin_name}}Node::GetTypeId());
    if (!status)
    {
        MGlobal::displayError("Failed to deregister hello world node.");
        return(status);
    }

    return(status);
}
