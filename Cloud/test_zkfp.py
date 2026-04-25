from pyzkfp import ZKFP2

def test():
    zkfp = ZKFP2()
    try:
        res = zkfp.Init()
        print("Init res:", res)
        try:
            zkfp.OpenDevice(0)
            print("Opened!")
            # test DBIdentify with None
            try:
                zkfp.DBIdentify(b"abc")
            except Exception as e:
                print("Identify error:", str(e))
                
            # test DBMerge with None
            try:
                zkfp.DBMerge(b"1", b"2", b"3")
            except Exception as e:
                print("Merge error:", str(e))
                
        finally:
            zkfp.CloseDevice()
            zkfp.Terminate()
    except Exception as e:
        print("Error:", str(e))

test()
