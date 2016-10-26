/**
 * Copyright 2016 ZTE Corporation.
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
package org.openo.commontosca.catalog.wrapper;

import org.glassfish.jersey.media.multipart.FormDataContentDisposition;
import org.openo.commontosca.catalog.common.CommonConstant;
import org.openo.commontosca.catalog.common.HttpServerPathConfig;
import org.openo.commontosca.catalog.common.RestUtil;
import org.openo.commontosca.catalog.common.ToolUtil;
import org.openo.commontosca.catalog.db.entity.PackageData;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.resource.PackageManager;
import org.openo.commontosca.catalog.db.resource.TemplateManager;
import org.openo.commontosca.catalog.entity.request.PackageBasicInfo;
import org.openo.commontosca.catalog.entity.response.CsarFileUriResponse;
import org.openo.commontosca.catalog.entity.response.PackageMeta;
import org.openo.commontosca.catalog.entity.response.UploadPackageResponse;
import org.openo.commontosca.catalog.filemanage.FileManagerFactory;
import org.openo.commontosca.catalog.model.parser.ModelParserFactory;
import org.openo.commontosca.catalog.model.service.ModelService;
import org.openo.commontosca.catalog.resources.CatalogBadRequestException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

import javax.ws.rs.core.HttpHeaders;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.Response.Status;

public class PackageWrapper {
  private static PackageWrapper packageWrapper;
  private static final Logger LOG = LoggerFactory.getLogger(PackageWrapper.class);

  /**
   * get PackageWrapper instance.
   * @return package wrapper instance
   */
  public static PackageWrapper getInstance() {
    if (packageWrapper == null) {
      packageWrapper = new PackageWrapper();
    }
    return packageWrapper;
  }

  /**
   * query package by id.
   * @param csarId package id
   * @return Response
   */
  public Response queryPackageById(String csarId) {
    PackageData dbResult = new PackageData();
    PackageMeta result = new PackageMeta();
    dbResult = PackageWrapperUtil.getPackageInfoById(csarId);
    result = PackageWrapperUtil.packageData2PackageMeta(dbResult);
    return Response.ok(result).build();
  }

  /**
   * upload package.
   * @param uploadedInputStream inputStream
   * @param fileDetail package detail
   * @param head http header
   * @return Response
   * @throws Exception e
   */
  public Response uploadPackage(InputStream uploadedInputStream,
      FormDataContentDisposition fileDetail, HttpHeaders head) throws Exception {
    int fileSize = 0;
    if (uploadedInputStream == null) {
      LOG.info("the uploadStream is null");
      return Response.serverError().build();
    }
    if (fileDetail == null) {
      LOG.info("the fileDetail is null");
      return Response.serverError().build();
    }
    LOG.info("the fileDetail = " + ToolUtil.objectToString(fileDetail));
    String contentRange = null;
    String fileName = "";
    fileName = ToolUtil.processFileName(fileDetail.getFileName());
    String tempDirName = null;
    tempDirName = ToolUtil.getTempDir(CommonConstant.CATALOG_CSAR_DIR_NAME, fileName);
    if (head != null) {
      contentRange = head.getHeaderString(CommonConstant.HTTP_HEADER_CONTENT_RANGE);
    }
    LOG.info("store package chunk file, fileName:" + fileName + ",contentRange:" + contentRange);
    if (ToolUtil.isEmptyString(contentRange)) {
      fileSize = uploadedInputStream.available();
      contentRange = "0-" + fileSize + "/" + fileSize;
    }
    String fileLocation =
        ToolUtil.storeChunkFileInLocal(tempDirName, fileName, uploadedInputStream);
    LOG.info("the fileLocation when upload package is :" + fileLocation);
    uploadedInputStream.close();

    Boolean isEnd = PackageWrapperUtil.isUploadEnd(contentRange, fileName);
    PackageData packateDbData = new PackageData();
    UploadPackageResponse result = new UploadPackageResponse();
    if (isEnd) {
      PackageBasicInfo basicInfo = new PackageBasicInfo();
      basicInfo = PackageWrapperUtil.getPacageBasicInfo(fileLocation);
      String path =
          basicInfo.getType().toString() + File.separator + basicInfo.getProvider() + File.separator
              + fileName.replace(".csar", "") + File.separator + basicInfo.getVersion();
      LOG.info("dest path is : " + path);
      PackageMeta packageMeta = new PackageMeta();
      packageMeta = PackageWrapperUtil.getPackageMeta(fileName, fileLocation, basicInfo);
      String dowloadUri = File.separator + path + File.separator;
      String destPath = File.separator + path;
      packageMeta.setDownloadUri(dowloadUri);
      LOG.info("packageMeta = " + ToolUtil.objectToString(packageMeta));
      
      String serviceTemplateId = null;
      boolean uploadResult = FileManagerFactory.createFileManager().upload(tempDirName, destPath);
      if (uploadResult == true) {
        PackageData packageData = PackageWrapperUtil.getPackageData(packageMeta);
        ArrayList<PackageData> existPackageDatas =
            PackageManager.getInstance().queryPackage(packageData.getName(),
                packageData.getProvider(), packageData.getVersion(), null, packageData.getType());
        if (null != existPackageDatas && existPackageDatas.size() > 0) {
          LOG.warn("The package already exist ! Begin to delete the orgin data and reupload !");
          for (int i = 0; i < existPackageDatas.size(); i++) {
            this.delPackage(existPackageDatas.get(i).getCsarId());
          }
        } 
        packateDbData = PackageManager.getInstance().addPackage(packageData);
        LOG.info("Store package data to database succed ! packateDbData = "
            + ToolUtil.objectToString(packateDbData));
        try {
          String tempCsarPath = tempDirName + File.separator + fileName;
          serviceTemplateId = ModelParserFactory.getInstance().parse(packateDbData.getCsarId(),
              tempCsarPath, PackageWrapperUtil.getPackageFormat(packateDbData.getFormat()));
          LOG.info("Package parse success ! serviceTemplateId = " + serviceTemplateId);
        } catch (Exception e1) {
          LOG.error("Parse package error ! ");
          String packagePath = PackageWrapperUtil.getPackagePath(packageData.getCsarId());
          FileManagerFactory.createFileManager().delete(packagePath);
          if (tempDirName != null) {
            ToolUtil.deleteDir(new File(tempDirName));
          }
          PackageManager.getInstance().deletePackage(packateDbData.getCsarId());
          throw new Exception(e1);
        }

        if (null != packateDbData && null == serviceTemplateId) {
          LOG.info("Service template Id is null !");
          PackageManager.getInstance().deletePackage(packateDbData.getCsarId());
        }
      }
      LOG.info("upload package file end, fileName:" + fileName);
      result.setCsarId(packateDbData.getCsarId());
      if (tempDirName != null) {
        ToolUtil.deleteDir(new File(tempDirName));
      }
    }
    return Response.ok(result).build();
  }

  /**
   * delete package by package id.
   * @param csarId package id
   * @return Response
   */
  public Response delPackage(String csarId) {
    LOG.info("delete package  info.csarId:" + csarId);
    if (ToolUtil.isEmptyString(csarId)) {
      LOG.error("delete package  fail, csarid is null");
      return Response.serverError().build();
    }
    try {
      DelCsarThread thread = new DelCsarThread(csarId, false);
      new Thread(thread).start();
      return Response.noContent().build();
    } catch (Exception e1) {
      LOG.error("delete fail." + e1.getMessage());
      return RestUtil.getRestException(e1.getMessage());
    }
  }

  class DelCsarThread implements Runnable {
    private String csarid;
    private boolean isInstanceTemplate = false;

    public DelCsarThread(String csarid, boolean isInstanceTemplate) {
      this.csarid = csarid;
      this.isInstanceTemplate = isInstanceTemplate;
    }

    @Override
    public void run() {
      try {
        if (!ToolUtil.isEmptyString(csarid)) {
          delCsarData(csarid);
        }
      } catch (Exception e1) {
        LOG.error("del instance csar fail."+ e1.getMessage());
        updatePackageStatus(csarid, null, null, null, CommonConstant.PACKAGE_STATUS_DELETE_FAIL,
            null);
        // publishDelFinishCometdMessage(csarid, "false");
      }
    }

    private void delCsarData(String csarId) {
      updatePackageStatus(csarid, null, null, null, CommonConstant.PACKAGE_STATUS_DELETING, null);
      String packagePath = PackageWrapperUtil.getPackagePath(csarId);
      if (packagePath == null) {
        LOG.error("package path is null! ");
        return;
      }
      FileManagerFactory.createFileManager().delete(packagePath);
      // delete template data from db
      try {
        ModelService.getInstance().delete(csarId);
      } catch (CatalogBadRequestException e) {
        LOG.error("delete template data from db error! csarId = " + csarId, e);
      } catch (CatalogResourceException e) {
        LOG.error("delete template data from db error! csarId = " + csarId, e);
      }
//      PackageData packageData = new PackageData();
//      packageData.setCsarId(csarId);
//      try {
//        TemplateManager.getInstance().deleteServiceTemplateByCsarPackageInfo(packageData);
//      } catch (CatalogResourceException e2) {
//        LOG.error("delete template data from db error! csarId = " + csarId);
//      }
      //delete package data from database
      try {
        PackageManager.getInstance().deletePackage(csarId);
      } catch (CatalogResourceException e1) {
        LOG.error("delete package  by csarId from db error ! " + e1.getMessage(), e1);
      }
    }

    // private void publishDelFinishCometdMessage(String csarid, String csarDelStatus) {
    // if (isInstanceTemplate) {
    // LOG.info("delete instance Template finish. csarid:{}", csarid);
    // return;
    // }
    // try {
    // Map<String, Object> cometdMessage = new HashMap<String, Object>();
    // cometdMessage.put("csarid", csarid);
    // cometdMessage.put("status", csarDelStatus);
    // CometdService.getInstance().publish(CommonConstant.COMETD_CHANNEL_PACKAGE_DELETE,
    // cometdMessage);
    // } catch (CometdException e) {
    // LOG.error("publish delfinish cometdmsg fail.", e);
    // }
    // }
  }

  /**
   * update package status.
   * @param csarId package id
   * @param operationalState package operational state
   * @param usageState package usage state
   * @param onBoardState package onboard state
   * @param processState package process state
   * @param deletionPending package deletionPending status
   * @return Response
   */
  public Response updatePackageStatus(String csarId, String operationalState, String usageState,
      String onBoardState, String processState, String deletionPending) {
    LOG.info("update package status info.csarId:" + csarId + " operationalState:"
        + operationalState);
    if (ToolUtil.isEmptyString(csarId)) {
      LOG.error("update csar status fail, csarid is null");
      return Response.serverError().build();
    }
    try {
      // UpdatePackageResponse result = new UpdatePackageResponse();
      PackageData packageInfo = new PackageData();
      if (operationalState != null) {
        packageInfo.setOperationalState(operationalState);
      }
      if (usageState != null) {
        packageInfo.setUsageState(usageState);
      }
      if (onBoardState != null) {
        packageInfo.setOnBoardState(onBoardState);
      }
      if (processState != null) {
        packageInfo.setProcessState(processState);
      }
      if (deletionPending != null) {
        packageInfo.setDeletionPending(deletionPending);
      }
      SimpleDateFormat sdf1 = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
      String currentTime = sdf1.format(new Date());
      packageInfo.setModifyTime(currentTime);
      PackageManager.getInstance().updatePackage(packageInfo, csarId);
      // ArrayList<PackageData> pacackgeList = PackageWrapperUtil.getPackageInfoById(csarId);
      // String finalUsageState = pacackgeList.get(0).getUsageState();
      // result.setUsageState(finalUsageState);
      return Response.ok().build();
    } catch (CatalogResourceException e1) {
      LOG.error("update package status by csarId from db error ! " + e1.getMessage());
      return RestUtil.getRestException(e1.getMessage());
    }
  }

  /**
   * download package by package id.
   * @param csarId package id
   * @return Response
   */
  public Response downloadCsarPackagesById(String csarId) {
    PackageData packageData = PackageWrapperUtil.getPackageInfoById(csarId);
    String packageName = null;
    packageName = packageData.getName();
    String path = ToolUtil.getCatalogueCsarPath() + File.separator + packageName;
    File csarFile = new File(path);
    if (!csarFile.exists()) {
      return Response.status(Status.NOT_FOUND).build();
    }

    try {
      InputStream fis = new BufferedInputStream(new FileInputStream(path));
      return Response.ok(fis)
          .header("Content-Disposition", "attachment; filename=\"" + csarFile.getName() + "\"")
          .build();
    } catch (Exception e1) {
      LOG.error("download vnf package fail.", e1);
      return RestUtil.getRestException(e1.getMessage());
    }
  }

  /**
   * query package list by condition.
   * @param name package name
   * @param provider package provider
   * @param version package version
   * @param deletionPending package deletionPending
   * @param type package type
   * @return Response
   */
  public Response queryPackageListByCond(String name, String provider, String version,
      String deletionPending, String type) {
    ArrayList<PackageData> dbresult = new ArrayList<PackageData>();
    ArrayList<PackageMeta> result = new ArrayList<PackageMeta>();
    LOG.info("query package info.name:" + name + " provider:" + provider + " version" + version
        + " deletionPending" + deletionPending + " type:" + type);
    try {
      dbresult =
          PackageManager.getInstance().queryPackage(name, provider, version, deletionPending, type);
      result = PackageWrapperUtil.packageDataList2PackageMetaList(dbresult);
      return Response.ok(result).build();
    } catch (CatalogResourceException e1) {
      LOG.error("query package by csarId from db error ! " + e1.getMessage());
      return RestUtil.getRestException(e1.getMessage());
    }
  }

  /**
   * get package file uri.
   * @param csarId package id
   * @param relativePath file relative path
   * @return Response
   */
  public Response getCsarFileUri(String csarId, String relativePath) {
    try {
      CsarFileUriResponse result = getCsarFileDownloadUri(csarId, relativePath);
      return Response.ok(result).build();
    } catch (CatalogResourceException e1) {
      LOG.error("Query CSAR package by ID failed ! csarId = " + csarId);
    }

    return Response.serverError().build();
  }

  /**
   * get package file download uri.
   * @param csarId package id
   * @param relativePath package file relative path
   * @return CsarFileUriResponse
   * @throws CatalogResourceException e
   */
  public CsarFileUriResponse getCsarFileDownloadUri(String csarId, String relativePath)
      throws CatalogResourceException {
    CsarFileUriResponse result = new CsarFileUriResponse();
    String downloadUrl = null;
    String downloadUri = null;
    String localPath = null;
    ArrayList<PackageData> packageList = PackageManager.getInstance().queryPackageByCsarId(csarId);
    if (packageList != null && packageList.size() != 0) {
      String packageName = packageList.get(0).getName();
      String relativeUri = packageList.get(0).getDownloadUri() + packageName;
      downloadUri = relativeUri + relativePath;
      downloadUrl = PackageWrapperUtil.getUrl(downloadUri);
      String httpUri = HttpServerPathConfig.getHttpServerPath() + downloadUri;
      localPath = PackageWrapperUtil.getLocalPath(httpUri);
    }
    result.setDownloadUri(downloadUrl);
    result.setLocalPath(localPath);
    return result;
  }

  
}
