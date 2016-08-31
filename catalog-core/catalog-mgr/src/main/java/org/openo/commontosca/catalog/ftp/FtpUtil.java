/**
 * Copyright 2016 [ZTE] and others.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.openo.commontosca.catalog.ftp;

import org.apache.commons.net.ftp.FTPClient;
import org.apache.commons.net.ftp.FTPFile;
import org.apache.commons.net.ftp.FTPReply;
import org.apache.log4j.Logger;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;

public class FtpUtil {

  private static Logger logger = Logger.getLogger(FtpUtil.class);

  private static FTPClient ftp;

  /**
   * get ftp connection.
   * 
   * @param conftp Ftp
   * @return boolean
   * @throws Exception e
   */
  public static boolean connectFtp(Ftp conftp) throws Exception {
    ftp = new FTPClient();
    boolean flag = false;
    if (conftp.getPort() == null) {
      ftp.connect(conftp.getIpAddr(), 21);
    } else {
      ftp.connect(conftp.getIpAddr(), conftp.getPort());
    }
    ftp.login(conftp.getUserName(), conftp.getPwd());
    ftp.setFileType(FTPClient.BINARY_FILE_TYPE);
    int reply = ftp.getReplyCode();
    if (!FTPReply.isPositiveCompletion(reply)) {
      ftp.disconnect();
      return flag;
    }
    ftp.changeWorkingDirectory(conftp.getPath());
    flag = true;
    return flag;
  }

  /**
   * close ftp connection.
   */
  public static void closeFtp() {
    if (ftp != null && ftp.isConnected()) {
      try {
        ftp.logout();
        ftp.disconnect();
      } catch (IOException e1) {
        e1.printStackTrace();
      }
    }
  }

  /**
   * upload file by ftp.
   * 
   * @param file file to upload
   * @throws Exception e
   */
  public static void upload(File file) throws Exception {
    if (file.isDirectory()) {
      ftp.makeDirectory(file.getName());
      ftp.changeWorkingDirectory(file.getName());
      String[] files = file.list();
      for (String fstr : files) {
        File file1 = new File(file.getPath() + "/" + fstr);
        if (file1.isDirectory()) {
          upload(file1);
          ftp.changeToParentDirectory();
        } else {
          File file2 = new File(file.getPath() + "/" + fstr);
          FileInputStream input = new FileInputStream(file2);
          ftp.storeFile(file2.getName(), input);
          input.close();
        }
      }
    } else {
      File file2 = new File(file.getPath());
      FileInputStream input = new FileInputStream(file2);
      ftp.storeFile(file2.getName(), input);
      input.close();
    }
  }

  /**
   * download inline config.
   * 
   * @param downftp ftp to download
   * @param localBaseDir local directory
   * @param remoteBaseDir remote directory
   * @throws Exception e
   */
  public static void startDown(Ftp downftp, String localBaseDir, String remoteBaseDir)
      throws Exception {
    if (FtpUtil.connectFtp(downftp)) {

      try {
        FTPFile[] files = null;
        boolean changedir = ftp.changeWorkingDirectory(remoteBaseDir);
        if (changedir) {
          ftp.setControlEncoding("GBK");
          files = ftp.listFiles();
          for (int i = 0; i < files.length; i++) {
            try {
              downloadFile(files[i], localBaseDir, remoteBaseDir);
            } catch (Exception e1) {
              logger.error(e1);
              logger.error("<" + files[i].getName() + ">download failed");
            }
          }
        }
      } catch (Exception e1) {
        logger.error(e1);
        logger.error("error occoured while download");
      }
    } else {
      logger.error("Connect failed !");
    }

  }


  /**
   * download ftp file.
   * 
   * @param ftpFile ftp file to download
   * @param relativeLocalPath relative local path
   * @param relativeRemotePath relative remote path
   */
  private static void downloadFile(FTPFile ftpFile, String relativeLocalPath,
      String relativeRemotePath) {
    if (ftpFile.isFile()) {
      if (ftpFile.getName().indexOf("?") == -1) {
        OutputStream outputStream = null;
        try {
          File locaFile = new File(relativeLocalPath + ftpFile.getName());
          // 判断文件是否存在，存在则返回
          if (locaFile.exists()) {
            return;
          } else {
            outputStream = new FileOutputStream(relativeLocalPath + ftpFile.getName());
            ftp.retrieveFile(ftpFile.getName(), outputStream);
            outputStream.flush();
            outputStream.close();
          }
        } catch (Exception e1) {
          logger.error(e1);
        } finally {
          try {
            if (outputStream != null) {
              outputStream.close();
            }
          } catch (IOException e1) {
            logger.error("输出文件流异常");
          }
        }
      }
    } else {
      String newlocalRelatePath = relativeLocalPath + ftpFile.getName();
      String newRemote = new String(relativeRemotePath + ftpFile.getName().toString());
      File fl = new File(newlocalRelatePath);
      if (!fl.exists()) {
        fl.mkdirs();
      }
      try {
        newlocalRelatePath = newlocalRelatePath + '/';
        newRemote = newRemote + "/";
        String currentWorkDir = ftpFile.getName().toString();
        boolean changedir = ftp.changeWorkingDirectory(currentWorkDir);
        if (changedir) {
          FTPFile[] files = null;
          files = ftp.listFiles();
          for (int i = 0; i < files.length; i++) {
            downloadFile(files[i], newlocalRelatePath, newRemote);
          }
        }
        if (changedir) {
          ftp.changeToParentDirectory();
        }
      } catch (Exception e1) {
        logger.error(e1);
      }
    }
  }
}
