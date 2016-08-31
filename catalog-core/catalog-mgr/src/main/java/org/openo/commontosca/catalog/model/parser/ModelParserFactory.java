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

import org.openo.commontosca.catalog.db.exception.CatalogResourceException;

import java.util.HashMap;
import java.util.Map;


public class ModelParserFactory {
  private static final ModelParserFactory instance = new ModelParserFactory();

  public static ModelParserFactory getInstance() {
    return instance;
  }

  private Map<EnumPackageFormat, AbstractModelParser> pkgType2ParseMap =
      new HashMap<EnumPackageFormat, AbstractModelParser>();

  private ModelParserFactory() {
    // PackageParseMap.put(EnumPackageFormat.TOSCA_XML, new
    // ToscaXmlModelParser());
    pkgType2ParseMap.put(EnumPackageFormat.TOSCA_YAML, new ToscaYamlModelParser());
  }

  /**
   * parse package.
   * @param packageId package id
   * @param fileLocation package location
   * @param format package format
   * @return service template id 
   * @throws CatalogResourceException e
   */
  public String parse(String packageId, String fileLocation, EnumPackageFormat format)
      throws CatalogResourceException {
    if (pkgType2ParseMap.get(format) == null) {
      throw new CatalogResourceException("Can't find its parser. package type = "
          + format.toString());
    }

    return pkgType2ParseMap.get(format).parse(packageId, fileLocation);
  }
}
