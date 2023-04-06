import sys
sys.path.insert(0, "/libiec61850/pyiec61850")
import iec61850
import time
import signal


def signal_handler(signal, frame):
    global running
    running = 0
    print('bye')


tcpPort = 102

iedModel = iec61850.IedModel_create("testmodel")


ld1 = iec61850.LogicalDevice_create("LD1", iedModel)
ln1 = iec61850.LogicalNode_create("LN1", ld1);
do1 = iec61850.DataObject_create("DO1", iec61850.toModelNode(ln1), 0)
pw = iec61850.DataAttribute_create("power", iec61850.toModelNode(do1), iec61850.IEC61850_FLOAT64, iec61850.IEC61850_FC_MX, 0, 0, 0);

power = 5.0
powerValue = iec61850.MmsValue_newFloat(power);
powerTimestamp = iec61850.MmsValue_newUtcTime(int(time.time()));

iedServer = iec61850.IedServer_create(iedModel)
iec61850.IedServer_start(iedServer, tcpPort)
if not iec61850.IedServer_isRunning(iedServer):
    print("Starting server failed! Exit.")
    iec61850.IedServer_destroy(iedServer)
    sys.exit(-1)

running = 1
signal.signal(signal.SIGINT, signal_handler)


while running:
    #iec61850.MmsValue_setUtcTime(powerTimestamp, int(time.time()));
    iec61850.IedServer_lockDataModel(iedServer);

    iec61850.IedServer_updateFloatAttributeValue(iedServer, pw, power);
    #iec61850.IedServer_updateAttributeValue(iedServer, iec61850.IEDMODEL_Inverter_MMXU1_TotW_t, powerTimestamp);

    iec61850.IedServer_unlockDataModel(iedServer);

    power += 0.1
    iec61850.MmsValue_setFloat(powerValue, power)

    time.sleep(1)

iec61850.IedServer_stop(iedServer)
iec61850.IedServer_destroy(iedServer)
