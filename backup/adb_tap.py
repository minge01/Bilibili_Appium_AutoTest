import subprocess
import time

DEVICE = "127.0.0.1:7555"
# ========= 修改成你模拟器上跳过按钮的屏幕坐标 =========
SKIP_X = 930
SKIP_Y = 85

def adb_tap(x:int,y:int):
    cmd = [
        "adb","-s",DEVICE,"shell","input","tap",str(x),str(y)
    ]
    subprocess.run(cmd,timeout=5)

def try_tap_age_popup(max_wait_sec=8,interval=1.5):
    """轮询等待弹窗出现，到点没出现就放弃，不会卡死
    return True点击成功 / False弹窗未出现
    """
    start = time.time()
    print(f"开始轮询等待年龄性别弹窗，最长等待{max_wait_sec}秒")
    while time.time() - start < max_wait_sec:
        # 点击跳过坐标
        adb_tap(SKIP_X,SKIP_Y)
        time.sleep(interval)
    print("轮询超时，判定弹窗未弹出，继续首页业务")
    return False
