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

import org.apache.tools.ant.Project;
import org.apache.tools.ant.taskdefs.SQLExec;
import org.apache.tools.ant.types.EnumeratedAttribute;

import java.io.File;
import java.net.URISyntaxException;

public class H2DbServerUtil {
  private static String resourcePath;

  /**
   * init data table.
   */
  public static void initTable() {
    init();
    SQLExec sqlExec = new SQLExec();
    // set db connetc parameter
    sqlExec.setDriver("org.h2.Driver");
    sqlExec.setUrl("jdbc:h2:tcp://localhost:8205/" + resourcePath + "db/catalog");
    sqlExec.setUserid("catalog");
    sqlExec.setPassword("catalog");
    // execute sql
    sqlExec.setSrc(new File(resourcePath + "sql/catalog-resource-createObj-mysql.sql"));
    sqlExec.setOnerror((SQLExec.OnError) (EnumeratedAttribute.getInstance(SQLExec.OnError.class,
        "abort")));
    sqlExec.setPrint(true); // set print
    sqlExec.setProject(new Project());
    sqlExec.execute();
  }

  private static void init() {
    try {
      resourcePath = HibernateSession.class.getResource("/").toURI().getPath();
    } catch (URISyntaxException e1) {
      e1.printStackTrace();
    }
  }

  /**
   * test.
   */
  public static void main() {
    H2DbServer.startUp();
    H2DbServerUtil.initTable();
    H2DbServer.shutDown();
  }
}
