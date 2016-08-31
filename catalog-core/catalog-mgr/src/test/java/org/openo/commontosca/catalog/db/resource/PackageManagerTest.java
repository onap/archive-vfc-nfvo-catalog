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

import static org.junit.Assert.assertTrue;


import org.junit.After;
import org.junit.AfterClass;
import org.junit.Assert;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openo.commontosca.catalog.db.common.Parameters;
import org.openo.commontosca.catalog.db.dao.DaoManager;
import org.openo.commontosca.catalog.db.entity.PackageData;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.util.H2DbServer;
import org.openo.commontosca.catalog.db.util.HibernateSession;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;


public class PackageManagerTest {
  private static PackageManager manager;

  /**
   * startup db session before class.
   * @throws Exception e
   */
  @BeforeClass
  public static void setUpBeforeClass() throws Exception {
    H2DbServer.startUp();
    DaoManager.getInstance().setSessionFactory(HibernateSession.init());
    manager = PackageManager.getInstance();
  }

  /**
   * destory db session after class.
   * @throws Exception e
   */
  @AfterClass
  public static void tearDownAfterClass() throws Exception {
    try {
      HibernateSession.destory();
      DaoManager.getInstance().setPackageDao(null);
      H2DbServer.shutDown();
    } catch (Exception e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
  }

  /**
   * create data before test.
   */
  @Before
  public void setUp() {
    PackageData data = new PackageData();
    data.setCsarId("10001");
    data.setName("AG");
    data.setVersion("v1.0");
    data.setProvider("ZTE");
    try {
      manager.addPackage(data);
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
  }

  /**
   * delete data after test.
   */
  @After
  public void tearDown() {
    try {
      manager.deletePackage("10001");
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
  }

  @Test
  public void testAddPackageRepeat() {
    PackageData data = new PackageData();
    data.setCsarId("10001");
    data.setName("AG");
    data.setVersion("v1.0");
    data.setProvider("ZTE");
    try {
      manager.addPackage(data);
      Assert.fail("no exception");
    } catch (CatalogResourceException e1) {
      Assert.assertTrue(true);
    }

  }

  @Test
  public void testQueryPackageByCsarId_exist() {
    ArrayList<PackageData> list = new ArrayList<PackageData>();
    try {
      list = manager.queryPackageByCsarId("10001");
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
    Assert.assertTrue(list.size() > 0);
  }

  @Test
  public void testQueryPackageByCsarId_not_exist() {
    ArrayList<PackageData> list = new ArrayList<PackageData>();
    try {
      list = manager.queryPackageByCsarId("10002");
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
    Assert.assertTrue(list.size() == 0);
  }

  @Test
  public void testQueryPackage_exist() {

    ArrayList<PackageData> list = new ArrayList<PackageData>();
    try {
      list = manager.queryPackage("AG", "ZTE", "v1.0", null, null);
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
    Assert.assertTrue(list.size() > 0);

  }

  @Test
  public void testQueryPackage_not_exist() {

    ArrayList<PackageData> list = new ArrayList<PackageData>();
    try {
      list = manager.queryPackage("AG", "ZTE", "v2.0", null, null);
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
    Assert.assertTrue(list.size() == 0);

  }

  @Test
  public void testUpdatePackage() {
    PackageData data = new PackageData();
    data.setSize("20M");
    try {
      manager.updatePackage(data, "10001");
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
    Map<String, String> queryParam = new HashMap<String, String>();
    queryParam.put(Parameters.csarId.name(), "10001");
    ArrayList<PackageData> list = new ArrayList<PackageData>();
    try {
      list = manager.queryPackageByCsarId("10001");
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
    assertTrue(list.size() > 0 && list.get(0).getSize().equals("20M"));
  }

}
