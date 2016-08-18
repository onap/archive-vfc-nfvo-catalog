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

import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public final class FileUtil {

    public static final Logger LOG = LoggerFactory.getLogger(FileUtil.class);

    private static final int BUFFER_SIZE = 2 * 1024 * 1024;

    private static final int TRY_COUNT = 3;

    private FileUtil() {

    }

    /**
     * create dir
     * 
     * @param dir
     */
    public static boolean createDirectory(String dir) {
        File folder = new File(dir);
        int tryCount = 0;
        while (tryCount < TRY_COUNT) {
            tryCount++;
            if (!folder.exists() && !folder.mkdirs()) {
                continue;
            } else {
                return true;
            }
        }

        return folder.exists();
    }

    public static boolean deleteFile(File file) {
        String hintInfo = file.isDirectory() ? "dir " : "file ";
        boolean isFileDeleted = file.delete();
        boolean isFileExist = file.exists();
        if (!isFileExist) {
            if (isFileDeleted) {
                LOG.info("delete " + hintInfo + file.getAbsolutePath());
            } else {
                isFileDeleted = true;
                LOG.info("file not exist. no need delete " + hintInfo + file.getAbsolutePath());
            }
        } else {
            LOG.info("fail to delete " + hintInfo + file.getAbsolutePath());
        }
        return isFileDeleted;
    }

    /**
     * unzip zip file
     * 
     * @param zipFileName
     * @param unzip dir
     * @throws IOException
     */
    public static ArrayList<String> unzip(String zipFileName, String extPlace) throws IOException {
        ZipFile zipFile = null;
        ArrayList<String> unzipFileNams = new ArrayList<String>();

        try {
            zipFile = new ZipFile(zipFileName);
            Enumeration<?> fileEn = zipFile.entries();
            byte[] buffer = new byte[BUFFER_SIZE];

            while (fileEn.hasMoreElements()) {
                InputStream input = null;
                BufferedOutputStream bos = null;
                try {
                    ZipEntry entry = (ZipEntry) fileEn.nextElement();
                    if (entry.isDirectory()) {
                        continue;
                    }

                    input = zipFile.getInputStream(entry);
                    File file = new File(extPlace, entry.getName());
                    if (!file.getParentFile().exists()) {
                        createDirectory(file.getParentFile().getAbsolutePath());
                    }

                    bos = new BufferedOutputStream(new FileOutputStream(file));
                    while (true) {
                        int length = input.read(buffer);
                        if (length == -1) {
                            break;
                        }
                        bos.write(buffer, 0, length);
                    }
                    unzipFileNams.add(file.getAbsolutePath());
                } finally {
                    closeOutputStream(bos);
                    closeInputStream(input);
                }
            }
        } finally {
            closeZipFile(zipFile);
        }
        return unzipFileNams;
    }

    /**
     * close InputStream
     * 
     * @param inputStream
     */
    private static void closeInputStream(InputStream inputStream) {
        try {
            if (inputStream != null) {
                inputStream.close();
            }
        } catch (Exception e) {
            LOG.info("close InputStream error!");
        }
    }

    /**
     * close OutputStream
     * 
     * @param outputStream
     */
    private static void closeOutputStream(OutputStream outputStream) {
        try {
            if (outputStream != null) {
                outputStream.close();
            }
        } catch (Exception e) {
            LOG.info("close OutputStream error!");
        }
    }

    /**
     * close zipFile
     * 
     * @param zipFile
     */
    private static void closeZipFile(ZipFile zipFile) {
        try {
            if (zipFile != null) {
                zipFile.close();
                zipFile = null;
            }
        } catch (IOException e) {
            LOG.info("close ZipFile error!");
        }
    }
}
