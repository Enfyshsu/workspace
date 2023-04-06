import iec61850
import time
interface = 'eth0'

dataSetValues = iec61850.LinkedList_create()
iec61850.LinkedList_add(dataSetValues, iec61850.MmsValue_newIntegerFromInt32(1234))
iec61850.LinkedList_add(dataSetValues, iec61850.MmsValue_newBinaryTime(False))
iec61850.LinkedList_add(dataSetValues, iec61850.MmsValue_newIntegerFromInt32(5678))

gooseCommParameters = iec61850.CommParameters()
gooseCommParameters.appId = 1000
iec61850.CommParameters_setDstAddress(gooseCommParameters, 0x01, 0x0c, 0xcd, 0x01, 0x00, 0x01)
gooseCommParameters.vlanId = 0
gooseCommParameters.vlanPriority = 4

publisher = iec61850.GoosePublisher_create(gooseCommParameters, interface)
if publisher:
    iec61850.GoosePublisher_setGoCbRef(publisher, "simpleIOGenericIO/LLN0$GO$gcbAnalogValues")
    iec61850.GoosePublisher_setConfRev(publisher, 1)
    iec61850.GoosePublisher_setDataSetRef(publisher, "simpleIOGenericIO/LLN0$AnalogValues")
    iec61850.GoosePublisher_setTimeAllowedToLive(publisher, 500)
    
    for i in range(4):
        time.sleep(1)
        if i == 3:
            iec61850.LinkedList_add(dataSetValues, iec61850.
                    MmsValue_newBoolean(True))
            iec61850.GoosePublisher_publish(publisher, dataSetValues)
        else:
            if iec61850.GoosePublisher_publish(publisher, dataSetValues) == -1:
                print("Error sending message")
    iec61850.GoosePublisher_destroy(publisher)
else:
    print("Failed to create GOOSE publisher.")
    iec61850.LinkedList_destroyDeep(dataSetValues, iec61850.MmsValue_delete)
    



