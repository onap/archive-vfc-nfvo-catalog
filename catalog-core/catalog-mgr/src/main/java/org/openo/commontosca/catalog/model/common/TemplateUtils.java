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

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;
import java.util.Map;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.model.parser.yaml.yamlmodel.Input;
import org.openo.commontosca.catalog.model.parser.yaml.yamlmodel.Plan;
import org.openo.commontosca.catalog.model.parser.yaml.yamlmodel.ServiceTemplate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.esotericsoftware.yamlbeans.YamlConfig;
import com.esotericsoftware.yamlbeans.YamlException;
import com.esotericsoftware.yamlbeans.YamlReader;

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
    config.setPropertyElementType(Plan.class, "inputs", Input.class);
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
  public static String[] readFromZipFile(String zipFileName, String zipEntryName)
      throws CatalogResourceException {
    ZipFile zf = null;
    InputStream ins = null;
    try {
      zf = new ZipFile(zipFileName);
      ZipEntry ze = getZipEntryZipFile(zf, zipEntryName);
      
      if (ze != null) {
        ins = zf.getInputStream(ze);
        return readFromInputStream(ins);
      }
    } catch (IOException e) {
      throw new CatalogResourceException("readFromZipFile failed.", e);
    } finally {
      closeInputStream(ins);
      closeZipFile(zf);
    }
    return new String[0];
  }

  public static ZipEntry getZipEntryZipFile(ZipFile zf, String zipEntryName) {
    Enumeration<?> zes = zf.entries();
    while (zes.hasMoreElements()) {
      ZipEntry ze = (ZipEntry) zes.nextElement();
      if (zipEntryName.equals(ze.getName())
          || (zipEntryName.replaceAll("\\\\", "/")).equals(ze.getName())) {
        return ze;
      }
    }
    
    return null;
  }

  /**
   * @param ins
   */
  public static void closeInputStream(InputStream ins) {
    if (ins != null) {
      try {
        ins.close();
      } catch (IOException e) {
        logger.warn("closeInputStream failed.", e);
      }
    }
  }
  
  /**
   * @param zf
   */
  public static void closeZipFile(ZipFile zf) {
    if (zf != null) {
      try {
        zf.close();
      } catch (IOException e) {
        logger.warn("closeZipFile failed.", e);
      }
    }
  }

  private static String[] readFromInputStream(InputStream ins) throws CatalogResourceException {
    InputStreamReader insReader = new InputStreamReader(ins);
    BufferedReader reader = new BufferedReader(insReader);
    
    List<String> lineList = new ArrayList<>();
    String line;
    try {
      while ((line = reader.readLine()) != null) {
        lineList.add(line);
      }
    } catch (IOException e) {
      throw new CatalogResourceException("readFromInputStream failed.", e);
    } finally {
      closeReader(reader);
      closeReader(insReader);
    }
    
    return lineList.toArray(new String[0]);
  }
  
  /**
   * @param reader
   */
  private static void closeReader(Reader reader) {
    if (reader != null) {
      try {
        reader.close();
      } catch (IOException e) {
        logger.warn("closeReader failed.", e);
      }
    }
  }
}
