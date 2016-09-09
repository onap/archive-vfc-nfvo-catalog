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

package org.openo.commontosca.catalog.wrapper;

import org.glassfish.jersey.media.multipart.FormDataContentDisposition;
import org.openo.commontosca.catalog.common.CommonConstant;
import org.openo.commontosca.catalog.common.HttpServerPathConfig;
import org.openo.commontosca.catalog.common.RestUtil;
import org.openo.commontosca.catalog.common.ToolUtil;
import org.openo.commontosca.catalog.common.ZipCompressor;
import org.openo.commontosca.catalog.db.entity.PackageData;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.resource.PackageManager;
import org.openo.commontosca.catalog.db.resource.TemplateManager;
import org.openo.commontosca.catalog.entity.EnumType;
import org.openo.commontosca.catalog.entity.request.PackageBasicInfo;
import org.openo.commontosca.catalog.entity.request.UploadPackageFromFtpRequest;
import org.openo.commontosca.catalog.entity.response.CsarFileUriResponse;
import org.openo.commontosca.catalog.entity.response.PackageMeta;
import org.openo.commontosca.catalog.entity.response.UploadPackageResponse;
import org.openo.commontosca.catalog.filemanage.FileManagerFactory;
import org.openo.commontosca.catalog.filemanage.entity.FileLink;
import org.openo.commontosca.catalog.model.parser.EnumPackageFormat;
import org.openo.commontosca.catalog.model.parser.ModelParserFactory;
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
    ArrayList<PackageData> dbResult = new ArrayList<PackageData>();
    ArrayList<PackageMeta> result = new ArrayList<PackageMeta>();
    dbResult = PackageWrapperUtil.getPackageInfoById(csarId);
    if (dbResult.size() != 0) {
      result = PackageWrapperUtil.packageDataList2PackageMetaList(dbResult);
      return Response.ok(result).build();
    } else {
      String errorMsg = "get package info by Id error !";
      return RestUtil.getRestException(errorMsg);
    }
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
    PackageBasicInfo basicInfo = new PackageBasicInfo();
    String tempDirName = null;
    int fileSize = 0;
    String fileName = "";
    UploadPackageResponse result = new UploadPackageResponse();
    PackageMeta packageMeta = new PackageMeta();
    if (uploadedInputStream == null) {
      LOG.info("the uploadStream is null");
      return Response.serverError().build();
    }
    if (fileDetail == null) {
      LOG.info("the fileDetail is null");
      return Response.serverError().build();
    }

    try {
      String contentRange = null;
      fileName = ToolUtil.processFileName(fileDetail.getFileName());
      tempDirName = ToolUtil.getTempDir(CommonConstant.CATALOG_CSAR_DIR_NAME, fileName);
      if (head != null) {
        contentRange = head.getHeaderString(CommonConstant.HTTP_HEADER_CONTENT_RANGE);
      }
      LOG.debug("store package chunk file, fileName:" + fileName + ",contentRange:" + contentRange);
      if (ToolUtil.isEmptyString(contentRange)) {
        fileSize = uploadedInputStream.available();
        contentRange = "0-" + fileSize + "/" + fileSize;
      }
      String fileLocation =
          ToolUtil.storeChunkFileInLocal(tempDirName, fileName, uploadedInputStream);
      LOG.info("the fileLocation when upload package is :" + fileLocation);
      uploadedInputStream.close();

      basicInfo = PackageWrapperUtil.getPacageBasicInfo(fileLocation);
      String path =
          basicInfo.getType().toString() + File.separator + basicInfo.getProvider()
              + File.separator + fileName.replace(".csar", "") + File.separator
              + basicInfo.getVersion();
      LOG.info("dest path is : " + path);
      packageMeta = PackageWrapperUtil.getPackageMeta(fileName, fileLocation, basicInfo);
      String dowloadUri = File.separator + path + File.separator;
      String destPath = File.separator + path;
      packageMeta.setDownloadUri(dowloadUri);
      LOG.info("packageMeta = " + ToolUtil.objectToString(packageMeta));
      Boolean isEnd = PackageWrapperUtil.isUploadEnd(contentRange, fileName);
      if (isEnd) {
        boolean uploadResult = FileManagerFactory.createFileManager().upload(tempDirName, destPath);
        if (uploadResult == true) {
          try {
            String tempCsarPath = tempDirName + File.separator + fileName;
            ModelParserFactory.getInstance().parse(packageMeta.getCsarId(),
                tempCsarPath , PackageWrapperUtil.getPackageFormat(packageMeta.getFormat()));
          } catch (CatalogResourceException e1) {
            LOG.error("parse package error ! " + e1.getMessage());
          }
          PackageData packageData = PackageWrapperUtil.getPackageData(packageMeta);
          PackageManager.getInstance().addPackage(packageData);
        }
        LOG.info("upload package file end, fileName:" + fileName);
      }
      result.setCsarId(packageMeta.getCsarId());
      return Response.ok(result).build();
    } catch (Exception e1) {
      LOG.error("upload package fail.", e1);
      String csarId = packageMeta.getCsarId();
      if (csarId != null) {
        PackageManager.getInstance().deletePackage(csarId);
      }
      return RestUtil.getRestException(e1.getMessage());
    } finally {
      if (tempDirName != null) {
        ToolUtil.deleteDir(new File(tempDirName));
      }
    }
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
      LOG.error("delete fail.", e1);
      return RestUtil.getRestException(e1.getMessage());
    }
  }

  // public Response delPackageByServiceTemplateId(String serviceTemplateId) {
  // LOG.info("delete package  info.serviceTemplateId:" + serviceTemplateId);
  // if (ToolUtil.isEmptyString(serviceTemplateId)) {
  // LOG.error("delete package  fail, serviceTemplateId is null");
  // return Response.serverError().build();
  // }
  // ArrayList<PackageData> result = new ArrayList<PackageData>();
  // try {
  // result = PackageManager.getInstance().queryPackageByServiceTemplateId(serviceTemplateId);
  //
  // } catch (CatalogResourceException e) {
  // LOG.error("query package by csarId from db error ! " + e.getMessage());
  // return RestUtil.getRestException(e.getMessage());
  // }
  // if (result.size() <= 0) {
  // LOG.warn("not exist package by serviceTemplateId");
  // return Response.status(Status.NOT_FOUND).build();
  // }
  // if ("true".equals(result.get(0).getDeletionPending())) {
  // LOG.info("start delete package.csarId:" + result.get(0).getCsarId());
  // delCsarThread thread = new delCsarThread(result.get(0).getCsarId(), true);
  // new Thread(thread).start();
  // }
  // return Response.noContent().build();
  // }

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
        LOG.error("del instance csar fail.", e1);
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
      try {
        PackageManager.getInstance().deletePackage(csarId);
      } catch (CatalogResourceException e1) {
        LOG.error("delete package  by csarId from db error ! " + e1.getMessage());
      }
      // delete template data from db
      PackageData packageData = new PackageData();
      packageData.setCsarId(csarId);
      try {
        TemplateManager.getInstance().deleteServiceTemplateByCsarPackageInfo(packageData);
      } catch (CatalogResourceException e2) {
        LOG.error("delete template data from db error! csarId = " + csarId);
      }
      // publishDelFinishCometdMessage(csarid, "true");
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
    ArrayList<PackageData> packageList = PackageWrapperUtil.getPackageInfoById(csarId);
    String packageName = null;
    if (null != packageList && packageList.size() > 0) {
      packageName = packageList.get(0).getName();
    }
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

  /**
   * upload package from ftp.
   * @param request package basic information
   * @return Response
   */
  public Response uploadPackageFromFtp(UploadPackageFromFtpRequest request) {
    PackageBasicInfo basicInfo = new PackageBasicInfo();
    String tempDirName = null;
    String fileName = "";
    UploadPackageResponse result = new UploadPackageResponse();
    basicInfo.setProvider("zte");
    basicInfo.setType(EnumType.NSAR);
    basicInfo.setVersion("v1.0");
    PackageMeta packageMeta = new PackageMeta();

    try {
      String ftpUrl = request.getFtpUrl();
      String packageName = PackageWrapperUtil.getPackageName(ftpUrl);
      fileName = ToolUtil.processFileName(packageName);
      tempDirName = ToolUtil.getTempDir(CommonConstant.CATALOG_CSAR_DIR_NAME, fileName);
      PackageWrapperUtil.downPackageFromFtp(ftpUrl, tempDirName);
      String path =
          basicInfo.getType().toString() + File.separator + basicInfo.getProvider()
              + File.separator + fileName.replace(".csar", "") + File.separator
              + basicInfo.getVersion();
      LOG.info("dest path is : " + path);
      packageMeta = PackageWrapperUtil.getPackageMeta(fileName, tempDirName, basicInfo);
      String dowloadUri = File.separator + path + File.separator + fileName;
      packageMeta.setDownloadUri(dowloadUri);
      LOG.info("packageMeta = " + ToolUtil.objectToString(packageMeta));
      String destPath = File.separator + path;
      boolean uploadResult = FileManagerFactory.createFileManager().upload(tempDirName, destPath);
      if (uploadResult == true) {
        String newZipPath = tempDirName + fileName.replace(".csar", ".zip");
        ZipCompressor zc = new ZipCompressor(newZipPath);
        String metadataPath = tempDirName + File.separator + CommonConstant.TOSCA_METADATA;
        String definitions = tempDirName + File.separator + CommonConstant.DEFINITIONS;
        zc.compress(metadataPath, definitions);
        String parseResult = ModelParserFactory.getInstance().parse(packageMeta.getCsarId(),
            newZipPath, EnumPackageFormat.valueOf(packageMeta.getFormat()));
        PackageData packageData = PackageWrapperUtil.getPackageData(packageMeta);
        PackageManager.getInstance().addPackage(packageData);
      }
      LOG.info("upload package file end, fileName:" + fileName);
      result.setCsarId(packageMeta.getCsarId());
      return Response.ok(result).build();
    } catch (Exception e1) {
      LOG.error("upload package fail.", e1);
      String csarId = packageMeta.getCsarId();
      if (csarId != null) {
        try {
          PackageManager.getInstance().deletePackage(csarId);
        } catch (CatalogResourceException e2) {
          LOG.error("delete package failed !");
        }
      }
      return RestUtil.getRestException(e1.getMessage());
    } finally {
      if (tempDirName != null) {
        ToolUtil.deleteDir(new File(tempDirName));
      }
    }
  }

  /**
   * get csar plan uri.
   * @param csarId package id
   * @return Response
   */
  public Response getCsarPlansUri(String csarId) {
    ArrayList<FileLink> fileLinks = new ArrayList<FileLink>();
    LOG.info("start query plans of package.csarId:" + csarId);
    ArrayList<PackageData> packageList = new ArrayList<PackageData>();
    try {
      packageList = PackageManager.getInstance().queryPackageByCsarId(csarId);
      if (packageList != null && packageList.size() != 0) {
        String downloadUri = packageList.get(0).getDownloadUri();
        fileLinks = FileManagerFactory.createFileManager().queryWorkFlow(downloadUri);
      }
      return Response.ok(fileLinks).build();
    } catch (CatalogResourceException e1) {
      LOG.error("Query plans of  package by ID failed ! csarId = " + csarId);
      return RestUtil.getRestException(e1.getMessage());
    }
    // return Response.serverError().build();
  }
}
