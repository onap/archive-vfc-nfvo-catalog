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

package org.openo.commontosca.catalog.db.util;

import static org.junit.Assert.assertEquals;

import org.junit.Test;
import org.openo.commontosca.catalog.db.entity.PackageData;
import org.openo.commontosca.catalog.db.entity.ServiceTemplateData;

public class HqlFactoryTest {

  @Test
  public void when_input_entity_output_udatehql() {
    PackageData data = new PackageData();
    String filter = "csarId='xd03dsfsdfsfsdfsd'";
    data.setName("csarName");
    data.setType("NS");
    String expect =
        "update PackageData set name='csarName',type='NS' where csarId='xd03dsfsdfsfsdfsd'";
    String actual = HqlFactory.getUpdateHql(data, null, filter);
    assertEquals(expect, actual);
  }

  @Test
  public void when_input_null_testContain_output_false() {
    boolean expect = false;
    boolean actual = HqlFactory.contain(null, "name");
    assertEquals(expect, actual);
    String[] src = new String[0];
    actual = HqlFactory.contain(src, "name");
    assertEquals(expect, actual);
    src = new String[1];
    actual = HqlFactory.contain(src, null);
    assertEquals(expect, actual);
  }

  @Test
  public void when_input_src_contain_target_testContain_output_true() {
    boolean expect = true;
    String[] src = {"name", "type"};
    String target = "name";
    boolean actual = HqlFactory.contain(src, target);
    assertEquals(expect, actual);
  }

  @Test
  public void when_input_src_not_contain_target_testContain_output_false() {
    boolean expect = false;
    String[] src = {"name", "type"};
    String target = "version";
    boolean actual = HqlFactory.contain(src, target);
    assertEquals(expect, actual);
  }

  @Test
  public void testGetOidFilter() {
    // fail("Not yet implemented");
    String key = "csarId";
    String value = "xd03dsfsdfsfsdfsd";
    String expect = "csarId= 'xd03dsfsdfsfsdfsd'";
    String actual = HqlFactory.getOidFilter(key, value);
    assertEquals(expect, actual);
  }

  @Test
  public void when_input_entity_output_queryhql() {
    PackageData data = new PackageData();
    String filter = "csarId";
    data.setName("csarName");
    data.setType("NS");
    String expect = "select q.csarId from PackageData as q where q.name='csarName' and q.type='NS'";
    String actual = HqlFactory.getQueryHql(data, filter);
    assertEquals(expect, actual);
  }

  @Test
  public void when_input_entity_output_getQueryHqlByFilter() {
    PackageData data = new PackageData();
    String filter = "csarId";
    data.setName("csarName");
    data.setType("NS");
    String expect =
        " from ServiceTemplateData as a where a.csarId "
        + "in(select q.csarId from PackageData as q "
        + "where q.name='csarName' and q.type='NS')";
    String actual = HqlFactory.getQueryHqlByFilter(ServiceTemplateData.class, data, filter);
    assertEquals(expect, actual);
  }

  @Test
  public void when_input_entity_output_getDeleteHqlByFilter() {
    PackageData data = new PackageData();
    String filter = "csarId";
    data.setName("csarName");
    data.setType("NS");
    String expect =
        "delete from ServiceTemplateData as b where b.csarId "
        + "in(select q.csarId from PackageData as q "
        + "where q.name='csarName' and q.type='NS')";
    String actual = HqlFactory.getDeleteHqlByFilter(ServiceTemplateData.class, data, filter);
    assertEquals(expect, actual);
  }
}
