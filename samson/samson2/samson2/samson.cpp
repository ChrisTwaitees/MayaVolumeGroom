#include "samson.h"

MTypeId     SamsonNode::id(0x00000231);
MObject		SamsonNode::aInputCurve;
MObject		SamsonNode::aOutCurvesNum;
MObject		SamsonNode::aInMesh;
MObject		SamsonNode::aOutMesh;


SamsonNode::SamsonNode()
{
}

SamsonNode::~SamsonNode()
{
}

void* SamsonNode::creator()
{
	return new SamsonNode();
}

MStatus SamsonNode::initialize()
{
	MStatus status;
	MFnNumericAttribute nAttr;
	MFnTypedAttribute nTypedAttr;

	// OutPositions
	aOutCurvesNum = nAttr.create("curveBasePoint", "curveBasePoint", MFnNumericData::kFloat);
	nAttr.setArray(true);
	nAttr.setWritable(false);
	nAttr.setReadable(true);
	nAttr.setUsesArrayDataBuilder(true);
	addAttribute(aOutCurvesNum);

	// OutMesh
	aOutMesh = nTypedAttr.create("outMesh", "outMesh", MFnData::kMesh);
	nTypedAttr.setWritable(false);
	nTypedAttr.setReadable(true);
	addAttribute(aOutMesh);

	// Input Mesh
	aInMesh = nTypedAttr.create("inputMesh", "inputMesh", MFnMeshData::kMesh);
	nTypedAttr.setReadable(false);
	nTypedAttr.setWritable(true);
	addAttribute(aInMesh);
	attributeAffects(aInMesh, aOutMesh);

	// Input Curves
	aInputCurve = nTypedAttr.create("inputCurve", "inputCurve", MFnNurbsCurveData::kNurbsCurve, MObject::kNullObj);
	nTypedAttr.setReadable(false);
	nTypedAttr.setWritable(true);
	addAttribute(aInputCurve);
	attributeAffects(aInputCurve, aOutCurvesNum);

	return MS::kSuccess;
}

MStatus SamsonNode::connectionMade(const MPlug& plug, const MPlug& otherPlug, bool asSrc)
{
	MStatus status;
	MDagModifier DGModifier;
	
	
	// When Mesh Connected
	if (plug == aInMesh)
	{
	
		// Create New Mesh Trs Node 
		MObject newMeshTrsObj = DGModifier.createNode(MString("mesh"), MObject::kNullObj, &status);
		DGModifier.renameNode(newMeshTrsObj, MString("SamsonMeshTransform"));

		// Get New Mesh Shape Node
		MFnDagNode FnNewMeshTrs(newMeshTrsObj);
		MDagPath newMeshShapePath;
		FnNewMeshTrs.getPath(newMeshShapePath);
		newMeshShapePath.extendToShapeDirectlyBelow(0);

		DGModifier.renameNode(newMeshShapePath.node(), MString("SamsonMeshShape"));


		//MFnDependencyNode NewMeshShapeObjFn(newMeshShapePath.node());
		MFnDependencyNode NewMeshShapeObjFn(newMeshTrsObj);
		//MObject inNewMesh = NewMeshShapeObjFn.attribute(MString("inMesh"));
		MPlug dstPlug = NewMeshShapeObjFn.findPlug(MString("inMesh"), true, &status);

		// Get Own MeshOut Plug
		MPlug srcPlug(this->thisMObject(), SamsonNode::aOutMesh);

		DGModifier.connect(srcPlug, dstPlug);

		status = DGModifier.doIt();

	}
	else { return MS::kUnknownParameter; }
	return status;
}

MStatus SamsonNode::connectionBroken(const MPlug& plug, const MPlug& otherPlug, bool asSrc)
{
	MStatus status;
	// When Mesh Disconnected
	if (plug == aInMesh)
	{
		return MS::kUnknownParameter;
	}
	else { return MS::kUnknownParameter; }
	return status;
}

MStatus SamsonNode::compute(const MPlug& plug, MDataBlock& data)
{
	MStatus status;
	
	// Compute for
	if (plug == aOutMesh)
	{
		// Input Mesh
		MObject inputMeshInput = data.inputValue(aInMesh, &status).asMeshTransformed();
		MFnMesh FnInMesh(inputMeshInput);

		// Output Mesh
		MDataHandle outputMeshHandle = data.outputValue(aOutMesh, &status);

		// Duplicate InMesh for Output Mesh
		MFnMesh OutMeshFn;
		MFnMeshData dataCreator;
		MObject outMeshData = dataCreator.create();
		OutMeshFn.copy(inputMeshInput, outMeshData, &status);

		// Getting and Setting Input Mesh Points to Output Mesh Points
		MPointArray inputPnts;
		FnInMesh.getPoints(inputPnts, MSpace::kWorld);
		OutMeshFn.setPoints(inputPnts, MSpace::kWorld);

		// Setting Outputs
		outputMeshHandle.set(outMeshData);
		data.setClean(plug);
	}
	else if (plug == aOutCurvesNum)
	{
		// Input Curve 
		MObject inputCurveInput = data.inputValue(aInputCurve, &status).asNurbsCurveTransformed();
		MFnNurbsCurve FnInputCurve(inputCurveInput);

		// Input Curve CVs
		MPointArray cvs;
		FnInputCurve.getCVs(cvs, MSpace::kWorld);

		// Ouput Array
		MArrayDataHandle outputCurvesNumArray = data.outputArrayValue(aOutCurvesNum, &status);
		MArrayDataBuilder builder(nullptr, aOutCurvesNum, cvs.length(), &status);

		// Creating and setting attr per CV
		for (int cvNum = 0; cvNum < cvs.length(); cvNum++)
		{
			//get handle to attr
			MDataHandle outHandle = builder.addElement(cvNum);
			outHandle.set(float(cvNum));

		}

		// Setting Outputs
		outputCurvesNumArray.set(builder);
		outputCurvesNumArray.setAllClean();
		data.setClean(plug);
	}
	else { return MS::kUnknownParameter; }

	return MS::kSuccess;
}
