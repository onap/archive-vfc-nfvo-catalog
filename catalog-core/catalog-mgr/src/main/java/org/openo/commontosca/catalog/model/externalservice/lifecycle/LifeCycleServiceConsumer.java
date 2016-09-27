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
package org.openo.commontosca.catalog.model.externalservice.lifecycle;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import com.eclipsesource.jaxrs.consumer.ConsumerFactory;
import org.openo.commontosca.catalog.common.MsbUtil;
import org.openo.commontosca.catalog.common.ToolUtil;
import org.openo.commontosca.catalog.model.externalservice.entity.lifecycle.InstanceEntity;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.lang.reflect.Type;
import java.util.ArrayList;



/**
 * The lifecycle service.
 * 
 * @author 10189609
 * 
 */
public class LifeCycleServiceConsumer {
  private static final Logger LOG = LoggerFactory.getLogger(LifeCycleServiceConsumer.class);

  /**
   * get lifecycle application instances.
   * 
   * @return instance entity
   */
  public static ArrayList<InstanceEntity> getInstances() {
    ILifeCycleServiceRest resourceserviceproxy =
        ConsumerFactory.createConsumer(MsbUtil.getNsocLifecycleBaseUrl(),
            ILifeCycleServiceRest.class);
    String result = "";
    try {
      result = resourceserviceproxy.getVnfInstances();
    } catch (Exception e1) {
      LOG.error("query vim info faild.", e1);
      return null;
    }
    if (ToolUtil.isEmptyString(result)) {
      return null;
    }

    Gson gson = new Gson();
    Type listType = new TypeToken<ArrayList<InstanceEntity>>() {}.getType();
    return gson.fromJson(result, listType);
  }
}
