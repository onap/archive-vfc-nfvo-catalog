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
package org.openo.commontosca.catalog.model.common;

import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.model.parser.yaml.yamlmodel.Plan;
import org.openo.commontosca.catalog.model.parser.yaml.yamlmodel.ServiceTemplate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.esotericsoftware.yamlbeans.YamlConfig;
import com.esotericsoftware.yamlbeans.YamlException;
import com.esotericsoftware.yamlbeans.YamlReader;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;
import java.util.zip.ZipInputStream;

public class TemplateUtils {
  private static final Logger logger = LoggerFactory.getLogger(TemplateUtils.class);
  
  public static Map<String, Plan> loadPlan(String yamlString) throws CatalogResourceException {
    ServiceTemplate st = loadServiceTemplate(yamlString);
    return st.getPlans();
  }
  
  /**
   * @param yamlString
   * @return
   * @throws CatalogResourceException
   */
  public static ServiceTemplate loadServiceTemplate(String yamlString) throws CatalogResourceException {
    if (yamlString == null || yamlString.isEmpty()) {
      return new ServiceTemplate();
    }
    final YamlReader reader = new YamlReader(yamlString);
    adjustConfig(reader.getConfig());
    try {
        return reader.read(ServiceTemplate.class);
    } catch (final YamlException e) {
        throw new CatalogResourceException("Load plan information failed.", e);
    } finally {
      if (reader != null) {
        try {
            reader.close();
        } catch (IOException e) {
        }
      }
    }
}
  
  
  /**
   * @param config
   */
  private static void adjustConfig(YamlConfig config) {
    config.setPropertyElementType(ServiceTemplate.class, "plans", Plan.class);
  }


  /**
   * @param zipFileName
   * @param zipEntryName
   * @return
   * @throws CatalogResourceException
   */
  public static String readStringFromZipFile(String zipFileName, String zipEntryName) throws CatalogResourceException {
    String[] lines = readFromZipFile(zipFileName, zipEntryName);
    StringBuffer sb = new StringBuffer();
    for (String line : lines) {
      sb.append(line).append(System.lineSeparator());
    }
    return sb.toString();
  }
  
  /**
   * @param zipFileName
   * @param zipEntryName
   * @return
   * @throws CatalogResourceException
   */
  @SuppressWarnings("resource")
  public static String[] readFromZipFile(String zipFileName, String zipEntryName)
      throws CatalogResourceException {
    ZipInputStream zipIns = null;
    BufferedReader zipEntryBr = null;
    try {
      ZipFile zipFile = new ZipFile(zipFileName);
      
      zipIns = new ZipInputStream(new BufferedInputStream(new FileInputStream(zipFileName)));
      ZipEntry zipEntry;
      while ((zipEntry = zipIns.getNextEntry()) != null) {
        if (zipEntryName.equals(zipEntry.getName())
            || (zipEntryName.replaceAll("/", "\\\\")).equals(zipEntry.getName())) {
          zipEntryBr = new BufferedReader(new InputStreamReader(zipFile.getInputStream(zipEntry)));
          List<String> lineList = new ArrayList<>();
          String line;
          while ((line = zipEntryBr.readLine()) != null) {
            lineList.add(line);
          }
          
          return lineList.toArray(new String[0]);
        }
      }
    } catch (IOException e) {
      throw new CatalogResourceException("Parse Tosca Meta Fail.", e);
    } finally {
      closeStreamAndReader(zipIns, zipEntryBr);
    }
    return new String[0];
  }
  
  private static void closeStreamAndReader(ZipInputStream zin, BufferedReader br) {
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
