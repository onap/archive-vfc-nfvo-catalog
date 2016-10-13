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

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import org.openo.commontosca.catalog.common.CommonConstant;
import org.openo.commontosca.catalog.common.FileUtil;
import org.openo.commontosca.catalog.common.HttpServerAddrConfig;
import org.openo.commontosca.catalog.common.MsbAddrConfig;
import org.openo.commontosca.catalog.common.ToolUtil;
import org.openo.commontosca.catalog.db.entity.PackageData;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.resource.PackageManager;
import org.openo.commontosca.catalog.entity.CsarPackage;
import org.openo.commontosca.catalog.entity.EnumOnboardState;
import org.openo.commontosca.catalog.entity.EnumOperationalState;
import org.openo.commontosca.catalog.entity.EnumProcessState;
import org.openo.commontosca.catalog.entity.EnumType;
import org.openo.commontosca.catalog.entity.EnumUsageState;
import org.openo.commontosca.catalog.entity.request.PackageBasicInfo;
import org.openo.commontosca.catalog.entity.response.PackageMeta;
import org.openo.commontosca.catalog.ftp.Ftp;
import org.openo.commontosca.catalog.ftp.FtpUtil;
import org.openo.commontosca.catalog.model.entity.ServiceTemplate;
import org.openo.commontosca.catalog.model.externalservice.entity.lifecycle.InstanceEntity;
import org.openo.commontosca.catalog.model.externalservice.lifecycle.LifeCycleServiceConsumer;
import org.openo.commontosca.catalog.model.parser.EnumPackageFormat;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashSet;
import java.util.List;

import javax.ws.rs.NotFoundException;

public class PackageWrapperUtil {
  private static final Logger LOG = LoggerFactory.getLogger(PackageWrapperUtil.class);


  /**
   * change json to object list.
   * @param packageJson json
   * @return package list
   */
  public static List<CsarPackage> formJson2Packages(String packageJson) {
    List<CsarPackage> packageList =
        new Gson().fromJson(packageJson, new TypeToken<List<CsarPackage>>() {}.getType());
    if (null == packageList || packageList.size() == 0) {
      throw new NotFoundException("Package do not exist");
    }
    return packageList;
  }

  public static long getPacakgeSize(String fileLocation) {
    File file = new File(fileLocation);
    return file.length();
  }

  /**
   * change package metadata to fix database.
   * @param meta package metadata
   * @return package data in database 
   */
  public static PackageData getPackageData(PackageMeta meta) {
    PackageData packageData = new PackageData();
    packageData.setCreateTime(meta.getCreateTime());
    packageData.setDeletionPending(String.valueOf(meta.isDeletionPending()));
    packageData.setDownloadUri(meta.getDownloadUri());
    packageData.setFormat(meta.getFormat());
    packageData.setModifyTime(meta.getModifyTime());
    packageData.setName(meta.getName());
    packageData.setCsarId(meta.getCsarId());
    packageData.setOperationalState(meta.getOperationalState().toString());
    packageData.setProvider(meta.getProvider());
    String fileSize = meta.getSize();
    packageData.setSize(fileSize);
    packageData.setType(meta.getType());
    packageData.setUsageState(meta.getUsageState().toString());
    packageData.setVersion(meta.getVersion());
    packageData.setOnBoardState(meta.getOnBoardState());
    packageData.setProcessState(meta.getProcessState().toString());
    return packageData;
  }

  /**
   * judge wether is the end of upload package.
   * @param contentRange package sise range
   * @param csarName package name
   * @return boolean
   */
  public static boolean isUploadEnd(String contentRange, String csarName) {
    String range = contentRange;
    range = range.replace("bytes", "").trim();
    range = range.substring(0, range.indexOf("/"));
    String size =
        contentRange.substring(contentRange.indexOf("/") + 1, contentRange.length()).trim();
    int fileSize = Integer.parseInt(size);
    String[] ranges = range.split("-");
    int startPosition = Integer.parseInt(ranges[0]);
    if (startPosition == 0) {
      // delPackageBySync(csarName);
    }
    // index start from 0
    int endPosition = Integer.parseInt(ranges[1]) + 1;
    if (endPosition >= fileSize) {
      return true;
    }
    return false;
  }

