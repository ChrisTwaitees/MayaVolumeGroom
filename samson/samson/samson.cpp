#include "samson.h"

MTypeId     GaussianNode::id(0x00000231);
MObject     GaussianNode::aOutValue;
MObject     GaussianNode::aInValue;
MObject     GaussianNode::aMagnitude;
MObject     GaussianNode::aMean;
MObject     GaussianNode::aVariance;

GaussianNode::GaussianNode()
{
}


GaussianNode::~GaussianNode()
{
}


void* GaussianNode::creator()
{
	return new GaussianNode();
}


MStatus GaussianNode::compute(const MPlug& plug, MDataBlock& data)
{
	MStatus status;

	if (plug != aOutValue)
	{
		return MS::kUnknownParameter;
	}


	float inputValue = data.inputValue(aInValue, &status).asFloat();
	float magnitude = data.inputValue(aMagnitude, &status).asFloat();
	float mean = data.inputValue(aMean, &status).asFloat();
	float variance = data.inputValue(aVariance, &status).asFloat();
	if (variance <= 0.0f)
	{
		variance = 0.001f;
	}

	float xMinusB = inputValue - mean;
	float output = magnitude * exp(-(xMinusB * xMinusB) / (2.0f * variance));

	MDataHandle hOutput = data.outputValue(aOutValue, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	hOutput.setFloat(output);
	hOutput.setClean();
	data.setClean(plug);

	return MS::kSuccess;
}


MStatus GaussianNode::initialize()
{
	MStatus status;
	MFnNumericAttribute nAttr;

	aOutValue = nAttr.create("outValue", "outValue", MFnNumericData::kFloat);
	nAttr.setWritable(false);
	nAttr.setStorable(false);
	addAttribute(aOutValue);

	aInValue = nAttr.create("inValue", "inValue", MFnNumericData::kFloat);
	nAttr.setKeyable(true);
	addAttribute(aInValue);
	attributeAffects(aInValue, aOutValue);

	aMagnitude = nAttr.create("magnitude", "magnitude", MFnNumericData::kFloat);
	nAttr.setKeyable(true);
	addAttribute(aMagnitude);
	attributeAffects(aMagnitude, aOutValue);

	aMean = nAttr.create("mean", "mean", MFnNumericData::kFloat);
	nAttr.setKeyable(true);
	addAttribute(aMean);
	attributeAffects(aMean, aOutValue);

	aVariance = nAttr.create("variance", "variance", MFnNumericData::kFloat);
	nAttr.setKeyable(true);
	addAttribute(aVariance);
	attributeAffects(aVariance, aOutValue);

	return MS::kSuccess;
}
