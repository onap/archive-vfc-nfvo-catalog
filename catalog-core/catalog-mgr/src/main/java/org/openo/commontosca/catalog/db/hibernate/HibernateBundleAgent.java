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

package org.openo.commontosca.catalog.db.hibernate;

import io.dropwizard.ConfiguredBundle;
import io.dropwizard.setup.Bootstrap;
import io.dropwizard.setup.Environment;

import org.openo.commontosca.catalog.CatalogAppConfiguration;
import org.openo.commontosca.catalog.db.dao.DaoManager;
import org.openo.commontosca.catalog.db.entity.NodeTemplateData;
import org.openo.commontosca.catalog.db.entity.PackageData;
import org.openo.commontosca.catalog.db.entity.ServiceTemplateData;
import org.openo.commontosca.catalog.db.entity.ServiceTemplateMappingData;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class HibernateBundleAgent implements ConfiguredBundle<CatalogAppConfiguration> {

  private final HibernateBundleExt bundle = new HibernateBundleExt(ServiceTemplateData.class,
      PackageData.class, NodeTemplateData.class, ServiceTemplateMappingData.class);
  private static final Logger LOGGER = LoggerFactory.getLogger(HibernateBundleAgent.class);

  @Override
  public void run(final CatalogAppConfiguration configuration, final Environment environment)
      throws Exception {
    Thread thread = new Thread(new Runnable() {
      int retry = 0;
      boolean flag = true;

      public void run() {
        while (retry < 1000) {
          LOGGER.info("init hibernateBundle.retry:" + retry);
          retry++;
          try {
            bundle.runExt(configuration, environment);
          } catch (Exception e1) {
            flag = false;
            LOGGER.warn(
                "init hibernateBundle failed, sleep 15S and try again.errorMsg:" + e1.getMessage());
            threadSleep(15000);
          }
          if (flag) {
            LOGGER.info("init hibernateBundle success!");
            initDao();
            break;
          }
        }
      }
    });
    thread.setName("init hibernateBundle");
    thread.start();
  }

  private void initDao() {
    DaoManager.getInstance().setSessionFactory(bundle.getSessionFactory());
  }

  private void threadSleep(int second) {
    LOGGER.info("start sleep ....");
    try {
      Thread.sleep(second);
    } catch (InterruptedException error) {
      LOGGER.error("thread sleep error.errorMsg:" + error.getMessage());
    }
    LOGGER.info("sleep end .");
  }

  @Override
  public void initialize(Bootstrap<?> bootstrap) {
    bundle.initializeExt(bootstrap);
  }
  //
  // public SessionFactory getSessionFactory() {
  // return bundle.getSessionFactory();
  // }
}
