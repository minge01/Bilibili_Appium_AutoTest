import os
os.environ["PYTHONIOENCODING"] = "utf-8"
import sys
import time
import argparse
from airtest.core.api import auto_setup, touch, exists, device
from airtest.core.settings import Settings as ST

parser = argparse.ArgumentParser()
parser.add_argument("--device", required=True)
parser.add_argument("--tpl", required=True)
parser.add_argument("--threshold", type=float, default=0.72)
args = parser.parse_args()

try:
    dev_uri = f"Android://127.0.0.1:5037/{args.device}"
    auto_setup(__file__, devices=[dev_uri])

    # ========= MSTPL核心配置 =========
    ST.CVSTRATEGY = ["mstpl"]
    ST.MS_SCALE_RANGE = (0.7, 1.3)
    ST.MS_SCALE_STEP = 4
    # =================================

    print(f"Airtest MSTPL多尺度匹配开始轮询弹窗,阈值:{args.threshold}")
    pop_ele = exists(args.tpl, threshold=args.threshold, timeout=2)
    if pop_ele:
        touch(pop_ele)
        print("✅ MSTPL多尺度模板匹配成功，已点击关闭弹窗")
        time.sleep(0.8)
        sys.exit(0)
    else:
        print("❌ MSTPL多尺度匹配失败，弹窗画面未找到")
        sys.exit(1)

except Exception as e:
    print(f"Airtest脚本异常 {e}")
    sys.exit(1)
finally:
    # 安全断开，先判断设备是否成功连接
    try:
        if device():
            device().disconnect()
    except Exception:
        pass