  /**
   * get package detail by package id.
   * @param csarId package id
   * @return package detail
   */
  public static ArrayList<PackageData> getPackageInfoById(String csarId) {
    ArrayList<PackageData> result = new ArrayList<PackageData>();
    try {
      result = PackageManager.getInstance().queryPackageByCsarId(csarId);
    } catch (CatalogResourceException e1) {
      LOG.error("query package by csarId from db error ! " + e1.getMessage());
    }
    return result;
  }

  /**
   * get package metadata from basic info.
   * @param fileName package name
   * @param fileLocation the location of package
   * @param basic basic infomation of package. include version, type and provider
   * @return package metadata
   */
  public static PackageMeta getPackageMeta(String fileName, String fileLocation,
      PackageBasicInfo basic) {
    PackageMeta packageMeta = new PackageMeta();
    long size = getPacakgeSize(fileLocation);
    packageMeta.setFormat(basic.getFormat());
    String packageId = ToolUtil.generateId();
    packageMeta.setName(fileName.replace(CommonConstant.CSAR_SUFFIX, ""));
    packageMeta.setCsarId(packageId);
    packageMeta.setType(basic.getType().toString());
    packageMeta.setVersion(basic.getVersion());
    packageMeta.setProvider(basic.getProvider());
    packageMeta.setDeletionPending(false);
    String sizeStr = ToolUtil.getFormatFileSize(size);
    packageMeta.setSize(sizeStr);
    SimpleDateFormat sdf1 = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
    String currentTime = sdf1.format(new Date());
    packageMeta.setCreateTime(currentTime);
    packageMeta.setModifyTime(currentTime);
    packageMeta.setOperationalState(EnumOperationalState.Disabled);
    packageMeta.setUsageState(EnumUsageState.NotInUse);
    packageMeta.setOnBoardState(EnumOnboardState.nonOnBoarded.getValue());
    packageMeta.setProcessState(EnumProcessState.normal);
    return packageMeta;
  }

  /**
   * get downloadUri from package metadata.
   * @param csarId package id
   * @return download uri
   */
  public static String getPackagePath(String csarId) {
    ArrayList<PackageData> packageList = new ArrayList<PackageData>();
    String downloadUri = null;
    try {
      packageList = PackageManager.getInstance().queryPackageByCsarId(csarId);
      downloadUri = packageList.get(0).getDownloadUri();
    } catch (CatalogResourceException e1) {
      LOG.error("Query CSAR package by ID failed ! csarId = " + csarId);
    }
    return downloadUri;
  }


  /**
   * convert instance to hashset.
   * @param instancelist instance list
   * @return HashSet
   */
  public static HashSet<String> instanceConvertToHashSet(ArrayList<InstanceEntity> instancelist) {
    HashSet<String> result = new HashSet<String>();
    if (instancelist != null) {
      for (InstanceEntity instance : instancelist) {
        result.add(instance.getServiceTemplateId());
      }
    }
    return result;
  }

  /**
   * get ftp detail information.
   * @param ftpUrl ftp url
   * @return ftp detail
   */
  public static Ftp getFtpDetail(String ftpUrl) {
    Ftp ftp = new Ftp();
    int index1 = ftpUrl.indexOf("ftp://");
    int index2 = ftpUrl.indexOf("@");
    String userPassSubString = ftpUrl.substring(index1, index2);
    int index3 = userPassSubString.indexOf(":");
    String userName = userPassSubString.substring(0, index3);
    String pass = userPassSubString.substring(index3 + 1);
    String subString1 = ftpUrl.substring(index2 + 1);
    int index4 = subString1.indexOf("/");
    String ipPortSubString = subString1.substring(0, index4);
    int index5 = ipPortSubString.indexOf(":");
    String ip = ipPortSubString.substring(0, index5);
    String port = ipPortSubString.substring(index5 + 1);
    int index6 = ftpUrl.lastIndexOf("/");
    String path = ftpUrl.substring(0, index6);
    ftp.setIpAddr(ip);
    ftp.setPath(path);
    ftp.setPort(Integer.valueOf(port));
    ftp.setPwd(pass);
    ftp.setUserName(userName);
    return ftp;
  }

