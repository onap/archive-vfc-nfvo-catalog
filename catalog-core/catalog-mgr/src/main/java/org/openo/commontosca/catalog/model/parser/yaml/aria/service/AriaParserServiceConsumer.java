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

package org.openo.commontosca.catalog.model.parser.yaml.aria.service;

import org.glassfish.jersey.client.ClientConfig;
import org.openo.commontosca.catalog.common.Config;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.model.parser.yaml.aria.entity.AriaParserRequest;
import org.openo.commontosca.catalog.model.parser.yaml.aria.entity.AriaParserResult;

import com.eclipsesource.jaxrs.consumer.ConsumerFactory;
import com.google.gson.Gson;


public class AriaParserServiceConsumer {
  public static AriaParserResult parseCsarPackage(String uri) throws CatalogResourceException {
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
              Config.getConfigration().getAriaParserAddr(),
              new ClientConfig(),
              IAriaParserRest.class);
      String jsonStr = parseProxy.parse(request);
      return new Gson().fromJson(jsonStr, AriaParserResult.class);
    } catch (Exception e) {
      throw new CatalogResourceException("Call aria parser api failed.", e);
    }

  }
}
