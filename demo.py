import PySmart
import logging

def dotest():    
    logging.basicConfig(level=logging.INFO)
    PySmart.Initial('D:')
    
    logging.info('SMART initialized')
    logging.info('Read SMART')

    ret = PySmart.Read()        
    logging.info('result: {}'.format(ret))

    if (ret != 0):
        print('got error:', PySmart.GetErrorMessage())

    info = PySmart.GetBasicSmartInfo()   

    print(info)
    

if __name__ == '__main__':
    	dotest()
else:
	pass