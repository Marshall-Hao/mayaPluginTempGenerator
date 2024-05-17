#include <maya/MFnPlugin.h>
#include <maya/MGlobal.h>

#include "{{plugin_name}}Command.h"

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
    status = pluginFn.registerCommand({{plugin_name}}Command::CommandName(), {{plugin_name}}Command::Creator, {{plugin_name}}Command::CreateSyntax);
    if (!status)
    {
		MGlobal::displayError("Failed to register command: " + {{plugin_name}}Command::CommandName() + status.errorString());
		return(status);
	}


    return(status);
}

MStatus uninitializePlugin(MObject pluginObj)
{
    MStatus status;

    MFnPlugin pluginFn(pluginObj);

    status = pluginFn.deregisterCommand({{plugin_name}}Command::CommandName());
    if (!status)
    {
		MGlobal::displayError("Failed to deregister command: " + {{plugin_name}}Command::CommandName() + status.errorString());
		return(status);
	}

    return(status);
}
