"""
批量移除图片中的Alpha通道.
--input_dir 输入路径
--output_dir 输出路径
"""
import os
import argparse
import cv2

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", default="input",type=str, help="输入根路径.")
parser.add_argument("--output_dir", type=str,default="output", help="输出根路径.")
arg = parser.parse_args()

def main():
    cnt = 0
    default_img_format = [".png"]#文件拓展名,可添加其他拓展名以支持其他格式
    src_dir = arg.input_dir
    dst_dir = arg.output_dir
    for root, dirs, files in os.walk(src_dir, topdown=False):
        for file_name in files:
            for extend in default_img_format:
                if not file_name.endswith(extend):
                    continue
                print("Processing {}...".format(file_name))
                img = cv2.imread(os.path.join(src_dir,file_name), flags=cv2.IMREAD_COLOR)
                cv2.waitKey(0)
                cv2.imwrite(os.path.join(dst_dir,file_name),img)
                cnt+=1
    print("Removed {} alpha channels of images successfully.".format(str(cnt)))

if __name__ == "__main__":
	main()
