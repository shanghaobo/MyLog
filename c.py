from MyLog import getLogger
import a
import b

a.aa()
b.bb()

log=getLogger(__name__)

log.info('c')