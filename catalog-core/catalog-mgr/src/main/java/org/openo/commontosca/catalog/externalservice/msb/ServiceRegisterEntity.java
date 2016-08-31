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

package org.openo.commontosca.catalog.externalservice.msb;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;


@Data
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class ServiceRegisterEntity {
  private String serviceName;
  private String version;
  private String url;
  private String protocol;
  private String visualRange;
  private ArrayList<ServiceNode> nodes = new ArrayList<ServiceNode>();

  /**
   * set single node.
   * @param ip ip
   * @param port port
   * @param ttl ttl
   */
  public void setSingleNode(String ip, String port, int ttl) {
    ServiceNode node = new ServiceNode();
    node.setIp(ip);
    node.setPort(port);
    node.setTtl(ttl);
    nodes.add(node);
  }

}
