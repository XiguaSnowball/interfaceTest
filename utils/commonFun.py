import readConfig as readConfig
import os
from xlrd import open_workbook
from xml.etree import ElementTree as ElementTree
from utils import configHttp as configHttp
from utils.Log import MyLog as Log
import json
import requests

localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir
localConfigHttp = configHttp.ConfigHttp()
log = Log.get_log()
logger = log.get_logger()

caseNo = 0


# ****************************** 获取登录session ********************************
def get_login_session():
    """
    get login session
    :return:
    """
    host = localReadConfig.get_http("BASEURL")
    port = localReadConfig.get_http("PORT")
    # user_data = json.loads(localReadConfig.get_http("book"))
    user_data = json.loads(localReadConfig.get_http("paper_group"))
    # user_data = json.loads(localReadConfig.get_http("task"))
    # user_data = json.loads(localReadConfig.get_http("book"))

    UA = localReadConfig.get_http("UA")
    data1 = json.dumps(user_data)
    login_url = "http://" + host + ":" + port + "/account/index/login_new"
    header = {"User-Agent": UA}

    luru_session = requests.Session()
    luru_session.post(url=login_url, data=data1, headers=header)

    # response1 = json.loads(response2.text)
    # print(response1)

    # luru_index = luru_session.get('http://10.2.1.170:8080/work/paper/dist/index.html#/?_k=w040dd', headers=header)
    # soup = BeautifulSoup(luru_index.content, "html.parser")
    # if soup.find_all(text="试卷管理"):
    #     print('登录成功')
    # sleep(3)

    logger.debug("Create session:%s" % luru_session)
    return luru_session


# def set_login_session_to_config():
#     """
#     set login session to config
#     :return:
#     """
#     session_login = get_login_session()
#     localReadConfig.set_headers("TOKEN_V", token_v)


def get_value_from_return_json(resultsJson, name1, name2):
    """
    get value by key
    :param json:
    :param name1:
    :param name2:
    :return:
    """
    info = resultsJson
    group = info[name1]
    value = group[name2]
    return value


def show_return_msg(response):
    """
    show msg detail
    :param response:
    :return:
    """
    url = response.url
    msg = response.text
    print("\n请求地址：" + url)
    # 可以显示中文
    print("\n请求返回值：" + '\n' + json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))


# ****************************** read testCase excel ********************************


def get_xls(xls_name, sheet_name):
    """
    get interface data from xls file
    :return:
    """
    cls = []
    # get xls file's path
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)
    # open xls file
    file = open_workbook(xlsPath)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows
    # for i in range(1,nrows):#遍历excel表格
    #     cell_A3 =table.row_values(i)
    #     #获取excel表格中的数据
    #     name    = cell_A3[0]
    #     url    = cell_A3[1]
    #     params=eval(cell_A3[2])
    #     type   = cell_A3[3]
    #     status =cell_A3[4]
    #     Remarks =cell_A3[5]


    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls


'''
###################################################################################################
#处理excel表格
data = xlrd.open_workbook('/Users/gzit000567/PycharmProjects/luru/data/API.xls')#打开excel表格
logging.info("打开%s excel表格成功"%data)
table = data.sheet_by_name(u'sheet2')#打开工作表
logging.info("打开%s表成功"%table)
nrows = table.nrows#统计行数
logging.info("表中有%s行"%nrows)
ncols = table.ncols#统计列数
logging.info("表中有%s列"%ncols)
logging.info("开始进行循环")
name_1=[];url_1=[];params_1=[];type_1=[];Expected_result_1=[];Actual_result_1 =[];test_result_1=[];Remarks_1=[]#定义数组
Success=0;fail=0           #初始化成功失败用例
##################################################################################################################
for i in range(1,nrows):#遍历excel表格
    cell_A3 =table.row_values(i)
#获取excel表格中的数据
    name    = cell_A3[0]
    url    = cell_A3[1]
    params=eval(cell_A3[2])
    type   = cell_A3[3]
    status =cell_A3[4]
    Remarks =cell_A3[5]
    logging.info(url)
'''
# ****************************** read SQL xml ********************************
database = {}


def set_xml():
    """
    set sql xml
    :return:
    """
    if len(database) == 0:
        sql_path = os.path.join(proDir, "testFile", "SQL.xml")
        tree = ElementTree.parse(sql_path)
        for db in tree.findall("database"):
            database_name = db.get("name")
            # print(db_name)
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                # print(table_name)
                sql = {}
                for data in tb.getchildren():
                    sql_id = data.get("id")
                    # print(sql_id)
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[database_name] = table
            # return database


def get_xml_dict(database_name, table_name):
    """
    get db dict by given name
    :param database_name:
    :param table_name:
    :return:
    """
    set_xml()
    first_dict = database.get(database_name)
    database_dict = first_dict.get(table_name)
    return database_dict


def get_sql(database_name, table_name, sql_id):
    """
    get sql by given name and sql_id
    :param database_name:
    :param table_name:
    :param sql_id:
    :return:
    """
    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    return sql


# ****************************** read interfaceURL xml ********************************


def get_url_from_xml(name):
    """
    By name get url from interfaceURL.xml
    :param name: interface's url name
    :return: url
    """
    url_list = []
    url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')
    tree = ElementTree.parse(url_path)
    for u in tree.findall('url'):
        url_name = u.get('name')
        if url_name == name:
            for c in u.getchildren():
                url_list.append(c.text)

    url = '/' + '/'.join(url_list)
    return url

# if __name__ == "__main__":
#     print(get_xls("login"))
#     set_visitor_token_to_config()
