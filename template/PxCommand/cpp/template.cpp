#include "{{plugin_name}}Command.h"


//-----------------------------------------------------------------------------
// STATIC CONSTANTS
//-----------------------------------------------------------------------------

static const MString MEL_COMMAND = "{{plugin_name}}Command";
//-----------------------------------------------------------------------------
// translation command example
//-----------------------------------------------------------------------------
static const char* TRANSLATE_FLAG[2] = {"-t","-translate"};
static const char* VERSION_FLAG[2] = {"-v","-version"};
//-----------------------------------------------------------------------------
// translation command example
//-----------------------------------------------------------------------------


//-----------------------------------------------------------------------------
// PUBLIC METHODS
//-----------------------------------------------------------------------------
{{plugin_name}}Command::{{plugin_name}}Command() :
    M{{detail_name}}(),
    mUndoable(false),
    mEdit(false),
    mQuery(false),
    mTranslate(false),
    mVersion(false)
{


}

{{plugin_name}}Command::~{{plugin_name}}Command()
{
}

MStatus {{plugin_name}}Command::doIt(const MArgList& args)
{
    MStatus status;

    MArgDatabase argData(syntax(), args, &status);

    
    if (!status)
    {
		MGlobal::displayError("Failed to parse arguments: " + status.errorString());
        return(status);
	}
    //-----------------------------------------------------------------------------
    // translation command example
    //-----------------------------------------------------------------------------
    MSelectionList selectionList;
    status = argData.getObjects(selectionList);

    if (!status)
	{ 
        MGlobal::displayError("Failed to get selection list: " + status.errorString());
		return(status);
    }

    // pass the first object in the selection list to the mSelectionObj
    selectionList.getDependNode(0, mSelectionObj);

    if (mSelectionObj.apiType() != MFn::kTransform)
    {
		MGlobal::displayError("Selected object is not a transform node");
		return(MStatus::kFailure);
	}

    mEdit = argData.isEdit();
    mQuery = argData.isQuery();

    mVersion = argData.isFlagSet(VERSION_FLAG[0]);
    mTranslate = argData.isFlagSet(TRANSLATE_FLAG[0]);
    
    if (mTranslate)
    {
        MFnTransform transformFn(mSelectionObj);

        mOrigTranslation = transformFn.getTranslation(MSpace::kTransform);

        if (mEdit)
        {   
            // set the new translation,get the values from the flag based on the index
            mNewTranslation = MVector(argData.flagArgumentDouble(TRANSLATE_FLAG[0], 0),
                									  argData.flagArgumentDouble(TRANSLATE_FLAG[0], 1),
                									  argData.flagArgumentDouble(TRANSLATE_FLAG[0], 2));

            mUndoable = true;

        }
    }
    //-----------------------------------------------------------------------------
    // translation command example
    //-----------------------------------------------------------------------------

    return(redoIt());
}

MStatus {{plugin_name}}Command::undoIt()
{   
    //-----------------------------------------------------------------------------
    // translation command example
    //-----------------------------------------------------------------------------
   MFnTransform transformFn(mSelectionObj);


   transformFn.setTranslation(mOrigTranslation, MSpace::kTransform);

    //-----------------------------------------------------------------------------
    // translation command example
    //-----------------------------------------------------------------------------
   return MS::kSuccess;
}

MStatus {{plugin_name}}Command::redoIt()
{   
    //-----------------------------------------------------------------------------
    // translation command example
    //-----------------------------------------------------------------------------
    MFnTransform transformFn(mSelectionObj);

    if (mQuery)
    {
        if (mTranslate)
        {
            double result[3];
            // store the original translation values in the result array
            mOrigTranslation.get(result);


            setResult(MDoubleArray(result,3));

        }
        else
        {
            MGlobal::displayError("Flag does not support query");
            return MS::kFailure;
        }
    }
    else if (mEdit)
    {   
        // set the new translation values if the translate flag is set
        if (mTranslate)
        {
            transformFn.setTranslation(mNewTranslation, MSpace::kTransform);
        }
        else
        {
            MGlobal::displayError("Flag does not support edit");
            return MS::kFailure;
        }
    }
    else if (mVersion)
    {
		setResult("1.0.0");
	}
    else
    {
        setResult(transformFn.name());
	}

    //-----------------------------------------------------------------------------
    // translation command example
    //-----------------------------------------------------------------------------
    return MS::kSuccess;
}

bool {{plugin_name}}Command::isUndoable() const
{
    return mUndoable;
}


//-----------------------------------------------------------------------------
// STATIC METHODS
//-----------------------------------------------------------------------------
void* {{plugin_name}}Command::Creator()
{
    return(new {{plugin_name}}Command());
}

MString {{plugin_name}}Command::CommandName()
{
    return(MEL_COMMAND);
}

MSyntax {{plugin_name}}Command::CreateSyntax()
{
    MSyntax syntax;

    syntax.enableEdit(true);
    syntax.enableQuery(true);
    //-----------------------------------------------------------------------------
    // translation command example
    //-----------------------------------------------------------------------------
    syntax.addFlag(TRANSLATE_FLAG[0], TRANSLATE_FLAG[1], MSyntax::kDouble, MSyntax::kDouble, MSyntax::kDouble);
    syntax.addFlag(VERSION_FLAG[0], VERSION_FLAG[1]);

    // can only accept one selected object
    syntax.setObjectType(MSyntax::kSelectionList, 1, 1);
    // will use the current selection list
    syntax.useSelectionAsDefault(true);
    //-----------------------------------------------------------------------------
    // translation command example
    //-----------------------------------------------------------------------------
    return syntax;
}
