#include "{{plugin_name}}Node.h"

//-----------------------------------------------------------------------------
// PUBLIC METHODS
//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------
// HelloWorld node example
//----------------------------------------------------------------------------- 
{{plugin_name}}DrawOverride::~{{plugin_name}}DrawOverride()
{
}

MHWRender::DrawAPI {{plugin_name}}DrawOverride::supportedDrawAPIs() const
{
    return(MHWRender::kAllDevices);
}

bool {{plugin_name}}DrawOverride::hasUIDrawables() const
{
    return(true);
}

void {{plugin_name}}DrawOverride::addUIDrawables(const MDagPath& objPath, MHWRender::MUIDrawManager& drawManager, const MHWRender::MFrameContext& frameContext, const MUserData* data)
{
    drawManager.beginDrawable();

    drawManager.text2d(MPoint(100, 100), "Hello World");

    drawManager.endDrawable();
}

MUserData* {{plugin_name}}DrawOverride::prepareForDraw(const MDagPath& objPath, const MDagPath& cameraPath, const MHWRender::MFrameContext& frameContext, MUserData* oldData)
{
    return(nullptr);
}

//-----------------------------------------------------------------------------
// STATIC METHODS
//-----------------------------------------------------------------------------
MHWRender::MPxDrawOverride* {{plugin_name}}DrawOverride::Creator(const MObject& obj)
{
    return(new {{plugin_name}}DrawOverride(obj));
}


//-----------------------------------------------------------------------------
// PRIVATE METHODS
//-----------------------------------------------------------------------------
{{plugin_name}}DrawOverride::{{plugin_name}}DrawOverride(const MObject& obj) :
    MHWRender::MPxDrawOverride(obj, nullptr)
{
}

//-----------------------------------------------------------------------------
// HelloWorld node example
//----------------------------------------------------------------------------- 
//-----------------------------------------------------------------------------
// CONSTANTS
//-----------------------------------------------------------------------------
static const MTypeId TYPE_ID = MTypeId(0x0007F7F7);
static const MString TYPE_NAME = "{{plugin_name}}Node";
//-----------------------------------------------------------------------------
// HelloWorld node example
//----------------------------------------------------------------------------- 
static const MString DRAW_DB_CLASSIFICATION = "drawdb/geometry/{{plugin_name}}";
static const MString DRAW_REGISTRATION_ID = "{{plugin_name}}Plugin";

//-----------------------------------------------------------------------------
// HelloWorld node example
//----------------------------------------------------------------------------- 

//-----------------------------------------------------------------------------
// PUBLIC METHODS
//-----------------------------------------------------------------------------
{{plugin_name}}Node::{{plugin_name}}Node() :
    MPxLocatorNode()
{
}

{{plugin_name}}Node::~{{plugin_name}}Node()
{
}


//-----------------------------------------------------------------------------
// STATIC METHODS
//-----------------------------------------------------------------------------
void* {{plugin_name}}Node::Creator()
{
    return(new {{plugin_name}}Node());
}

MStatus {{plugin_name}}Node::Initialize()
{
    return(MS::kSuccess);
}

MTypeId {{plugin_name}}Node::GetTypeId()
{
    return(TYPE_ID);
}

MString {{plugin_name}}Node::GetTypeName()
{
    return(TYPE_NAME);
}
//-----------------------------------------------------------------------------
// HelloWorld node example
//----------------------------------------------------------------------------- 
MString {{plugin_name}}Node::GetDrawDbClassification()
{
    return(DRAW_DB_CLASSIFICATION);
}

MString {{plugin_name}}Node::GetDrawRegistrationId()
{
    return(DRAW_REGISTRATION_ID);
}

//-----------------------------------------------------------------------------
// HelloWorld node example
//----------------------------------------------------------------------------- 