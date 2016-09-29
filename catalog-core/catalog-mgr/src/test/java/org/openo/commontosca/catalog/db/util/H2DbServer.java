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

import org.h2.tools.Server;

import java.sql.SQLException;


public class H2DbServer {

  private static Server h2DbWebServer;
  private static Server h2DbTcpServer;

  /**
   * start up db service.
   */
  public static void startUp() {
    try {
      h2DbWebServer =
          Server.createWebServer(new String[] {"-web", "-webAllowOthers", "-webPort", "8206"});
      h2DbWebServer.start();

      h2DbTcpServer =
          Server.createTcpServer(new String[] {"-tcp", "-tcpAllowOthers", "-tcpPort", "8205"});
      h2DbTcpServer.start();
    } catch (SQLException e1) {
      e1.printStackTrace();
    }
  }

  /**
   * shut down db service.
   */
  public static void shutDown() {
    if (h2DbWebServer.isRunning(true)) {
      h2DbWebServer.stop();
      h2DbWebServer.shutdown();
    }
    if (h2DbTcpServer.isRunning(true)) {
      h2DbTcpServer.stop();
      h2DbTcpServer.shutdown();
    }
  }
}
