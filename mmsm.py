#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tarfile, zipfile, os, shutil, requests
from BeautifulSoup import *
def url_open(url):
    data = requests.get(url).content
    return data
def file_load(file_link, name):
    print "Start loading " + name
    ifile = url_open(file_link)
    f = open(name, "wb")
    f.write(ifile)
    f.close()
    print name + " downloaded"
def mm_load(os_name):
    page = url_open("http://www.sourcemm.net/snapshots")
    spage = BeautifulSoup(page)
    if os_name == 'lin':
        file_link = spage.table.table.nextSibling.next.next.table.tr.nextSibling.next.td.nextSibling.next.a["href"]
        file_name = "mm_lin_last.tar.gz"
    elif os_name == 'win':
        file_link = spage.table.table.nextSibling.next.next.table.tr.nextSibling.next.td.a["href"]
        file_name = "mm_win_last.zip"
    elif os_name == 'mac':
        file_link = spage.table.table.nextSibling.next.next.table.tr.nextSibling.next.td.nextSibling.next.nextSibling.next.a["href"]
        file_name = "mm_mac_last.zip"
    file_load(file_link, file_name)
    return file_name
def sm_load(os_name):
    page  = url_open("http://www.sourcemod.net/downloads.php?branch=dev")
    spage = BeautifulSoup(page)
    if os_name == 'lin':
        file_link = spage.table.td.nextSibling.next.td.nextSibling.next.nextSibling.next.a["href"]
        file_name = "sm_lin_last.tar.gz"
    elif os_name == 'win':
        file_link = spage.table.td.nextSibling.next.td.nextSibling.next.a["href"]
        file_name = "sm_win_last.zip"
    elif os_name == 'mac':
        file_link = spage.table.td.nextSibling.next.td.nextSibling.next.nextSibling.next.nextSibling.next.a["href"]
        file_name = "sm_mac_last.zip"
    file_load(file_link, file_name)
    return file_name
def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        zf.extractall(dest_dir)
    zf.close()
def untar(source_filename, dest_dir):
    tar = tarfile.open(source_filename, "r")
    tar.extractall(dest_dir)
    tar.close()
def plugins_load(w_dir):
    zip_name = "plugins.zip"
    file_load('https://github.com/LiberBear/recomm_plugins/archive/master.zip', 'plugins.zip')
    print "Unpacking plugins..."
    unzip(zip_name, w_dir)
    move_over(w_dir + "/recomm_plugins-master/", w_dir + "/addons/sourcemod/")
    return zip_name
def move_over(src_dir, dest_dir):
    fileList = os.listdir(src_dir)
    for i in fileList:
        src = os.path.join(src_dir, i)
        dest = os.path.join(dest_dir, i)
        if os.path.exists(dest):
            if os.path.isdir(dest):
                move_over(src, dest)
                continue
            else:
                os.remove(dest)
        shutil.move(src, dest_dir)    
def main():
    print "SourceMod Downloader v0.2"
    print "Created by @LiberBear\nhttps://github.com/LiberBear/SourceMod-Downloader\nvk.com./protector"
    av_os = ('lin', 'mac', 'win')
    os_name = raw_input("Choose one of this ==> mac lin win\n")
    if os_name in av_os:
        w_dir = os.path.join(os.path.basename(os.curdir), "build_" + os_name)
        mm_name = mm_load(os_name)
        sm_name = sm_load(os_name)
        if (os_name == "win" or os_name == "mac"):
            print "Unpacking MM to " + w_dir
            unzip(mm_name, w_dir)
            print "Unpacking SM to " + w_dir
            unzip(sm_name, w_dir)
        else:
            print "Unpacking MM to " + w_dir
            untar(mm_name, w_dir)
            print "Unpacking SM to " + w_dir
            untar(sm_name, w_dir)
        pl_name = plugins_load(w_dir)
        print "Deleting temp files"
        os.remove(mm_name)
        os.remove(sm_name)
        os.remove(pl_name)
        shutil.rmtree(w_dir + "/recomm_plugins-master/", ignore_errors=True)
        print "Done"
        raw_input()
    else:
        print "You failed with choosing OS :D\n"
        raw_input()
if __name__ == "__main__":
    main()
