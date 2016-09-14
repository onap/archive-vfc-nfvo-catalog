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

package org.openo.commontosca.catalog.model.parser;

import org.openo.commontosca.catalog.common.MsbAddrConfig;
import org.openo.commontosca.catalog.common.ToolUtil;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.entity.response.CsarFileUriResponse;
import org.openo.commontosca.catalog.model.entity.NodeTemplate;
import org.openo.commontosca.catalog.wrapper.PackageWrapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;
import java.util.zip.ZipInputStream;

public abstract class AbstractModelParser {
  private static final Logger logger = LoggerFactory.getLogger(AbstractModelParser.class);

  
  public abstract String parse(String packageId, String fileLocation)
      throws CatalogResourceException;
  
  public String copyTemporaryFile2HttpServer(String fileLocation) throws CatalogResourceException {
    String destPath = Class.class.getClass().getResource("/").getPath()
        + org.openo.commontosca.catalog.filemanage.http.ToolUtil.getHttpServerPath()
        + toTempFileLocalPath(fileLocation);
    if (!org.openo.commontosca.catalog.filemanage.http.ToolUtil.copyFile(fileLocation, destPath,
        true)) {
      throw new CatalogResourceException("Copy Temporary To HttpServer Failed.");
    }
    return destPath;
  }
  
  public String getUrl(String uri) {
    String url = null;
    if ((MsbAddrConfig.getMsbAddress().endsWith("/")) && uri.startsWith("/")) {
      url = MsbAddrConfig.getMsbAddress() + uri.substring(1);
    }
    url = MsbAddrConfig.getMsbAddress() + uri;
    String urlresult = url.replace("\\", "/");
    return urlresult;
  }
  
  protected String toTempFileLocalPath(String fileLocation) {
    return File.separator + "temp" + File.separator + (new File(fileLocation)).getName();
  }
  
  protected EnumTemplateType getTemplateType(String substitutionType, List<NodeTemplate> ntList) {
    if (isNsType(substitutionType)) {
      return EnumTemplateType.NS;
    }

    if (isVnfType(substitutionType)) {
      return EnumTemplateType.VNF;
    }

    return getTemplateTypeFromNodeTemplates(ntList);
  }
  
  private boolean isVnfType(String type) {
    if (ToolUtil.isTrimedEmptyString(type)) {
      return false;
    }
    return type.toUpperCase().contains(".VNF");
  }

  private boolean isNsType(String type) {
    if (ToolUtil.isTrimedEmptyString(type)) {
      return false;
    }
    return type.toUpperCase().contains(".NS");
  }
  
  private EnumTemplateType getTemplateTypeFromNodeTemplates(List<NodeTemplate> ntList) {
    for (NodeTemplate nt : ntList) {
      if (isNsType(nt.getType()) || isVnfType(nt.getType())) {
        return EnumTemplateType.NS;
      }
    }

    return EnumTemplateType.VNF;
  }
  
  private static final String TOSCA_META_FIELD_ENTRY_DEFINITIONS = "Entry-Definitions";
  
  protected CsarFileUriResponse buildServiceTemplateDownloadUri(String packageId, String fileLocation)
      throws CatalogResourceException {
    Map<String, String> toscaMeta = parseToscaMeta(fileLocation);
    String stFileName = toscaMeta.get(TOSCA_META_FIELD_ENTRY_DEFINITIONS);
    CsarFileUriResponse stDownloadUri =
        PackageWrapper.getInstance().getCsarFileDownloadUri(packageId, stFileName);
    return stDownloadUri;
  }
  
  @SuppressWarnings("resource")
  protected Map<String, String> parseToscaMeta(String fileLocation) throws CatalogResourceException {
    Map<String, String> toscaMeta = new HashMap<>();

    ZipInputStream zin = null;
    BufferedReader br = null;
    try {
      InputStream in = new BufferedInputStream(new FileInputStream(fileLocation));
      zin = new ZipInputStream(in);
      ZipEntry ze;
      while ((ze = zin.getNextEntry()) != null) {
        if (("TOSCA-Metadata" + File.separator + "TOSCA.meta").equals(ze.getName())
            || "TOSCA-Metadata/TOSCA.meta".equals(ze.getName())) {
          ZipFile zf = new ZipFile(fileLocation);
          br = new BufferedReader(new InputStreamReader(zf.getInputStream(ze)));
          String line;
          String[] tmps;
          while ((line = br.readLine()) != null) {
            if (line.indexOf(":") > 0) {
              tmps = line.split(":");
              toscaMeta.put(tmps[0].trim(), tmps[1].trim());
            }
          }

          return toscaMeta;
        }
      }

    } catch (IOException e1) {
      throw new CatalogResourceException("Parse Tosca Meta Fail.", e1);
    } finally {
      closeStreamAndReader(zin, br);
    }

    return toscaMeta;
  }
  
  private void closeStreamAndReader(ZipInputStream zin, BufferedReader br) {
    if (br != null) {
      try {
        br.close();
      } catch (IOException e1) {
        logger.error("Buffered reader close failed !");
      }
    }
    if (zin != null) {
      try {
        zin.closeEntry();
      } catch (IOException e2) {
        logger.error("Zip inputStream close failed !");
      }
    }
  }

}
