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
package org.openo.commontosca.catalog.externalservice.msb;


import org.glassfish.jersey.client.ClientConfig;
import org.openo.commontosca.catalog.common.Config;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.eclipsesource.jaxrs.consumer.ConsumerFactory;

/**
 * @author 10159474
 *
 */
public class MicroserviceBusConsumer {
    private static final Logger LOG = LoggerFactory.getLogger(MicroserviceBusConsumer.class);

    public static boolean registerService(ServiceRegisterEntity entity) {
        ClientConfig config = new ClientConfig();
        try {
            MicroserviceBusRest resourceserviceproxy = ConsumerFactory.createConsumer(
                    Config.getConfigration().getMsbServerAddr(),config, MicroserviceBusRest.class);
            resourceserviceproxy.registerServce("false", entity);
        } catch (Exception e) {
            LOG.error("microservice register failed!" + e.getMessage());
            return false;
        }
        return true;
    }
}