  /**
   * get package name from ftpUrl.
   * @param ftpUrl ftp url
   * @return package name
   */
  public static String getPackageName(String ftpUrl) {
    int index = ftpUrl.lastIndexOf("/");
    String packageName = ftpUrl.substring(index);
    return packageName;
  }

  /**
   * download package from ftp.
   * @param ftpUrl ftp url
   * @param tempDirName temp directory
   */
  public static void downPackageFromFtp(String ftpUrl, String tempDirName) {
    Ftp ftp = new Ftp();
    ftp = PackageWrapperUtil.getFtpDetail(ftpUrl);
    String remoteBaseDir = ftp.getPath();
    try {
      FtpUtil.startDown(ftp, tempDirName, remoteBaseDir);
    } catch (Exception e1) {
      LOG.error("Down package from ftp failed !");
    }
  }

  /**
   * translate package data from database to package metadata.
   * @param dbResult data from database
   * @return package metadata list
   */
  public static ArrayList<PackageMeta> packageDataList2PackageMetaList(
      ArrayList<PackageData> dbResult) {
    ArrayList<PackageMeta> metas = new ArrayList<PackageMeta>();
    PackageMeta meta = new PackageMeta();
    if (dbResult.size() > 0) {
      for (int i = 0; i < dbResult.size(); i++) {
        PackageData data = dbResult.get(i);
        meta = packageData2PackageMeta(data);
        metas.add(meta);
      }
    }
    return metas;
  }

  /**
   * get onboarded enum value.
   * @param value onboard value
   * @return enum
   */
  public static EnumOnboardState getEnumByValue(String value) {
    if (value == "non-onBoarded") {
      return EnumOnboardState.nonOnBoarded;
    } else {
      return EnumOnboardState.onBoarded;
    }
  }

  private static PackageMeta packageData2PackageMeta(PackageData packageData) {
    PackageMeta meta = new PackageMeta();
    meta.setCsarId(packageData.getCsarId());
    meta.setCreateTime(packageData.getCreateTime());
    meta.setDeletionPending(Boolean.getBoolean(packageData.getDeletionPending()));
    String packageUri =
        packageData.getDownloadUri() + packageData.getName() + CommonConstant.CSAR_SUFFIX;
    String packageUrl = getUrl(packageUri);
    meta.setDownloadUri(packageUrl);
    meta.setFormat(packageData.getFormat());
    meta.setModifyTime(packageData.getModifyTime());
    meta.setName(packageData.getName());
    meta.setOperationalState(EnumOperationalState.valueOf(packageData.getOperationalState()));
    meta.setProvider(packageData.getProvider());
    meta.setSize(packageData.getSize());
    meta.setType(packageData.getType());
    meta.setUsageState(EnumUsageState.valueOf(packageData.getUsageState()));
    meta.setVersion(packageData.getVersion());
    meta.setOnBoardState(packageData.getOnBoardState());
    String processState = packageData.getProcessState();
    if (processState.equals("deletefail")) {
      processState = "deleteFailed";
    }
    meta.setProcessState(EnumProcessState.valueOf(processState));
    return meta;
  }

