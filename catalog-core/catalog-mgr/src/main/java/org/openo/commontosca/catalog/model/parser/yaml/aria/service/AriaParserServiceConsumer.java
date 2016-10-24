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
package org.openo.commontosca.catalog.model.parser.yaml.aria.service;

import org.glassfish.jersey.client.ClientConfig;
import org.openo.commontosca.catalog.common.Config;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.model.parser.yaml.aria.entity.AriaParserRequest;
import org.openo.commontosca.catalog.model.parser.yaml.aria.entity.AriaParserResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.eclipsesource.jaxrs.consumer.ConsumerFactory;
import com.google.gson.Gson;


public class AriaParserServiceConsumer {
  private static final Logger logger = LoggerFactory.getLogger(AriaParserServiceConsumer.class);
  
  public static AriaParserResult parseCsarPackage(String uri) throws CatalogResourceException {
    logger.info("parseCsarPackage uri = " + uri);
    return parseCsarPackage(new AriaParserRequest(uri, null));
  }
  /**
   * parse csar package via aria parser.
   * 
   * @param request parse yaml request
   * @return parase yaml result
   * @throws CatalogResourceException e
   */
  public static AriaParserResult parseCsarPackage(AriaParserRequest request)
      throws CatalogResourceException {
    try {
      IAriaParserRest parseProxy =
          ConsumerFactory.createConsumer(
              Config.getConfigration().getMsbServerAddr(),
              new ClientConfig(),
              IAriaParserRest.class);
      String strResult = parseProxy.parse(request);
      AriaParserResult result = new Gson().fromJson(strResult, AriaParserResult.class);
      validateResult(result, strResult);
      return result;
    } catch (Exception e) {
      throw new CatalogResourceException("Call aria parser api failed.", e);
    }

  }
  private static void validateResult(AriaParserResult result, String strResult) throws CatalogResourceException {
    if (result.getIssues() != null && result.getIssues().length > 0) {
      logger.error("Aria parser return failure message: " + strResult);
      throw new CatalogResourceException("Aria parser return failure message: " + strResult);
    }
  }
}
