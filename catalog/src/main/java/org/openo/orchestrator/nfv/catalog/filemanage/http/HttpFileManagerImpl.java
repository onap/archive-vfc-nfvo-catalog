/**
 *     Copyright (C) 2016 ZTE, Inc. and others. All rights reserved. (ZTE)
 *
 *     Licensed under the Apache License, Version 2.0 (the "License");
 *     you may not use this file except in compliance with the License.
 *     You may obtain a copy of the License at
 *
 *             http://www.apache.org/licenses/LICENSE-2.0
 *
 *     Unless required by applicable law or agreed to in writing, software
 *     distributed under the License is distributed on an "AS IS" BASIS,
 *     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *     See the License for the specific language governing permissions and
 *     limitations under the License.
 */
package org.openo.orchestrator.nfv.catalog.filemanage.http;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

import org.openo.orchestrator.nfv.catalog.filemanage.FileManager;
import org.openo.orchestrator.nfv.catalog.filemanage.entity.FileLink;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class HttpFileManagerImpl implements FileManager {
    private static final Logger LOGGER = LoggerFactory.getLogger(HttpFileManagerImpl.class);

    @Override
    public boolean upload(String srcPath, String dstPath) {
        boolean flag = true;
        LOGGER.info("start upload file.srcPath:" + srcPath + " dstPath" + dstPath);
        File srcFile = new File(srcPath);
        if (!srcFile.exists()) {
            LOGGER.error("src file not exist!");
            return false;
        }
        // File dstFile = new File(ToolUtil.getHttpServerPath() + dstPath);
        // LOGGER.info("dstFile AbsolutePath:" + dstFile.getAbsolutePath());
        try {
            ToolUtil.copyDirectory(srcPath, ToolUtil.getHttpServerPath() + dstPath, true);
        } catch (IOException e) {
            flag = false;
            LOGGER.error("copy file failed.errorMsg:" + e.getMessage());
        }
        LOGGER.info("upload file success!");
        return flag;
    }

    @Override
    public boolean download(String srcPath, String dstPath) {
        // TODO Auto-generated method stub
        return false;
    }

    @Override
    public boolean delete(String srcPath) {
        boolean flag = true;
        LOGGER.info("start delete file from http server.srcPath:" + srcPath);
        flag = ToolUtil.deleteDir(new File(ToolUtil.getHttpServerPath() + srcPath));
        LOGGER.info("delete file from http server end.flag:" + flag);
        return flag;
    }

    @Override
    public ArrayList<FileLink> queryWorkFlow(String path) {
        LOGGER.info("start query workFlow from http server.path:" + path);
        File workFlowRoot = new File(ToolUtil.getHttpServerPath() + path);
        ArrayList<FileLink> fileLinks = new ArrayList<FileLink>();
        File[] files = workFlowRoot.listFiles();
        if (files != null && files.length != 0) {
            for (File file : files) {
                if (file.isFile() && file.getName().endsWith(".zip")) {
                    FileLink fileLink = new FileLink();
                    fileLink.setFileName(file.getName());
                    fileLink.setDownloadUri(path + "/" + file.getName());
                }
            }
        }
        LOGGER.info("start query workFlow from http server.size:" + fileLinks.size());
        return fileLinks;
    }

}
