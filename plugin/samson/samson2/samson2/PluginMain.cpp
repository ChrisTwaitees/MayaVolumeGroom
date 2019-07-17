#include "samson.h"

#include <maya/MFnPlugin.h>

MStatus initializePlugin(MObject obj)
{
	MStatus status;

	MFnPlugin fnPlugin(obj, "Chris Thwaites", "1.0", "Any");

	status = fnPlugin.registerNode("samson",
		SamsonNode::id,
		SamsonNode::creator,
		SamsonNode::initialize);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	return MS::kSuccess;
}


MStatus uninitializePlugin(MObject obj)
{
	MStatus status;

	MFnPlugin fnPlugin(obj);

	status = fnPlugin.deregisterNode(SamsonNode::id);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	return MS::kSuccess;
}