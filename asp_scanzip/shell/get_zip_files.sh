#!/user/bin/env python
# -*- coding:utf-8 -*-

import zipfile, os

# 解压后文件放置位置
# unzip_folders_path = "/test/20201103/unzip_pkg"
# 需解压地址
# zip_folders_path = "/vulnerability_test/zip_app_script/zip_pkg"


unzip_folders_path = "/data/ftproot/scan_project/pool_scan_tasks/lvmeng"
zip_folders_path = "/home/zabbix/security_report/app_monthly_report"


def unzip_folder():
    zip_folder_list = os.listdir(zip_folders_path)
    if not zip_folder_list:
        print("ZipTypeERROR:%s未存在压缩文件" % zip_folders_path)
    for folder_zip in zip_folder_list:
        zip_files_path = "%s/%s" % (zip_folders_path, folder_zip)
        if os.path.splitext(folder_zip)[1] == '.zip':
            file_zip = zipfile.ZipFile(zip_files_path, 'r')
            for file in file_zip.namelist():
                file_zip.extract(file, unzip_folders_path)
            file_zip.close()
            os.remove(zip_files_path)


# 创建业务下的文件夹
def mkdir(mkpath, path):
    path = "%s/%s" % (mkpath, path)
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # print(path + ' 创建成功')
        os.makedirs(path)
    else:
        print(path + ' 目录已存在')
    return path


def get_resources():
    # unzip_folder_list：['xxg', 'hachi', 'huchi']
    unzip_folder_list = os.listdir(unzip_folders_path)
    if not unzip_folder_list:
        print("UnZipTypeERROR:%s未存在解压文件" % unzip_folders_path)
    for unzip_folder_name in unzip_folder_list:
        # tmp_file : /test/20201103/unzip_pkg/xxg
        unzip_folder_path = "%s/%s" % (unzip_folders_path, unzip_folder_name)
        if not unzip_folder_path:
            print("NotFindUnzipFile:%s目录为空" % unzip_folder_path)
        for unzip_file in os.listdir(unzip_folder_path):
            if os.path.splitext(unzip_file)[1] == '.zip':
                file_path = unzip_file.rsplit('.', 1)[0].strip()
                path = mkdir(unzip_folder_path, file_path)
                if path:
                    if path.rsplit('/', 1)[1].strip() == file_path:
                        unzip_files_path = "%s/%s" % (unzip_folder_path, unzip_file)
                        print(">>>", unzip_files_path)
                        file_zip = zipfile.ZipFile(unzip_files_path, 'r')
                        for file in file_zip.namelist():
                            file_zip.extract(file, path)
                        file_zip.close()
                        os.remove(unzip_files_path)

    print("解压完成！！")


if __name__ == "__main__":
    unzip_folder()
    get_resources()
