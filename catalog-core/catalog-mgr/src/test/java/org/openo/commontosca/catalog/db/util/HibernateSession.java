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
package org.openo.commontosca.catalog.db.util;

import org.hibernate.SessionFactory;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.hibernate.cfg.Configuration;
import org.hibernate.service.ServiceRegistry;

import java.io.File;
import java.net.URISyntaxException;

public class HibernateSession {
  private static File cfgfile = null;

  private static ServiceRegistry serviceRegistry = null;
  private static Configuration configuration = null;
  private static SessionFactory sessionFactory = null;
  private static String resourcePath;

  /**
   * Get a hibernate sessionFactory.
   */
  public static SessionFactory init() {
    initConfigure();
    configuration = new Configuration().configure(cfgfile);
    configuration.setProperty("hibernate.connection.url", "jdbc:h2:tcp://localhost:8205/"
        + resourcePath + "db/catalog");
    serviceRegistry =
        new StandardServiceRegistryBuilder().applySettings(configuration.getProperties()).build();
    sessionFactory = configuration.buildSessionFactory(serviceRegistry);
    return sessionFactory;
  }

  private static void initConfigure() {
    try {
      resourcePath = HibernateSession.class.getResource("/").toURI().getPath();
    } catch (URISyntaxException e1) {
      e1.printStackTrace();
    }
    final String filename = "Hibernate.cfg.xml";
    cfgfile = new File(resourcePath + filename);
  }

  /**
   * Destory a hibernate sessionFactory.
   */
  public static void destory() {
    sessionFactory.close();
  }

  /* Maybe you don't need it. */
  private static void removeCfgFile() {
    if (cfgfile.exists()) {
      cfgfile.deleteOnExit();
    }
  }

  /**
   * test.
   * @param args param
   */
  public static void main(String[] args) {
    // createCfgFile();
    // removeCfgFile();


  }
}
