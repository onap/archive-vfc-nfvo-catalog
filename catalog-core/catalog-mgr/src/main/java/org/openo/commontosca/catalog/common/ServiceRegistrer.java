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
package org.openo.commontosca.catalog.common;

import org.openo.commontosca.catalog.externalservice.msb.MicroserviceBusConsumer;
import org.openo.commontosca.catalog.externalservice.msb.ServiceRegisterEntity;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.Iterator;

public class ServiceRegistrer implements Runnable {
  private final ArrayList<ServiceRegisterEntity> serviceEntityList =
      new ArrayList<ServiceRegisterEntity>();
  private static final Logger LOG = LoggerFactory.getLogger(ServiceRegistrer.class);

  public ServiceRegistrer() {
    initServiceEntity();
  }

  @Override
  public void run() {
    LOG.info("start  microservice register");
    boolean flag = false;
    ServiceRegisterEntity entity = new ServiceRegisterEntity();
    int retry = 0;
    while (retry < 1000 && serviceEntityList.size() > 0) {
      Iterator<ServiceRegisterEntity> it = serviceEntityList.iterator();
      while (it.hasNext()) {
        entity = it.next();
        LOG.info("start" + entity.getServiceName() + " catalog microservice register.retry:"
            + retry);
        flag = MicroserviceBusConsumer.registerService(entity);
        if (flag == false) {
          LOG.warn(entity.getServiceName()
              + " microservice register failed, sleep 30S and try again.");
          threadSleep(30000);
        } else {
          LOG.info(entity.getServiceName() + " microservice register success!");
          it.remove();
        }
      }
      retry++;

    }
    LOG.info("catalog microservice register end.");

  }

  /**
   * sleep thread.
   * @param second sleep second
   */
  private void threadSleep(int seconds) {
    LOG.info("start sleep ....");
    try {
      Thread.sleep(seconds);
    } catch (InterruptedException e1) {
      LOG.error("thread sleep error.errorMsg:" + e1.getMessage());
    }
    LOG.info("sleep end .");
  }

  private void initServiceEntity() {
    ServiceRegisterEntity catalogEntity = new ServiceRegisterEntity();
    catalogEntity.setServiceName("catalog");
    catalogEntity.setProtocol("REST");
    catalogEntity.setVersion("v1");
    catalogEntity.setUrl("/openoapi/catalog/v1");
    catalogEntity.setSingleNode(null, "8200", 0);
    catalogEntity.setVisualRange("1");
    serviceEntityList.add(catalogEntity);
    ServiceRegisterEntity httpServiceEntity = new ServiceRegisterEntity();
    httpServiceEntity.setServiceName("/files/catalog-http");
    httpServiceEntity.setProtocol("REST");
    httpServiceEntity.setVersion("v1");
    httpServiceEntity.setUrl("/");
    httpServiceEntity.setSingleNode(null, "8201", 0);
    httpServiceEntity.setVisualRange("1");
    serviceEntityList.add(httpServiceEntity);
  }
}
