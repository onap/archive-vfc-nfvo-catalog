/**
 *     Copyright (C) 2016 ZTE, Inc. and others. All rights reserved. (ZTE)
 *
 *     Licensed under the Apache License, Version 2.0 (the "License");
 *     you may not use this file except in compliance with the License.
 *     You may obtain a copy of the License at
 *
 *             http://www.apache.org/licenses/LICENSE-2.0
 *
 *     Unless required by applicable law or agreed to in writing, software
 *     distributed under the License is distributed on an "AS IS" BASIS,
 *     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *     See the License for the specific language governing permissions and
 *     limitations under the License.
 */
package org.openo.orchestrator.nfv.catalog.model.parser.yaml;

import org.glassfish.jersey.client.ClientConfig;
import org.openo.orchestrator.nfv.catalog.common.MSBUtil;
import org.openo.orchestrator.nfv.catalog.db.exception.CatalogResourceException;
import org.openo.orchestrator.nfv.catalog.model.parser.yaml.entity.ParseYamlRequestParemeter;
import org.openo.orchestrator.nfv.catalog.model.parser.yaml.entity.ParseYamlResult;

import com.eclipsesource.jaxrs.consumer.ConsumerFactory;
import com.google.gson.Gson;

/**
 * 
 * @author 10090474
 * 
 */
public class YamlParseServiceConsumer {
    /**
     * get service template by template id from container service.
     * 
     * @param request
     * @return
     * @throws CatalogResourceException
     */
    public static ParseYamlResult getServiceTemplates(
            final ParseYamlRequestParemeter request)
            throws CatalogResourceException {
        try {
            ClientConfig config = new ClientConfig();
            IYamlParseRest yamlParseProxy = ConsumerFactory
                    .createConsumer(MSBUtil.getYamlParseBaseUrl(), config,
                            IYamlParseRest.class);
            String jsonStr = yamlParseProxy.parse(request);
            return new Gson().fromJson(jsonStr, ParseYamlResult.class);
        } catch (Exception e) {
            throw new CatalogResourceException("Call parser api failed.", e);
        }

    }
}
