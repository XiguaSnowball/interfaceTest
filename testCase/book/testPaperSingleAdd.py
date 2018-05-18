# coding=utf-8
import unittest
import paramunittest
from utils import commonFun
from utils.Log import MyLog
import readConfig as readConfig
from utils import configHttp as configHttp
import json
from utils import configDB

singleAdd_xls = commonFun.get_xls("API.xls", "sheet2")

localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
localConfigDB = configDB.MyDB()


@paramunittest.parametrized(*singleAdd_xls)
class PaperSingleAdd(unittest.TestCase):
    def setParameters(self, case_name, params, method, status, msg):
        """
        set params
        :param case_name:
        :param params
        :param method:
        :param status:
        :param msg:
        :return:
        """

        self.case_name = str(case_name)
        self.params = json.loads(params)
        self.method = str(method)
        self.status = int(status)
        self.msg = str(msg)
        self.response = ''
        self.info = ''
        self.data = {}

    def description(self):
        """

        :return:
        """
        self.case_name

    def setUp(self):
        """
        :return:
        """
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()

    def testPaperSingleAdd(self):
        """
        test body
        :return:
        """
        # set uel
        self.log.build_out_info_line('--------Case Start----------------')
        self.url = commonFun.get_url_from_xml('paperSingleAdd')
        localConfigHttp.set_url(self.url)

        # set params
        if self.params == '' or self.params is None:
            params = None
        elif self.params == 'null':
            params = {"params": ""}
        else:
            params = self.params

        localConfigHttp.set_params(params)

        # get http
        self.response = localConfigHttp.postWithJson()

        # check result
        self.checkResult()

    def tearDown(self):
        """

        :return:

        """
        self.log.build_out_info_line('-------------Case End----------------')

    def checkResult(self):
        # print(self.response)
        self.info = json.loads(self.response.text)
        commonFun.show_return_msg(self.response)
        status = self.info['status']
        msg = self.info['msg']
        # data = self.info['data']
        insert_id = commonFun.get_value_from_return_json(self.info, "data", "insert_id")

        self.log.build_case_line(self.case_name, self.info['status'], self.info['msg'], str(self.info['data']))

        if status == 0:
            try:
                # 比较status
                self.log.build_out_info_line("比较status")
                self.assertEqual(status, self.status, msg='status与预期不同')
                self.log.build_out_info_line('status与预期相同')

                try:
                    sql = commonFun.get_sql('book', 'book', 'select_book_id')
                    # 生成带参数的sql
                    self.cursor = localConfigDB.executeSQL(sql, insert_id)
                    # 获取查询结果
                    results = localConfigDB.get_one(self.cursor)
                    # 比较查询结果，拿生成的id进行对比
                    self.log.build_out_info_line("与库中结果比较")
                    self.assertEqual(int(insert_id), results[0], msg='结果不一致，单卷添加失败')
                    self.log.build_out_info_line('结果一致，单卷添加成功')
                except:
                    self.log.build_out_error_line()
                    self.assertEqual(int(insert_id), results[0])

                localConfigDB.closeDB()
            except:
                self.log.build_out_error_line()
                self.assertEqual(status, self.status)

        if status == 1:
            self.assertEqual(self.info['status'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
            # if self.case_name == 'register_EmailExist':
            #     # delete register user from db
            #     sql = commonFun.get_sql('newsitetest', 'rs_member', 'delete_user')
            #     localConfigDB.executeSQL(sql, self.email)
            #     localConfigDB.closeDB()

            # try:
            #     # 执行SQL语句
            #     cursor.execute(sql)
            #     # 获取所有记录列表
            #     results = cursor.fetchall()
            #     for row in results:
            #         fname = row[0]
            #         lname = row[1]
            #         age = row[2]
            #         sex = row[3]
            #         income = row[4]
            #         # 打印结果
            #         print （"fname=%s,lname=%s,age=%d,sex=%s,income=%d" (fname, lname, age, sex, income )）
            # except:
            #     print （"Error: unable to fecth data"）
