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
  private String parserType;

  @NotEmpty
  private String cataloguePath;
  @NotEmpty
  private String httpServerPath;

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
  
  public String getParserType() {
    return parserType;
  }

  public void setParserType(String parserType) {
    this.parserType = parserType;
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
  public String getHttpServerPath() {
    return httpServerPath;
  }

  @JsonProperty
  public void setHttpServerPath(String httpServerPath) {
    this.httpServerPath = httpServerPath;
  }

}
