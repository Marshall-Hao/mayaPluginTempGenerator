#pragma once


#include <maya/M{{detail_name}}.h>  
//-----------------------------------------------------------------------------
// HelloWorld node example
//----------------------------------------------------------------------------- 
#include <maya/MPxDrawOverride.h>


class {{plugin_name}}DrawOverride : public MHWRender::MPxDrawOverride
{
public:
	virtual ~{{plugin_name}}DrawOverride() override;

	virtual MHWRender::DrawAPI supportedDrawAPIs() const override;

	virtual bool hasUIDrawables() const  override;
	virtual void addUIDrawables(const MDagPath& objPath, MHWRender::MUIDrawManager& drawManager, const MHWRender::MFrameContext& frameContext, const MUserData* data) override;

	virtual MUserData* prepareForDraw(const MDagPath& objPath, const MDagPath& cameraPath, const MHWRender::MFrameContext& frameContext, MUserData* oldData) override;


	// Static Methods
	static MHWRender::MPxDrawOverride* Creator(const MObject& obj);

private:
	{{plugin_name}}DrawOverride(const MObject& obj);
};

//-----------------------------------------------------------------------------
// HelloWorld node example
//----------------------------------------------------------------------------- 

class {{plugin_name}}Node : public M{{detail_name}}
{
public:
	{{plugin_name}}Node();
	virtual ~{{plugin_name}}Node() override;

	// static methods
	static void* Creator();
	static MStatus Initialize();

	static MTypeId GetTypeId();
	static MString GetTypeName();
	
	//-----------------------------------------------------------------------------
	// HelloWorld node example
	//----------------------------------------------------------------------------- 
	static MString GetDrawDbClassification();
	static MString GetDrawRegistrationId();
	//-----------------------------------------------------------------------------
	// HelloWorld node example
	//----------------------------------------------------------------------------- 


};