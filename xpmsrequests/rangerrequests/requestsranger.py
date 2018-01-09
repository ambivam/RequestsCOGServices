import time
import requests
import json
import os
import logging

from xpmsrequests.data import DataVariables
from xpmsrequests.rangerrequests import requestsrangerbase

class RangerReq(requestsrangerbase.RangerBase):

    def __init__(self):
        # Create the Logger
        super(RangerReq,self).__init__()
        self.logger = logging.getLogger(__name__)
    # *****************************************************************************************************
    # *****************************************************************************************************

    def getDataByJobId(self,JobId):
        self.logger.info('Into getDataByJobId method')
        jobIdUrl = DataVariables.RangerJobIdUrl+JobId
        self.logger.info('JobIdUrl is :'+jobIdUrl)
        status = 'in-progress'
        processStatus = 'process_status'

        try:
            count = 1
            while (count <= DataVariables.TimeOut):
                tempJson = requests.get(jobIdUrl).json()
                if(count > DataVariables.TimeOut):
                    self.logger.error('Time Count Exceeded')
                    return None
                if (tempJson[processStatus] != status):
                    print('Exited while')
                    self.logger.info('Returning Json :'+str(tempJson))
                    return tempJson
                if (tempJson[processStatus] == status):
                    self.logger.info('Into Sleep')
                    self.logger.info('Sleep Time is : '+str(DataVariables.PollTime))
                    time.sleep(DataVariables.PollTime)
                    count += 1
                    self.logger.info('count is :'+str(count))
        except:
            print('Unable to generate response')
            self.logger.error('Unable to generate response')


    # *****************************************************************************************************
    # *****************************************************************************************************

    def upLoadReq(self, imgUrl):

        self.logger.info('Into upLoadReq method')
        files = {'file': open(imgUrl, 'rb')}
        # self.logger.info('file is:'+str(files))
        response = requests.post(DataVariables.UploadUrl, files=files)
        self.logger.info('Response Json after uploading image is' + str(response.json()))
        if (response.status_code == 200):
            self.logger.info(
                'Status of Response returned after uploading the image is ' + str(response.status_code))
            return response.json()
        else:
            self.logger.error(
                'Status of Response returned after uploading the image is' + str(response.status_code))
            return None

    # ****************************************************************************************************
    # *****************************************************************************************************

    def insightIngest(self, uploadjson):
        self.logger.info('Into Insight Ingest method')
        jsonFileData = self.getJsonFileData(DataVariables.Insightingestjson)
        self.logger.info('The body Of insight Ingest Json Is :' + str(jsonFileData))
        jsonFileData['data']['file_path'][0] = uploadjson['metadata']['file_path']
        jsonFileData['data']['request_type'] = 'ingest_document'
        jsonFileData['entity_id'] = DataVariables.entityId
        jsonFileData['solution_id'] = DataVariables.solutionId

        self.logger.info(
            'Insight Ingest json after assigning metadata of Upload json and RequestType,EntityID and Solution Is is :' + str(
                jsonFileData))

        ingestFileJobID = self.getResponse(DataVariables.GetInsightURL, jsonFileData)
        self.logger.info('Job Id returned by insightIngest is :' + str(ingestFileJobID))
        return ingestFileJobID

    # *****************************************************************************************************

    def insightExtractDocumentMetadata(self,injestInsightJson):
        self.logger.info('Into insightExtractDocumentMetadata method')
        jsonFileData = self.getJsonFileData(DataVariables.GetInsightJson)
        self.logger.info('The body Of Getinsight Json Is :' + str(jsonFileData))
        #import pdb;pdb.set_trace()
        jsonFileData['data']['doc_id'] = injestInsightJson['result']['metadata']['insights'][0]['insight']['doc_id']
        print('$$$$$$$$$$$$$$The Doc Id Is $$$$$$$$$$$$$$$$$$',jsonFileData['data']['doc_id'])
        self.logger.info('$$$$$$$$$$$$$$The Doc Id Is $$$$$$$$$$$$$$$$$$'+ str(jsonFileData['data']['doc_id']))
        jsonFileData['data']['request_type'] = 'extract_document_metadata'
        jsonFileData['entity_id'] = DataVariables.entityId
        jsonFileData['solution_id'] = DataVariables.solutionId

        self.logger.info(
            'Insight json after assigning metadata of InsightIngest json and RequestType,EntityID and Solution Is is :' + str(
                jsonFileData))

        insightExtractDocumentMetadataJobID = self.getResponse(DataVariables.GetInsightURL, jsonFileData)
        self.logger.info('Job Id returned by insightIngest is :' + str(insightExtractDocumentMetadataJobID))
        return insightExtractDocumentMetadataJobID