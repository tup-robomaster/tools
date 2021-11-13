"""
将四点标注格式转化为YOLO矩形标注.
--root_dir 输入根路径
--save_path 输出根路径
--w_ratio 矩形标注框宽度扩大倍数
--h_ratio 矩形标注框高度扩大倍数
"""
import os
import argparse
import cv2
import numpy as np

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser()
parser.add_argument("--root_dir", default="label",type=str, help="输入根路径.")
parser.add_argument("--save_path", type=str,default="output", help="输出根路径.")
parser.add_argument("--w_ratio", type=str,default='1.2', help="矩形标注框宽度扩大倍数.")
parser.add_argument("--h_ratio", type=str,default='2.0', help="矩形标注框高度扩大倍数.")
arg = parser.parse_args()


def min_rect(points):
	x_min = np.min(points[::2])
	x_max = np.max(points[::2])
	y_min = np.min(points[1::2])
	y_max = np.max(points[1::2])
	w = x_max - x_min
	h = y_max - y_min

	return [x_min + w / 2.0,
			y_min + h / 2.0,
			w,
			h,
	]



def main():
	src_dir = arg.root_dir
	out_dir = arg.save_path
	cnt = 0
	
	for root, dirs, files in os.walk(src_dir, topdown=False):
		for file_name in files:
			if not file_name.endswith(".txt"):
				continue

			#遍历所有TXT文本
			with open(os.path.join(out_dir,file_name),"w") as dst:
				with open(os.path.join(root,file_name),'r+') as src:
					lines = src.readlines()
					for line in lines:
						text = line.strip().split()
						
						object_index = text[0]
						
						#计算最小外接矩形
						[x, y, w, h] = min_rect(np.asarray(text[1:9],dtype=np.float32))
						#Adjust
						[x, y, w, h] = [x, y, float(arg.w_ratio) * w, float(arg.h_ratio) * h]

						dst.write(str(object_index) + " " + str(x) + " " + str(y) + " " + " " + str(w) + " " + str(h) +"\n")
					cnt+=1
	print("Successfully transformed", cnt, "txts from",arg.root_dir, "and saved to",arg.save_path, ".")

if __name__ == "__main__":
	main()
