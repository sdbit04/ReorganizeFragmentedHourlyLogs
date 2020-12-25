import os
import argparse
import shutil
import time


class FileOrganizer(object):

    def __init__(self, daily_directory):
        self.daily_log_dir = daily_directory
        self.hour_v_hour_details = self._get_file_list()
        self.new_dirs = ["9-0", "9-1", "9-2", "9-3"]

    def _get_file_list(self):
        with open("..\\reorganise_file.log", 'a') as log_file:
            # for cur_dir, dirs, files in os.walk(daily_log_dir):
            #     files_count = len(files)
            #     hour_dir = os.path.basename(cur_dir)
            #     print("{} -- > {}".format(hour_dir, files_count), file=files_per_hour)
            hour_v_hour_details = dict()
            try:
                dirs = os.listdir(self.daily_log_dir)
            except Exception as E:
                print("The daily directory {} doesnt exist".format(self.daily_log_dir), file=log_file)
                raise E
            else:
                dirs = set(dirs)
                for dir in dirs:
                    hour_details = dict()
                    dir_path = os.path.join(self.daily_log_dir, dir)
                    files_per_hour = os.listdir(dir_path)
                    files_count_per_hour = len(files_per_hour)
                    hour_details["file_count"] =files_count_per_hour
                    hour_details["files"] = files_per_hour
                    hour_v_hour_details[dir_path]=hour_details
                return hour_v_hour_details

    def _check_existence_of_target_dir(self):
        # print(self.hour_v_hour_details)
        # new_dirs = ["9-0", "9-1", "9-2", "9-3"]
        target_directory = None
        with open("..\\reorganise_file.log", 'a') as log_file:
            for nd in self.new_dirs:
                dir_path = "{}\\{}".format(self.daily_log_dir, nd)
                # TODO test the dir_path
                if dir_path in self.hour_v_hour_details.keys():
                    file_count = self.hour_v_hour_details[dir_path]["file_count"]
                    print("Number of files in new directory are {},".format(file_count), file=log_file, end="\t")
                    if file_count < 100:
                        target_directory = dir_path
                        print("Taking this directory as target dir", file=log_file)
                        break
                    else:
                        continue
                else:
                    try:
                        os.mkdir(os.path.realpath(dir_path))
                    except (PermissionError, NotADirectoryError) as E:
                        print("Unable to create new directory, check permission", file=log_file)
                        raise E
                    except FileExistsError:
                        print("Directory already created, why trying again !!")

                    else:
                        print("New directory {} created ".format(dir_path), file=log_file)
                        self.hour_v_hour_details[dir_path]={"file_count":0, "files":[]}
                        target_directory = dir_path
                        break
        return target_directory

    def reorganize_files(self, min_file_count=30):
        # TODO Please note, the copy(), I have used to travers through a copy of dict, while I am updating original dict.
        # TODO this help me avoid exception RuntimeError : dict size change during loop
        hourly_dir_list = self.hour_v_hour_details.copy().keys()
        for hourly_dir in hourly_dir_list:
            # real_hourly_dir = os.path.realpath(hourly_dir)
            h_dir = os.path.basename(hourly_dir)
            if h_dir not in self.new_dirs:
                files_count = self.hour_v_hour_details[hourly_dir]["file_count"]
                if 0 < files_count < min_file_count:
                    target_dir = self._check_existence_of_target_dir()
                    with open("..\\reorganise_file.log", 'a') as log_file:
                        print("Trying to move files from {} to {}".format(hourly_dir, target_dir), file=log_file)
                        try:
                            for file in self.hour_v_hour_details[hourly_dir]["files"]:
                                file_path = os.path.realpath(os.path.join(hourly_dir, file))
                                print("Moving files {}".format(file_path), file=log_file)
                                shutil.move(file_path, target_dir)
                                # TODO, we will perform action, on the target directory based on the files there, so positively need to update register.
                                self.hour_v_hour_details[target_dir]["file_count"] = self.hour_v_hour_details[target_dir][
                                                                                         "file_count"] + 1
                                self.hour_v_hour_details[target_dir]["files"].append(file)
                        except (FileNotFoundError, TypeError) as E:
                            print("Exception occurred during moving files", file=log_file)
                            raise E
                        else:
                            # TODO in this loop of execution, we will not perform any action on this hourly_dir, no need to update register for it.
                            # self.hour_v_hour_details[hourly_dir]["files"].clear()
                            print("Moved all files from {}".format(hourly_dir), file=log_file)
                            shutil.rmtree(hourly_dir)

    def reorganize_files_1(self, min_file_count=30):
        with open("..\\reorganise_file.log", 'a') as log_file:
            # TODO Please note, the copy(), I have used to travers through a copy of dict, while I am updating original dict.
            # TODO this help me avoid exception RuntimeError : dict size change during loop
            hourly_dir_list = self.hour_v_hour_details.copy().keys()
            for hourly_dir in hourly_dir_list:
                # real_hourly_dir = os.path.realpath(hourly_dir)
                h_dir = os.path.basename(hourly_dir)
                if h_dir not in self.new_dirs:
                    files_count = self.hour_v_hour_details[hourly_dir]["file_count"]
                    if 0 < files_count < min_file_count:

                        target_dir = self._check_existence_of_target_dir()
                        print("Trying to move files from {} to {}".format(hourly_dir, target_dir), file=log_file)
                        try:
                            for file in self.hour_v_hour_details[hourly_dir]["files"]:
                                file_path = os.path.realpath(os.path.join(hourly_dir, file))
                                print("Moving files {}".format(file_path), file=log_file)
                                shutil.move(file_path, target_dir)
                                # TODO, we will perform action, on the target directory based on the files there, so positively need to update register.
                                self.hour_v_hour_details[target_dir]["file_count"] = self.hour_v_hour_details[target_dir]["file_count"] + 1
                                self.hour_v_hour_details[target_dir]["files"].append(file)
                        except (FileNotFoundError, TypeError) as E:
                            print("Exception occurred during moving files", file=log_file)
                            raise E
                        else:
                            # TODO in this loop of execution, we will not perform any action on this hourly_dir, no need to update register for it.
                            # self.hour_v_hour_details[hourly_dir]["files"].clear()

                            print("Moved all files from {}".format(hourly_dir), file=log_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base_path", help="Please provide the path cache\\...\\log under network-element directory")
    parser.add_argument("--datedir", help="Please provide a date (YYYYMMDD) you want to work on, if not provided it will work on sysdate",
                        action="store", default="sysdate")
    args = parser.parse_args()
    with open("..\\reorganise_file.log", 'w') as log_file:
        print("Started processing at {}".format(time.strftime("%Y/%m/%d-%H:%M:%S", time.gmtime())), file=log_file)
    base_dir_path = args.base_path
    dir_to_work = args.datedir
    if dir_to_work == "sysdate":
        dir_to_work = time.strftime("%Y%m%d", time.gmtime())
        daily_log_dir = os.path.join(base_dir_path, dir_to_work)
    else:
        daily_log_dir = os.path.join(base_dir_path, dir_to_work)

    file_organizer = FileOrganizer(daily_log_dir)
    file_organizer.reorganize_files()

