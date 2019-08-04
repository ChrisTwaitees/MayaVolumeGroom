#ifndef SAMSONNODE_H
#define SAMSONNODE_H

#include <maya/MGlobal.h>
#include <maya/MPxNode.h>
#include <maya/MPxDeformerNode.h>
#include <maya/MItGeometry.h>

#include <maya/MFnDependencyNode.h>
#include <maya/MDagModifier.h>
#include <maya/MDagPath.h>
#include <maya/MFnDagNode.h>


#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>

#include <maya/MFnMesh.h>
#include <maya/MFnMeshData.h>

#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsCurveData.h>

#include <maya/MString.h>

#include <maya/MPlug.h>
#include <maya/MPointArray.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MArrayDataBuilder.h>

#include <string.h>
#include <maya/MIOStream.h>
#include <math.h>


class SamsonNode : public MPxNode
{
public:
	SamsonNode();
	virtual				~SamsonNode();
	static  void* creator();
	static  MStatus		initialize();

	virtual MStatus     compute(const MPlug& plug, MDataBlock& data);
	virtual MStatus		connectionMade(const MPlug& plug, const MPlug& otherPlug, bool asSrc);
	virtual MStatus		connectionBroken(const MPlug& plug, const MPlug& otherPlug, bool asSrc);


	static MTypeId	id;
	static MObject  aOutCurvesNum;
	static MObject  aOutMesh;

	static MObject  aInputCurve;

	static MObject  aInMesh;

};

#endif
