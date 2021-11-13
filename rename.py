"""
数据集批量重命名.
--root_dir 输入根路径
--save_path 输出根路径
--start_num 起始计数.
--
"""
import os
import argparse
from shutil import copyfile

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser()
parser.add_argument("--root_dir", default="label",type=str, help="输入根路径.")
parser.add_argument("--save_path", type=str,default="output", help="输出根路径.")
parser.add_argument("--start_num", type=str,default='0', help="起始计数.")
arg = parser.parse_args()

def GenerateFileName(index):
    	# if index >= 1000
	if index >= 1000 :
		file_name = str(index)
	# if index >= 1000
	elif index >= 100:
		file_name = "0" + str(index)
	elif index >= 10:
		file_name = "00" + str(index)
	else:
		file_name = "000" + str(index)
	file_name_img = file_name + ".png"
	file_name_lab = file_name + ".txt"
	return file_name_img, file_name_lab

def main():
	src_dir = arg.root_dir
	out_dir = arg.save_path
	cnt = int(arg.start_num)
	for root, dirs, files in os.walk(src_dir, topdown=False):
		for file_name in files:
			file_name_img = file_name.replace(".txt",".png")
			if not file_name.endswith(".txt"):
				continue

			if not os.path.exists(os.path.join(src_dir, file_name_img)):
    				continue
			dst_file_img, dst_file_lab =  GenerateFileName(cnt)
			copyfile(os.path.join(src_dir, file_name), os.path.join(out_dir, dst_file_lab))
			copyfile(os.path.join(src_dir, file_name_img), os.path.join(out_dir, dst_file_img))
			cnt+=1

if __name__ == "__main__":
	main()
