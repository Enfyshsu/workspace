import lib61850
import time

interface = 'eth0'


svPublisher = lib61850.SVPublisher_create(None, interface)
if svPublisher:
    asdu1 = lib61850.SVPublisher_addASDU(svPublisher, "svpub1", None, 1)
    float1 = lib61850.SVPublisher_ASDU_addFLOAT(asdu1)
    float2 = lib61850.SVPublisher_ASDU_addFLOAT(asdu1)
    ts1 = lib61850.SVPublisher_ASDU_addTimestamp(asdu1)

    lib61850.SVPublisher_setupComplete(svPublisher)
    fVal1 = 1234.5678
    fVal2 = 0.12345
    for i in range(100):
        ts = lib61850.Timestamp()
        lib61850.Timestamp_clearFlags(ts)
        lib61850.Timestamp_setTimeInMilliseconds(ts, int(time.time()))
        
        lib61850.SVPublisher_ASDU_setFLOAT(asdu1, float1, fVal1)
        lib61850.SVPublisher_ASDU_setFLOAT(asdu1, float2, fVal2)
        lib61850.SVPublisher_ASDU_setTimestamp(asdu1, ts1, ts)

        lib61850.SVPublisher_ASDU_increaseSmpCnt(asdu1);
        fVal1 += 1.1
        fVal2 += 0.1

        lib61850.SVPublisher_publish(svPublisher)
        time.sleep(0.5)

    lib61850.SVPublisher_destroy(svPublisher)


