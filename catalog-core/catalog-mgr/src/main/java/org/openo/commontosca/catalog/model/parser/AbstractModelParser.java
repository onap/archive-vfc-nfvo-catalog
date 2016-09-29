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
package org.openo.commontosca.catalog.model.parser;

import org.openo.commontosca.catalog.common.Config;
import org.openo.commontosca.catalog.common.ToolUtil;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.model.common.TemplateUtils;
import org.openo.commontosca.catalog.model.entity.NodeTemplate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public abstract class AbstractModelParser {
  private static final Logger logger = LoggerFactory.getLogger(AbstractModelParser.class);

  public abstract String parse(String packageId, String fileLocation)
      throws CatalogResourceException;
  
  public String copyTemporaryFile2HttpServer(String fileLocation) throws CatalogResourceException {
    String destPath = org.openo.commontosca.catalog.filemanage.http.ToolUtil.getHttpServerAbsolutePath()
        + toTempFilePath(fileLocation);
    if (!org.openo.commontosca.catalog.filemanage.http.ToolUtil.copyFile(
        fileLocation, destPath, true)) {
      throw new CatalogResourceException("Copy Temporary To HttpServer Failed.");
    }
    
    logger.info("destPath = " + destPath);
    return destPath;
  }
  
  public String getUrlOnHttpServer(String path) {
    return Config.getConfigration().getHttpServerAddr() + "/" + path;
  }
  
  protected String toTempFilePath(String fileLocation) {
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
    return type.toUpperCase().endsWith(".VNF") || type.toUpperCase().contains(".VNF.");
  }

  private boolean isNsType(String type) {
    if (ToolUtil.isTrimedEmptyString(type)) {
      return false;
    }
    return type.toUpperCase().endsWith(".NS") || type.toUpperCase().contains(".NS.");
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
  
  protected String parseServiceTemplateFileName(String packageId, String fileLocation)
      throws CatalogResourceException {
    return File.separator + parseToscaMeta(fileLocation).get(TOSCA_META_FIELD_ENTRY_DEFINITIONS);
  }
  
  private static final String TOSCA_META_FILE_NAME = "TOSCA-Metadata/TOSCA.meta";
  protected Map<String, String> parseToscaMeta(String zipLocation) throws CatalogResourceException {
    Map<String, String> toscaMeta = new HashMap<>();
    String[] lines = TemplateUtils.readFromZipFile(zipLocation, TOSCA_META_FILE_NAME);

    for (String line : lines) {
      String[] tmps;
      if (line.indexOf(":") > 0) {
        tmps = line.split(":");
        toscaMeta.put(tmps[0].trim(), tmps[1].trim());
      }
    }

    return toscaMeta;
  }

  

}
