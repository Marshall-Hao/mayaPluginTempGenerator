#pragma once
#include <maya/MArgDatabase.h>
#include <maya/MDoubleArray.h>

#include <maya/MFnTransform.h>
#include <maya/MGlobal.h>
#include <maya/MSelectionList.h>

#include <maya/MObject.h>
#include <maya/M{{detail_name}}.h>
#include <maya/MSyntax.h>
#include <maya/MVector.h>

class {{plugin_name}}Command : public M{{detail_name}}
{
public:
    {{plugin_name}}Command();
    virtual ~{{plugin_name}}Command() override;

    virtual MStatus doIt(const MArgList& args) override;

    virtual MStatus undoIt() override;
    virtual MStatus redoIt() override;
    virtual bool isUndoable() const override;

    // Static methods
    static void* Creator();
    static MString CommandName();

    static MSyntax CreateSyntax();

private:
    MObject mSelectionObj;

    bool mUndoable;

    bool mEdit;
    bool mQuery;

    //-----------------------------------------------------------------------------
    // translation command example
    //-----------------------------------------------------------------------------
    bool mTranslate;
    bool mVersion;

    // translation values before move
    MVector mOrigTranslation;
    // after
    MVector mNewTranslation;
    //-----------------------------------------------------------------------------
    // translation command example
    //-----------------------------------------------------------------------------

};