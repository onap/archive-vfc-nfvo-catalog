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
package org.openo.commontosca.catalog.model.externalservice.ro;

import com.google.gson.Gson;

import com.eclipsesource.jaxrs.consumer.ConsumerFactory;

import org.openo.commontosca.catalog.common.MsbUtil;
import org.openo.commontosca.catalog.common.ToolUtil;
import org.openo.commontosca.catalog.model.externalservice.entity.ro.ResourceResponseEntity;
import org.openo.commontosca.catalog.model.externalservice.entity.ro.VimEntity;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


/**
 * The roc resource service.
 * 
 * @author 10189609
 * 
 */
public class ResourceServiceConsumer {
  private static final Logger LOG = LoggerFactory.getLogger(ResourceServiceConsumer.class);

  private static final String RESOURCE_REST_RESULT = "SUCCESS";

  /**
   * get vim entity from roc by vimid.
   * 
   * @param vimId id
   * @return vim entity
   */
  public static VimEntity getResourceVim(String vimId) {
    LOG.info("begin query vim info from roc,vimId:" + vimId);
    IResourceServiceRest resourceserviceproxy =
        ConsumerFactory.createConsumer(MsbUtil.getRocBaseUrl(), IResourceServiceRest.class);
    String result = "";
    try {
      result = resourceserviceproxy.getResourceVim(vimId);
    } catch (Exception e1) {
      LOG.error("query vim info faild.", e1);
      return null;
    }
    if (ToolUtil.isEmptyString(result)) {
      LOG.error("query vim info faild, vim info is null, vimId:" + vimId);
      return null;
    }

    Gson gson = new Gson();
    ResourceResponseEntity responseEntity = gson.fromJson(result, ResourceResponseEntity.class);
    if (!RESOURCE_REST_RESULT.equalsIgnoreCase(responseEntity.getOperationResult())) {
      LOG.error("query vim info faild.vimId:" + vimId);
      return null;
    }
    if (responseEntity.getData().size() <= 0) {
      LOG.error("query vim info faild, vim info is empty, vimId:" + vimId);
      return null;
    }

    LOG.info("end query vim info from roc.");
    return responseEntity.getData().get(0);
  }
}
