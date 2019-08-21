from MyLog import MyLog

def aa():
    mylog = MyLog(__name__)

    log = mylog.getLogger()

    log.info('a')