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

def GenerateFileName(index,extend_name):
	file_name = str(index).zfill(4)

	file_name_img = file_name + extend_name
	file_name_lab = file_name + ".txt"
	return file_name_img, file_name_lab

def main():
	default_img_format = [".jpg",".png",".jpeg"]
	src_dir = arg.root_dir
	out_dir = arg.save_path
	cnt = int(arg.start_num)
	for root, dirs, files in os.walk(src_dir, topdown=False):
		for file_name in files:
			# Continue while theres is no label.
			if not file_name.endswith(".txt"):
				continue

			file_name_label = file_name
			file_name = file_name.replace(".txt","")
			file_name_img = ""
			extend_name_img = ""
			
			for extend in default_img_format:
				if not os.path.exists(os.path.join(src_dir, file_name + extend)):
					continue
				file_name_img = file_name + extend
				extend_name_img = extend
				break
			if extend_name_img == "":
				print("A Problem occured while copying {} , Please check its image and label.".format(file_name))
				continue

			dst_file_img, dst_file_label = GenerateFileName(cnt,extend_name_img)
			# print(file_name_label)
			copyfile(os.path.join(src_dir, file_name_label), os.path.join(out_dir, dst_file_label))
			copyfile(os.path.join(src_dir, file_name_img), os.path.join(out_dir, dst_file_img))
			cnt+=1
	print("Renamed {} images and labels successfully.".format(str(cnt - int(arg.start_num))))

if __name__ == "__main__":
	main()
