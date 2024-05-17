#pragma once

#include <maya/M{{detail_name}}.h>


class {{plugin_name}}Node : public M{{detail_name}}
{
public:
    {{plugin_name}}Node();
    virtual ~{{plugin_name}}Node() override;
    
    //-----------------------------------------------------------------------------
    // rolling node example
    //-----------------------------------------------------------------------------
    virtual MStatus compute(const MPlug& plug, MDataBlock& data) override;

    // Static Methods
    static void* Creator();
    static MStatus Initialize();

    static MTypeId GetTypeId();
    static MString GetTypeName();


private:
    // Static Variables
    //-----------------------------------------------------------------------------
    // rolling node example
    //-----------------------------------------------------------------------------
    static MObject distanceObj;
    static MObject radiusObj;

    static MObject rotationsObj;    
    //-----------------------------------------------------------------------------
    // rolling node example
    //-----------------------------------------------------------------------------
};
