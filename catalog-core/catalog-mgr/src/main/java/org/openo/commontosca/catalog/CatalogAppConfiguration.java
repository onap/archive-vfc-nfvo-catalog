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

package org.openo.commontosca.catalog;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.dropwizard.Configuration;
import io.dropwizard.db.DataSourceFactory;
import org.hibernate.validator.constraints.NotEmpty;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;




public class CatalogAppConfiguration extends Configuration {
  @NotEmpty
  private String template;

  @NotEmpty
  private String defaultName = "OPENO-Catalog";

  @NotEmpty
  private String msbServerAddr;

  @NotEmpty
  private String httpServerAddr;

  @NotEmpty
  private String opentoscaServerAddr;

  @NotEmpty
  private String yamlParseAddr;

  @NotEmpty
  private String wso2HostIp;

  @NotEmpty
  private String wso2HostPort;

  @NotEmpty
  private String cataloguePath;
  @NotEmpty
  private String httpServerPath;
  @NotEmpty
  private String ldapServerIp;

  @NotEmpty
  private String ldapServerPort;

  @NotEmpty
  private String ldapLogindn;

  @NotEmpty
  private String ldapPassword;

  @NotEmpty
  private String ldapVersion;
  @Valid
  @NotNull
  private DataSourceFactory database = new DataSourceFactory();

  @JsonProperty("database")
  public DataSourceFactory getDataSourceFactory() {
    return database;
  }

  @JsonProperty("database")
  public void setDataSourceFactory(DataSourceFactory dataSourceFactory) {
    this.database = dataSourceFactory;
  }

  @JsonProperty
  public String getTemplate() {
    return template;
  }

  @JsonProperty
  public void setTemplate(String template) {
    this.template = template;
  }

  @JsonProperty
  public String getDefaultName() {
    return defaultName;
  }

  @JsonProperty
  public void setDefaultName(String name) {
    this.defaultName = name;
  }

  @JsonProperty
  public String getMsbServerAddr() {
    return msbServerAddr;
  }

  @JsonProperty
  public void setMsbServerAddr(String msbServerAddr) {
    this.msbServerAddr = msbServerAddr;
  }

  @JsonProperty
  public String getHttpServerAddr() {
    return httpServerAddr;
  }

  @JsonProperty
  public void setHttpServerAddr(String httpServerAddr) {
    this.httpServerAddr = httpServerAddr;
  }

  @JsonProperty
  public String getOpentoscaServerAddr() {
    return opentoscaServerAddr;
  }

  @JsonProperty
  public void setOpentoscaServerAddr(String opentoscaServerAddr) {
    this.opentoscaServerAddr = opentoscaServerAddr;
  }

  @JsonProperty
  public String getYamlParseAddr() {
    return yamlParseAddr;
  }

  @JsonProperty
  public void setYamlParseAddr(String yamlParseAddr) {
    this.yamlParseAddr = yamlParseAddr;
  }

  @JsonProperty
  public String getWso2HostIp() {
    return wso2HostIp;
  }

  @JsonProperty
  public void setWso2HostIp(String wso2HostIp) {
    this.wso2HostIp = wso2HostIp;
  }

  @JsonProperty
  public String getWso2HostPort() {
    return wso2HostPort;
  }

  @JsonProperty
  public void setWso2HostPort(String wso2HostPort) {
    this.wso2HostPort = wso2HostPort;
  }

  public String getWso2BaseUrl() {
    return "http://" + this.wso2HostIp + ":" + this.wso2HostPort;
  }

  @JsonProperty
  public String getCataloguePath() {
    return cataloguePath;
  }

  @JsonProperty
  public void setCataloguePath(String cataloguePath) {
    this.cataloguePath = cataloguePath;
  }

  @JsonProperty
  public String getLdapServerIp() {
    return ldapServerIp;
  }

  @JsonProperty
  public void setLdapServerIp(String ldapServerIp) {
    this.ldapServerIp = ldapServerIp;
  }

  @JsonProperty
  public String getLdapServerPort() {
    return ldapServerPort;
  }

  @JsonProperty
  public void setLdapServerPort(String ldapServerPort) {
    this.ldapServerPort = ldapServerPort;
  }

  @JsonProperty
  public String getLdapLogindn() {
    return ldapLogindn;
  }

  @JsonProperty
  public void setLdapLogindn(String ldapLogindn) {
    this.ldapLogindn = ldapLogindn;
  }

  @JsonProperty
  public String getLdapPassword() {
    return ldapPassword;
  }

  @JsonProperty
  public void setLdapPassword(String ldapPassword) {
    this.ldapPassword = ldapPassword;
  }

  @JsonProperty
  public String getLdapVersion() {
    return ldapVersion;
  }

  @JsonProperty
  public void setLdapVersion(String ldapVersion) {
    this.ldapVersion = ldapVersion;
  }

  @JsonProperty
  public String getHttpServerPath() {
    return httpServerPath;
  }

  @JsonProperty
  public void setHttpServerPath(String httpServerPath) {
    this.httpServerPath = httpServerPath;
  }

}
