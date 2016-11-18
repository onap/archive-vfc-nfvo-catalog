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

import java.io.Serializable;

public class ApiRouteInfo implements Serializable {
  private static final long serialVersionUID = 1L;
  private String serviceName;
  private String version = "";
  private String url;
  private String apiJson = "";
  private String apiJsonType = "1";
  private String metricsUrl = "";
  private String control = "0";
  private String status = "1";

  private RouteServer []servers;


  public String getServiceName() {
    return serviceName;
  }

  public void setServiceName(String serviceName) {
    this.serviceName = serviceName;
  }

  public String getVersion() {
    return version;
  }

  public void setVersion(String version) {
    this.version = version;
  }

  public String getApiJson() {
    return apiJson;
  }

  public void setApiJson(String apiJson) {
    this.apiJson = apiJson;
  }

  public String getUrl() {
    return url;
  }

  public void setUrl(String url) {
    this.url = url;
  }

  public RouteServer[] getServers() {
    return servers;
  }

  public void setServers(RouteServer[] servers) {
    this.servers = servers;
  }

  public String getApiJsonType() {
    return apiJsonType;
  }

  public void setApiJsonType(String apiJsonType) {
    this.apiJsonType = apiJsonType;
  }

  public String getMetricsUrl() {
    return metricsUrl;
  }

  public void setMetricsUrl(String metricsUrl) {
    this.metricsUrl = metricsUrl;
  }

  public String getControl() {
    return control;
  }

  public void setControl(String control) {
    this.control = control;
  }

  public String getStatus() {
    return status;
  }

  public void setStatus(String status) {
    this.status = status;
  }
}
