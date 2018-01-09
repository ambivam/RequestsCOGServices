import pytest
import os
import json
import  logging
import allure

from xpmsrequests.reqscripts import  CogXRequests
from xpmsrequests.data import DataVariables

logger = logging.getLogger(__name__)


#*************************************************
def upload(filename):
    logger.info('**********************************************************' )
    result = False
    try:
        logger.info('Testing upload of Image')
        reqTest = CogXRequests.CogXReq()
        filePath = os.path.abspath(__file__ + "/../../data/images") + '/'
        logger.info('FilePath is : '+filePath+filename)
        uploadResponseJson = reqTest.upLoadReq(filePath + filename)

        if (uploadResponseJson['status']['success'] == True):
            result = True
            logger.info('Status of returned json of upload image result is ' + str(uploadResponseJson['status']))

        assert True, result
        logger.info('test_uploadreq method passed')
        return uploadResponseJson
    except:
        logger.error('Status of returned json of upload image result is ' + str(uploadResponseJson['status']))
        logger.error('Upload of Image failed')
        logger.info('**********************************************************')
        assert True==result

    logger.info('**********************************************************')


#*************************************************
def mimeTypeClassifier(uploadJson):
    logger.info('**********************************************************')
    result = False
    try:
        logger.info('Testing MimeTypeClassifier')
        reqTest = CogXRequests.CogXReq()

        logger.info('Upload Response Json is :'+str(uploadJson))
        JobId = reqTest.mimeTypeClassifier(uploadJson)
        #logger.info('The test_MimeTypeClassifier Job Id Is :'+str(JobId))

        if (JobId != None):
            result = True

        assert True, result
        logger.info('Testing MimeTypeClassifier method passed')
        logger.info('**********************************************************')
        return JobId
    except:
        logger.error('result =' + str(result))
        logger.error('Testing MimeTypeClassifier method failed')
        logger.info('**********************************************************')
        assert True == result

#*************************************************
def classify(mimeTypeJobIdentifier):
    logger.info('**********************************************************')
    result = False
    try:
        logger.info('Testing Classify Method')
        logger.info('To Test The generated MimetypeClassifier Json after submitting the MimeType Job Id and to return the JobID generated by Classify method')

        logger.info('CogXRequests.CogXReq()')
        reqTest = CogXRequests.CogXReq()

        mimetypeclassifierjson = reqTest.getDataByJobId(mimeTypeJobIdentifier)
        logger.info('MimeType Classifier Json returned after submitting MimeTypeJobIdentifier is:'+str(mimetypeclassifierjson))
        classifyJobId = reqTest.classify(mimetypeclassifierjson)
        logger.info('JobIdentifier returned by Classify method is :'+str(classifyJobId))

        if (classifyJobId != None):
            result = True

        assert True, result
        logger.info('Classify method passed')
        logger.info('**********************************************************')
        return classifyJobId
    except:
        logger.error('result =' + str(result))
        logger.error('test_classify method failed')
        logger.info('**********************************************************')
        assert True == result
        # assert True, result


#**************************************************
def preProcess(classifyJobIdentifier):
    logger.info('**********************************************************')
    result = False
    try:
        logger.info('Testing Preprocess Method')
        logger.info('To Test The generated Classify Json after submitting the Classify Job Id and JobID generated by PreProcess method')
        reqTest = CogXRequests.CogXReq()
        classifyJson = reqTest.getDataByJobId(classifyJobIdentifier)
        logger.info('Classify Json returned after submitting classifyJobIdentifier is:' + str(classifyJson))
        preprocessJobID = reqTest.preProcess(classifyJson)
        logger.info('JobIdentifier returned by preProcess method is :' + str(preprocessJobID))
        if (preprocessJobID != None):
            result = True
        assert True, result
        logger.info('preprocess method passed')
        logger.info('**********************************************************')
        return preprocessJobID
    except:
        logger.error('result =' + str(result))
        logger.error('Preprocess method failed')
        logger.info('**********************************************************')
        assert True == result
        # assert True, result
#**********************************************
def slicing(preProcessJobIdentifier,tempData):
    logger.info('**********************************************************')
    result = False
    try:
        logger.info('Testing Slicing Method')
        logger.info('To Test The generated PreProcess Json after submitting the Preprocess Job Id and JobID generated by Slice method')
        reqTest = CogXRequests.CogXReq()
        preProcessJson = reqTest.getDataByJobId(preProcessJobIdentifier)
        logger.info('Preprocess Json returned after submitting preProcessJobIdentifier is:' + str(preProcessJson))
        sliceJobIdentfier = reqTest.slice(preProcessJson,tempData)
        logger.info('JobIdentifier returned by Slicing method is :' + str(sliceJobIdentfier))
        if (sliceJobIdentfier != None):
            result = True
        assert True, result
        logger.info('Slice method passed')
        logger.info('**********************************************************')
        return sliceJobIdentfier
    except:
        logger.error('result =' + str(result))
        logger.error('slice method failed')
        logger.info('**********************************************************')
        assert True == result
        # assert True, result

