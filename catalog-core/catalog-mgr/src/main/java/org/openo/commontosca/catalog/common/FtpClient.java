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
package org.openo.commontosca.catalog.common;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import org.apache.commons.net.ftp.FTP;
import org.apache.commons.net.ftp.FTPClient;
import org.apache.commons.net.ftp.FTPFile;
import org.apache.commons.net.ftp.FTPReply;

/**
 * FTP client user for upload or delete files in ftp client
 */
public class FtpClient {
    private FTPClient ftpClient;

    public static final String ZIP = ".zip";

    public FtpClient(String host, String username, String password, int port) throws Exception {
        ftpClient = new FTPClient();
        connect(host, username, password, port);
    }

    private void connect(String host, String user, String pwd, int port) throws Exception {
        ftpClient.connect(host, port);
        if (!FTPReply.isPositiveCompletion(ftpClient.getReplyCode())) {
            ftpClient.disconnect();
            throw new Exception("Exception in connecting to FTP Server");
        }
        ftpClient.login(user, pwd);
        ftpClient.setFileType(FTP.BINARY_FILE_TYPE);
        ftpClient.enterLocalPassiveMode();
    }

    public void disconnect() throws Exception {
        if (this.ftpClient.isConnected()) {
            this.ftpClient.logout();
            this.ftpClient.disconnect();
        }
    }

    public void get(String remoteFilePath, String localFilePath) throws IOException {
        FileOutputStream fos = new FileOutputStream(localFilePath);
        this.ftpClient.retrieveFile(remoteFilePath, fos);
        fos.close();
    }

    public void delete(String filePath) throws IOException {
        ftpClient.dele(filePath);
    }

    /**
     * upload a file to FTP client. support resuming
     * 
     * @param local
     * @param remote
     * @return
     * @throws IOException
     */
    public EnumUploadStatus upload(int startPosition, int endPosition, InputStream inputstream,
            String remote) throws IOException {
        // set transfer mode: PassiveMode
        ftpClient.enterLocalPassiveMode();
        // set transfer file type: binary
        ftpClient.setFileType(FTP.BINARY_FILE_TYPE);
        ftpClient.setControlEncoding("GBK");
        String remoteFileName = remote;
        if (remote.contains("/")) {
            remoteFileName = remote.substring(remote.lastIndexOf("/") + 1);
            if (CreateDirecroty(remote, ftpClient) == EnumUploadStatus.Create_Directory_Fail) {
                return EnumUploadStatus.Create_Directory_Fail;
            }
        }

        long lStartPos = 0;
        FTPFile[] files =
                ftpClient.listFiles(new String(remoteFileName.getBytes("GBK"), "iso-8859-1"));
        if (files.length == 1) {
            lStartPos = files[0].getSize();
        }
        if (lStartPos > endPosition) {
            return EnumUploadStatus.File_Exist;
        }
        if (lStartPos < startPosition) {
            lStartPos = startPosition;
        } else if (lStartPos > startPosition && lStartPos < endPosition) {
            lStartPos = startPosition;
        }

        return uploadFile(remoteFileName, inputstream, ftpClient, lStartPos);
    }

    /**
     * Create a remote server directory recursively
     * 
     * @param remote
     * @param ftpClient
     * @return
     * @throws IOException
     */
    public EnumUploadStatus CreateDirecroty(String remote, FTPClient ftpClient) throws IOException {
        String directory = remote.substring(0, remote.lastIndexOf("/") + 1);
        if (!directory.equalsIgnoreCase("/")
                && !ftpClient.changeWorkingDirectory(new String(directory.getBytes("GBK"),
                        "iso-8859-1"))) {
            int start = 0;
            int end = 0;
            if (directory.startsWith("/")) {
                start = 1;
            } else {
                start = 0;
            }
            end = directory.indexOf("/", start);
            while (true) {
                String subDirectory =
                        new String(remote.substring(start, end).getBytes("GBK"), "iso-8859-1");
                if (!ftpClient.changeWorkingDirectory(subDirectory)) {
                    if (ftpClient.makeDirectory(subDirectory)) {
                        ftpClient.changeWorkingDirectory(subDirectory);
                    } else {
                        return EnumUploadStatus.Create_Directory_Fail;
                    }
                }

                start = end + 1;
                end = directory.indexOf("/", start);

                // check whether all directories are created or not
                if (end <= start) {
                    break;
                }
            }
        }
        return EnumUploadStatus.Create_Directory_Success;
    }

    /**
     * upload file to client
     * 
     * @param remoteFile remote file name
     * @param localFile local file name, including absolute path
     * @param ftpClient FTPClient class
     * @param lStartPos starting position
     * @return
     * @throws IOException
     */
    public EnumUploadStatus uploadFile(String remoteFile, InputStream inputstream,
            FTPClient ftpClient, long lStartPos) throws IOException {
        OutputStream out =
                ftpClient.appendFileStream(new String(remoteFile.getBytes("GBK"), "iso-8859-1"));
        if (out == null) {
            out = ftpClient.storeFileStream(new String(remoteFile.getBytes("GBK"), "iso-8859-1"));
        }
        if (lStartPos > 0) {
            ftpClient.setRestartOffset(lStartPos);
        }
        byte[] bytes = new byte[512];
        int c;
        while ((c = inputstream.read(bytes, 0, 512)) > 0) {
            out.write(bytes, 0, c);
        }
        out.flush();
        out.close();
        boolean result = ftpClient.completePendingCommand();
        if (lStartPos > 0) {
            return result ? EnumUploadStatus.Upload_From_Break_Success
                    : EnumUploadStatus.Upload_From_Break_Failed;
        } else {
            return result ? EnumUploadStatus.Upload_New_File_Success
                    : EnumUploadStatus.Upload_New_File_Failed;
        }
    }
}
