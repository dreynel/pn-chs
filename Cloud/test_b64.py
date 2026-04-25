import base64
import clr
clr.AddReference("System")
from System import Array, Byte

arr = Array[Byte]([1, 2, 3, 4, 5])
try:
    s = base64.b64encode(arr)
    print("Success:", s)
except Exception as e:
    print("Error:", type(e).__name__, str(e))
