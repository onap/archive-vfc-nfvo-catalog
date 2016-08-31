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

package org.openo.commontosca.catalog.db.resource.dao;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;


import org.junit.After;
import org.junit.AfterClass;
import org.junit.Assert;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openo.commontosca.catalog.db.common.Parameters;
import org.openo.commontosca.catalog.db.dao.PackageDao;
import org.openo.commontosca.catalog.db.entity.PackageData;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.util.H2DbServer;
import org.openo.commontosca.catalog.db.util.HibernateSession;
import org.openo.commontosca.catalog.db.util.HqlFactory;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class PackageDaoTest {

  private static PackageDao packageDao;

  /**
   * setup db session before class.
   * @throws Exception e
   */
  @BeforeClass
  public static void setUpBeforeClass() throws Exception {
    H2DbServer.startUp();
    packageDao = new PackageDao(HibernateSession.init());

  }

  /**
   * shutdown db session before class.
   * @throws Exception e
   */
  @AfterClass
  public static void tearDownAfterClass() throws Exception {
    try {
      HibernateSession.destory();
      H2DbServer.shutDown();
    } catch (Exception e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
  }

  /**
   * create data before test.
   * @throws Exception e
   */
  @Before
  public void setUp() {
    PackageData data = new PackageData();
    data.setCsarId("10001");
    data.setName("AG");
    try {
      packageDao.create(data);
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
  }

  /**
   * delete data after test.
   * @throws Exception e
   */
  @After
  public void tearDown() {
    PackageData data = new PackageData();
    data.setCsarId("10001");
    try {
      packageDao.delete(data);
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
  }

  @Test
  public void testQueryPackageById() {
    Map<String, String> queryParam = new HashMap<String, String>();
    queryParam.put(Parameters.csarId.name(), "10001");
    ArrayList<PackageData> list = new ArrayList<PackageData>();
    try {
      list = (ArrayList<PackageData>) packageDao.query(queryParam);
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
    Assert.assertTrue(list.size() > 0);
  }

  @Test
  public void testUpdatePackage() {
    PackageData data = new PackageData();
    data.setSize("20M");
    try {
      packageDao.update(data, HqlFactory.getOidFilter(Parameters.csarId.name(), "10001"));
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
    Map<String, String> queryParam = new HashMap<String, String>();
    queryParam.put(Parameters.csarId.name(), "10001");
    ArrayList<PackageData> list = new ArrayList<PackageData>();
    try {
      list = (ArrayList<PackageData>) packageDao.query(queryParam);
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
    assertTrue(list.size() > 0 && list.get(0).getSize().equals("20M"));
  }

  @Test
  public void testDeleteByOid() {
    PackageData data = new PackageData();
    data.setCsarId("10001");
    try {
      packageDao.delete(data);
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
    Map<String, String> queryParam = new HashMap<String, String>();
    queryParam.put(Parameters.csarId.name(), "10001");
    ArrayList<PackageData> list = new ArrayList<PackageData>();
    try {
      list = (ArrayList<PackageData>) packageDao.query(queryParam);
    } catch (CatalogResourceException e1) {
      Assert.fail("Exception" + e1.getMessage());
    }
    assertEquals(list.size(), 0);
  }

}
