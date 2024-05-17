#include "{{plugin_name}}Node.h"

#include <maya/MFnNumericAttribute.h>
#include <maya/MFnUnitAttribute.h>

//-----------------------------------------------------------------------------
// CONSTANTS
//-----------------------------------------------------------------------------
static const MTypeId TYPE_ID = MTypeId(0x0007F8F9);
static const MString TYPE_NAME = "{{plugin_name}}Node";


//-----------------------------------------------------------------------------
// STATIC VARIABLES
//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------
// rolling node example
//-----------------------------------------------------------------------------
MObject {{plugin_name}}Node::distanceObj;
MObject {{plugin_name}}Node::radiusObj;
MObject {{plugin_name}}Node::rotationsObj;
//-----------------------------------------------------------------------------
// rolling node example
//-----------------------------------------------------------------------------


//-----------------------------------------------------------------------------
// PUBLIC METHODS
//-----------------------------------------------------------------------------
{{plugin_name}}Node::{{plugin_name}}Node() :
    M{{detail_name}}()
{
}

{{plugin_name}}Node::~{{plugin_name}}Node()
{
}

MStatus {{plugin_name}}Node::compute(const MPlug& plug, MDataBlock& data)
{   
    //-----------------------------------------------------------------------------
    // rolling node example
    //-----------------------------------------------------------------------------
    if (plug == rotationsObj)
    {
		double distance  = data.inputValue(distanceObj).asDouble();
        double radius = data.inputValue(radiusObj).asDouble();

        double rotations = 0.0;
        if (radius != 0.0)
        {
			rotations = distance / radius;
		}

        MDataHandle rotationsDataHandle = data.outputValue(rotationsObj);
        rotationsDataHandle.setDouble(rotations);
	    
        data.setClean(rotationsObj);

	}
    //-----------------------------------------------------------------------------
    // rolling node example
    //-----------------------------------------------------------------------------
    return(MS::kSuccess);
}


//-----------------------------------------------------------------------------
// STATIC METHODS
//-----------------------------------------------------------------------------
void* {{plugin_name}}Node::Creator()
{
    return(new {{plugin_name}}Node());
}

MStatus {{plugin_name}}Node::Initialize()
{   //-----------------------------------------------------------------------------
    // rolling node example
    //-----------------------------------------------------------------------------
    MFnNumericAttribute numericAttr;

    distanceObj = numericAttr.create("distance", "dist", MFnNumericData::kDouble, 0.0);
    numericAttr.setKeyable(true);
    numericAttr.setReadable(false);
    radiusObj = numericAttr.create("radius", "rad", MFnNumericData::kDouble, 0.0);
    numericAttr.setKeyable(true);
    numericAttr.setReadable(false);

    MFnUnitAttribute unitAttr;
    rotationsObj = unitAttr.create("rotations", "rot", MFnUnitAttribute::kAngle, 0.0);

    addAttribute(distanceObj);
    addAttribute(radiusObj);
    addAttribute(rotationsObj);

    attributeAffects(distanceObj, rotationsObj);
    attributeAffects(radiusObj, rotationsObj);
    //-----------------------------------------------------------------------------
    // rolling node example
    //-----------------------------------------------------------------------------

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