  /**
   * add msb address as prefix to uri.
   * @param uri uri
   * @return url
   */
  public static String getUrl(String uri) {
    String url = null;
//    if ((MsbAddrConfig.getMsbAddress().endsWith("/")) && uri.startsWith("/")) {
//      url = MsbAddrConfig.getMsbAddress() + uri.substring(1);
//    }
//    url = MsbAddrConfig.getMsbAddress() + uri;
    if ((getDownloadUriHead().endsWith("/")) && uri.startsWith("/")) {
      url = getDownloadUriHead() + uri.substring(1);
    }
    url = getDownloadUriHead() + uri;
    String urlresult = url.replace("\\", "/");
    return urlresult;
  }
  
  public static String getDownloadUriHead() {
    return MsbAddrConfig.getMsbAddress() + "/files/catalog-http";
  }

  /**
   * get local path.
   * @param uri uri
   * @return local path
   */
  public static String getLocalPath(String uri) {
    File srcDir = new File(uri);
    String localPath = srcDir.getAbsolutePath();
    return localPath.replace("\\", "/");
  }

  /**
   * get package basic information.
   * @param fileLocation package location
   * @return package basic information
   */
  public static PackageBasicInfo getPacageBasicInfo(String fileLocation) {
    PackageBasicInfo basicInfo = new PackageBasicInfo();
    String unzipDir = ToolUtil.getUnzipDir(fileLocation);
    boolean isXmlCsar = false;
    try {
      String tempfolder = unzipDir;
      ArrayList<String> unzipFiles = FileUtil.unzip(fileLocation, tempfolder);
      if (unzipFiles.isEmpty()) {
        isXmlCsar = true;
      }
      for (String unzipFile : unzipFiles) {
        if (unzipFile.endsWith(CommonConstant.CSAR_META)) {
          basicInfo = readCsarMeta(unzipFile);
        }
        if (ToolUtil.isYamlFile(new File(unzipFile))) {
          isXmlCsar = false;
        }
      }
    } catch (IOException e1) {
      LOG.error("judge package type error !");
    }
    if (isXmlCsar) {
      basicInfo.setFormat(CommonConstant.PACKAGE_XML_FORMAT);
    } else {
      basicInfo.setFormat(CommonConstant.PACKAGE_YAML_FORMAT);
    }
    return basicInfo;
  }

  private static PackageBasicInfo readCsarMeta(String unzipFile) {
    PackageBasicInfo basicInfo = new PackageBasicInfo();
    File file = new File(unzipFile);
    BufferedReader reader = null;
    try {
      reader = new BufferedReader(new FileReader(file));
      String tempString = null;
      while ((tempString = reader.readLine()) != null) {
        if (!tempString.equals("")) {
          int count1 = tempString.indexOf(":");
          String meta = tempString.substring(0, count1).trim();
          if (meta.equalsIgnoreCase(CommonConstant.CSAR_TYPE_META)) {
            int count = tempString.indexOf(":") + 1;
            basicInfo.setType(EnumType.valueOf(tempString.substring(count).trim()));
          }
          if (meta.equalsIgnoreCase(CommonConstant.CSAR_PROVIDER_META)) {
            int count = tempString.indexOf(":") + 1;
            basicInfo.setProvider(tempString.substring(count).trim());
          }
          if (meta.equalsIgnoreCase(CommonConstant.CSAR_VERSION_META)) {
            int count = tempString.indexOf(":") + 1;
            basicInfo.setVersion(tempString.substring(count).trim());
          }
        }
      }
      reader.close();
    } catch (IOException e2) {
      e2.printStackTrace();
    } finally {
      if (reader != null) {
        try {
          reader.close();
        } catch (IOException e1) {
          LOG.error("close reader failed ! " + e1.getMessage());
        }
      }
    }
    return basicInfo;
  }
  
  /**
   * get package format enum.
   * @param format package format
   * @return package format enum
   */
  public static EnumPackageFormat getPackageFormat(String format) {
    if (format.equals("xml")) {
      return EnumPackageFormat.TOSCA_XML;
    } else if (format.equals("yml") || format.equals("yaml")) {
      return EnumPackageFormat.TOSCA_YAML;
    } else {
      return null;
    }
  }
}
