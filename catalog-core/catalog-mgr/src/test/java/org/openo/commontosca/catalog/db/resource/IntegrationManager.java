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

package org.openo.commontosca.catalog.db.resource;


import org.junit.After;
import org.junit.AfterClass;
import org.junit.Assert;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openo.commontosca.catalog.db.dao.DaoManager;
import org.openo.commontosca.catalog.db.entity.NodeTemplateData;
import org.openo.commontosca.catalog.db.entity.PackageData;
import org.openo.commontosca.catalog.db.entity.ServiceTemplateData;
import org.openo.commontosca.catalog.db.entity.TemplateData;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.util.H2DbServer;
import org.openo.commontosca.catalog.db.util.HibernateSession;

import java.util.ArrayList;

public class IntegrationManager {
  private static PackageManager packageManager;
  private static TemplateManager templateManager;

  /**
   * startup H2DB session before class.
   * @throws Exception e
   */
  @BeforeClass
  public static void setUpBeforeClass() throws Exception {
    H2DbServer.startUp();
    DaoManager.getInstance().setSessionFactory(HibernateSession.init());
    packageManager = PackageManager.getInstance();
    templateManager = TemplateManager.getInstance();
  }

  /**
   * destory H2DB session after class.
   * @throws Exception e
   */
  @AfterClass
  public static void tearDownAfterClass() throws Exception {
    try {
      HibernateSession.destory();
      DaoManager.getInstance().setDaoNull();
      H2DbServer.shutDown();
    } catch (Exception e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
  }

  @Before
  public void setUp() {
    initPackageInfo();
    initTemplateInfo();
  }

  /**
   * init package information.
   */
  public void initPackageInfo() {
    PackageData data = new PackageData();
    data.setCsarId("10001");
    data.setName("AG");
    data.setVersion("v1.0");
    data.setProvider("ZTE");
    try {
      packageManager.addPackage(data);
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
  }

  /**
   * delete package information.
   */
  public void deletePackageInfo() {
    try {
      packageManager.deletePackage("10001");
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
  }

  /**
   * init template information.
   */
  public void initTemplateInfo() {
    ServiceTemplateData serviceData = new ServiceTemplateData();
    serviceData.setCsarId("10001");
    serviceData.setServiceTemplateId("20001");
    serviceData.setVendor("ZTE");
    serviceData.setVersion("v1.0");
    NodeTemplateData nodeData = new NodeTemplateData();
    nodeData.setName("node");
    nodeData.setNodeTemplateId("30001");
    nodeData.setServiceTemplateId("20001");
    ArrayList<NodeTemplateData> nodelist = new ArrayList<NodeTemplateData>();
    nodelist.add(nodeData);
    TemplateData data = new TemplateData();
    data.setServiceTemplate(serviceData);
    data.setNodeTemplates(nodelist);
    try {
      templateManager.addServiceTemplate(data);
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
  }

  /**
   * delete template.
   */
  public void deleteTemplate() {
    try {
      templateManager.deleteServiceTemplateById("20001");
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
  }

  @After
  public void tearDown() {
    deleteTemplate();
    deletePackageInfo();
  }

  @Test
  public void testDeletePackageByServiceTemplateId() {
    try {
      packageManager.deletePackageByServiceTemplateId("20001");
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
    ArrayList<PackageData> list = new ArrayList<PackageData>();
    try {
      list = packageManager.queryPackageByServiceTemplateId("20001");
    } catch (CatalogResourceException e2) {
      Assert.fail("Exception" + e2.getMessage());
    }
    Assert.assertTrue(list.size() == 0);
  }

  @Test
  public void testQueryPackageByServiceTemplateId() {
    ArrayList<PackageData> list = new ArrayList<PackageData>();
    try {
      list = packageManager.queryPackageByServiceTemplateId("20001");
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
    Assert.assertTrue(list.size() > 0);
  }

  @Test
  public void testDeleteServiceTemplateByCsarPackageInfo() {
    PackageData data = new PackageData();
    data.setCsarId("10001");
    ArrayList<ServiceTemplateData> list = new ArrayList<ServiceTemplateData>();
    try {
      templateManager.deleteServiceTemplateByCsarPackageInfo(data);
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
    try {
      list = templateManager.queryServiceTemplateByCsarPackageInfo(data);
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
    Assert.assertTrue(list.size() == 0);
  }

  @Test
  public void testQueryServiceTemplateByCsarPackageInfo() {
    PackageData data = new PackageData();
    data.setCsarId("10001");
    ArrayList<ServiceTemplateData> list = new ArrayList<ServiceTemplateData>();
    try {
      list = templateManager.queryServiceTemplateByCsarPackageInfo(data);
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
    Assert.assertTrue(list.size() > 0);
  }
}