#***********************************************
def ocr(sliceJobIdentfier):
    logger.info('**********************************************************')
    result = False
    try:
        logger.info('Testing Ocr method')
        logger.info('To Test The generated Slice Json after submitting the Slice Job Id and JobID generated by Ocr method')
        reqTest = CogXRequests.CogXReq()
        sliceJson = reqTest.getDataByJobId(sliceJobIdentfier)
        logger.info('Slice Json returned after submitting sliceJobIdentfier is:' + str(sliceJson))
        ocrJobIdentifier = reqTest.ocr(sliceJson)
        logger.info('JobIdentifier returned by Ocr method is :' + str(ocrJobIdentifier))
        if (ocrJobIdentifier != None):
            result = True
        assert True, result
        logger.info('Ocr method passed')
        return ocrJobIdentifier
    except:
        logger.error('result =' + str(result))
        logger.error('test_slice method failed')
        logger.info('**********************************************************')
        assert True == result
        # assert True, result

#***********************************************
#***********************************************
#To Validate The Json Returned By Upload Request
#***********************************************
@pytest.allure.severity(pytest.allure.severity_level.MINOR)
@pytest.allure.step('To Test The Request Uploading test_uploadreq')
@allure.feature('Feature1')
@allure.story('Smoke','Regression','upload')
def test_uploadreq():
    upload(DataVariables.CmsImage)

#****************************************************
#To Validate The JobId returned by MimeTypeClassifier
#****************************************************
@pytest.allure.severity(pytest.allure.severity_level.CRITICAL)
@pytest.allure.step('To Test The JobId returned by MimeTypeClassifier test_MimeTypeClassifier')
@allure.feature('Feature1')
@allure.story('Regression','mimeclassifier')
def test_MimeTypeClassifier():
    mimeTypeClassifier(upload(DataVariables.CmsImage))
#****************************************************
#To Validate The JobId returned by Classifier
#****************************************************
@pytest.allure.severity(pytest.allure.severity_level.CRITICAL)
@pytest.allure.step('To Test The JobId returned by Classifier test_classify')
@allure.feature('Feature1')
@allure.story('Smoke','Regression','classify')
def test_classify():
    classify(mimeTypeClassifier(upload(DataVariables.CmsImage)))
#****************************************************
#To Validate The JobId returned by PreProcess
#****************************************************
@pytest.allure.severity(pytest.allure.severity_level.CRITICAL)
@pytest.allure.step('To Test The JobId returned by PreProcess test_preprocess')
@allure.feature('Feature1')
@allure.story('Smoke','Regression','preprocess')
def test_preprocess():
    preProcess(classify(mimeTypeClassifier(upload(DataVariables.CmsImage))))
#****************************************************
#To Validate The JobId returned by Slice
#****************************************************
@pytest.allure.severity(pytest.allure.severity_level.CRITICAL)
@pytest.allure.step('To Test The JobId returned by Slice test_slice')
@allure.feature('Feature1')
@allure.story('Smoke','Regression','slicing')
def test_slice():
    logger.info('Temp data is :'+DataVariables.tempData)
    slicing(preProcess(classify(mimeTypeClassifier(upload(DataVariables.CmsImage)))),DataVariables.tempData)

#****************************************************
#To Validate The JobId returned by ocr
#****************************************************
@pytest.allure.severity(pytest.allure.severity_level.CRITICAL)
@pytest.allure.step('To Test The JobId returned by ocr test_ocr')
@allure.feature('Feature1')
@allure.story('Smoke','Regression','ocr')
def test_ocr():
    ocr(slicing(preProcess(classify(mimeTypeClassifier(upload(DataVariables.CmsImage)))),DataVariables.tempData))

#****************************************************
@pytest.allure.severity(pytest.allure.severity_level.CRITICAL)
@pytest.allure.step('To Test The JobId returned by ocr test_ocr jpg')
@allure.feature('Feature1')
@allure.story('Smoke','Regression','ocrjpg')
def test_ocr_jpeg():
    ocr(slicing(preProcess(classify(mimeTypeClassifier(upload(DataVariables.JpgImage)))),DataVariables.tempDataJpg))

#****************************************************