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
package org.openo.commontosca.catalog.model.parser.yaml.zte.service;

import com.google.gson.Gson;
import com.eclipsesource.jaxrs.consumer.ConsumerFactory;

import org.glassfish.jersey.client.ClientConfig;
import org.openo.commontosca.catalog.common.MsbUtil;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.model.parser.yaml.zte.entity.ParseYamlRequestParemeter;
import org.openo.commontosca.catalog.model.parser.yaml.zte.entity.ParseYamlResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class YamlParseServiceConsumer {
  private static final Logger logger = LoggerFactory.getLogger(YamlParseServiceConsumer.class);
  /**
   * get service template by template id from container service.
   * 
   * @param request parse yaml request
   * @return parase yaml result
   * @throws CatalogResourceException e
   */
  public static ParseYamlResult getServiceTemplates(ParseYamlRequestParemeter request)
      throws CatalogResourceException {
    logger.info("parseCsarPackage uri = " + request.getPath());

    try {
      ClientConfig config = new ClientConfig();
      IYamlParseRest yamlParseProxy =
          ConsumerFactory.createConsumer(MsbUtil.getYamlParseBaseUrl(), config,
              IYamlParseRest.class);
      String jsonStr = yamlParseProxy.parse(request);
      ParseYamlResult result = new Gson().fromJson(jsonStr, ParseYamlResult.class);
      result.setRawData(jsonStr);
      return result;
    } catch (Exception e1) {
      throw new CatalogResourceException("Call parser api failed.", e1);
    }

  }
}
