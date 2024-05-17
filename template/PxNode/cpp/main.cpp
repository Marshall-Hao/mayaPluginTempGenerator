#include <maya/MFnPlugin.h>
#include <maya/MGlobal.h>
#include <maya/MIOStream.h>

#include "{{plugin_name}}Node.h"


MStatus initializePlugin(MObject pluginObj)
{
    const char* vendor = "{{author}}";
    const char* version = "{{version}}";
    const char* requiredApiVersion = "Any";

    MStatus status;

    MFnPlugin pluginFn(pluginObj, vendor, version, requiredApiVersion, &status);
    if (!status)
    {
        MGlobal::displayError("Failed to initialize plugin: " + status.errorString());
        return(status);
    }

    status = pluginFn.registerNode({{plugin_name}}Node::GetTypeName(),
        {{plugin_name}}Node::GetTypeId(),
        {{plugin_name}}Node::Creator,
        {{plugin_name}}Node::Initialize,
        {{plugin_name}}Node::kDependNode);
    if (!status)
    {
        MGlobal::displayError("Failed to register node: " + {{plugin_name}}Node::GetTypeName());
        return(status);
    }

    return(status);
}

MStatus uninitializePlugin(MObject pluginObj)
{
    MStatus status;

    MFnPlugin pluginFn(pluginObj);

    status = pluginFn.deregisterNode({{plugin_name}}Node::GetTypeId());
    if (!status)
    {
        MGlobal::displayError("Failed to deregister node: " + {{plugin_name}}Node::GetTypeName());
        return(status);
    }

    return(status);
}
