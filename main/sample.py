
import logging
import random
import os
import shutil
import sys
logger = logging.getLogger("sample")
# 总的图片目录txt文件位置
txt_all = 'train.txt'
# 分出图片的路径
person_path = "data/everybody/"
# 源文件路径
src_path = '/src'
# 正确文件路径
good_path = '/good'
# 错误文件路径
bad_path = '/bad'

def init_logger():
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s',
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()])

# 用户拿原图片
def get_img_by_person(person_img_num,user_name):
    for i in range(person_img_num):
        img_txt = open(txt_all, 'r')
        lines = img_txt.readlines()  # 读取所有行
        first_line = lines[0].split( )  # 取第一行
        img_path = first_line[0]
        img_name = img_path.split("/")[2]
        label = first_line[1]
        # 将该图片和label写入该用户的文件夹
        write_img_label_to_newfile(img_path,label,user_name,img_name)
        # 修改txt文件
        with open(img_txt.name, "w", encoding="utf-8") as f_w:
            for line in lines:
                if lines[0] in line:
                    continue
                f_w.write(line)



# 将该图片和label写入该用户的文件夹
def write_img_label_to_newfile(img_path,label,user_name,img_name):
    img_path = os.path.join('%s%s' % ("", img_path))
    new_path = os.path.join('%s%s' % (person_path, user_name))
    logger.info("邮箱前缀为" + user_name + "的用户的文件路径为" + new_path)
    if not os.path.isdir(new_path):
        os.mkdir(new_path)
    # 源文件路径
    img_src = os.path.join('%s%s' % (new_path, src_path))
    if not os.path.isdir(img_src):
        os.mkdir(img_src)
    logger.info("将图片%r移动到%r",img_path,img_src)
    moveFileto(img_path,img_src)
    # 用户对应的txt
    user_txt_name = os.path.join('%s%s' % (user_name,".txt"))
    user_txt = os.path.join('%s%s%s%s' % (new_path, src_path ,"/",user_txt_name))
    fopen = open(user_txt, 'a+')
    write_txt = img_name + " " + label
    fopen.write('%s%s' % (write_txt, os.linesep))
    fopen.close()

def moveFileto(sourceDir,  targetDir):
    shutil.move(sourceDir,  targetDir)


#
if __name__ == '__main__':

    import argparse

    init_logger()

    parser = argparse.ArgumentParser()
    parser.add_argument("--dir")
    parser.add_argument("--person_img_num")
    parser.add_argument("--user_name")

    args = parser.parse_args()
    # 数据位置
    DATA_DIR = args.dir
    # 每个人一次拿的图片数
    person_img_num = int(args.person_img_num)
    # 邮箱前缀
    user_name = args.user_name
    get_img_by_person(person_img_num,user_name)

