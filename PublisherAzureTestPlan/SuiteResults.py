from robot.api import ResultVisitor
from Logger import logger
import Constants


class SuiteResults(ResultVisitor):
    def __init__(self, robotOutputPath):
        self.robotOutputPath = robotOutputPath
        self.suites = []

    def start_suite(self, suite):
        self.get_testcases_id_status(suite)

    def get_testcases_id_status(self, suite):
        tests_ids_status = {}
        tests_witout_ids = []
        global testplanId, suiteId
        testplanId = suiteId = None
        testcases = {}
        for s in suite.suites:
            if len(s.tests) > 0:
                for tc in s.tests:
                    infoTestCase = {}
                    try:
                        infoTestCase['id'] = SuiteResults.get_tags_with_prefixe(
                            tc, Constants.PREFIXE_TAG_TEST_ID)
                        infoTestCase['starttime'] = tc.starttime
                        infoTestCase['endtime'] = tc.endtime
                        infoTestCase['elapsedtime'] = tc.elapsedtime
                        infoTestCase['critical'] = tc.critical
                        infoTestCase['message'] = tc.message
                        infoTestCase['name'] = tc.name
                        infoTestCase["status"] = tc.status
                        infoTestCase["planId"] = SuiteResults.get_tags_with_prefixe(
                            tc, Constants.PREFIXE_TAG_TESTPLAN_ID)
                        infoTestCase["suiteId"] = SuiteResults.get_tags_with_prefixe(
                            tc, Constants.PREFIXE_TAG_SUITE_ID)
                        tests_ids_status[infoTestCase['id']
                                         ] = infoTestCase['status']
                        testcases[infoTestCase['id']] = infoTestCase
                        suiteId = SuiteResults.get_tags_with_prefixe(
                            tc, 'SUITE-')
                        testplanId = SuiteResults.get_tags_with_prefixe(
                            tc, 'TESTPLAN-')
                    except Exception as ex:
                        tests_witout_ids.append({"name": tc.name})
                        pass
                if len(tests_witout_ids):
                    logger.warning(
                        "\nSutie "+s.name+" ==> Tests without IDs:\n"+str(tests_witout_ids))
                self.suites.append({'name': s.name, 'id': suiteId, 'planId': testplanId, 'tests_ids_status': tests_ids_status,
                                   'tests_witout_ids': tests_witout_ids, 'testcases': testcases, 'starttime': suite.starttime, 'endtime': suite.endtime})

    def get_testcase_ids(self, suite):
        print(suite['tests_ids_status'])
        return [k for k in suite['tests_ids_status'].keys()]

    def get_tags_with_prefixe(testcase, tag_perfixe):
        try:
            if testcase.tags:
                id = [id for id in testcase.tags if str(id).startswith(
                    tag_perfixe)][0].split(tag_perfixe)[1]
                return id
        except Exception:
            raise Exception("Tag with prefix "+tag_perfixe +
                            " dosent exist in test case "+testcase.name)
