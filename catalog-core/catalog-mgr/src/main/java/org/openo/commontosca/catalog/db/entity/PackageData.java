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

package org.openo.commontosca.catalog.db.entity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "catalog_package_table")
@JsonIgnoreProperties(ignoreUnknown = true)
public class PackageData extends BaseData {

  @Id
  @Column(name = "CSARID")
  private String csarId;
  @Column(name = "DOWNLOADURi")
  private String downloadUri;

  @Column(name = "NAME")
  private String name;

  @Column(name = "SIZE")
  private String size;
  @Column(name = "VERSION")
  private String version;

  @Column(name = "PROVIDER")
  private String provider;
  @Column(name = "TYPE")
  private String type;
  @Column(name = "FORMAT")
  private String format;

  @Column(name = "DELETIONPENDING")
  private String deletionPending;

  @Column(name = "MODIFYTIME")
  private String modifyTime;
  @Column(name = "OPERATIONALSTATE")
  private String operationalState;
  @Column(name = "USAGESTATE")
  private String usageState;
  @Column(name = "CREATETIME")
  private String createTime;
  @Column(name = "ONBOARDSTATE")
  private String onBoardState;
  @Column(name = "PROCESSSTATE")
  private String processState;

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getOnBoardState() {
    return onBoardState;
  }

  public void setOnBoardState(String onBoardState) {
    this.onBoardState = onBoardState;
  }

  public String getVersion() {
    return version;
  }

  public void setVersion(String version) {
    this.version = version;
  }

  public String getProvider() {
    return provider;
  }

  public void setProvider(String provider) {
    this.provider = provider;
  }

  public String getType() {
    return type;
  }

  public void setType(String type) {
    this.type = type;
  }

  public String getDownloadUri() {
    return downloadUri;
  }

  public void setDownloadUri(String downloadUri) {
    this.downloadUri = downloadUri;
  }

  public String getSize() {
    return size;
  }

  public void setSize(String size) {
    this.size = size;
  }

  public String getFormat() {
    return format;
  }

  public void setFormat(String format) {
    this.format = format;
  }

  public String getDeletionPending() {
    return deletionPending;
  }

  public void setDeletionPending(String deletionPending) {
    this.deletionPending = deletionPending;
  }

  public String getModifyTime() {
    return modifyTime;
  }

  public void setModifyTime(String modifyTime) {
    this.modifyTime = modifyTime;
  }

  public String getOperationalState() {
    return operationalState;
  }

  public void setOperationalState(String operationalState) {
    this.operationalState = operationalState;
  }

  public String getUsageState() {
    return usageState;
  }

  public void setUsageState(String usageState) {
    this.usageState = usageState;
  }

  public String getCreateTime() {
    return createTime;
  }

  public void setCreateTime(String createTime) {
    this.createTime = createTime;
  }

  public void setCsarId(String csarId) {
    this.csarId = csarId;
  }

  public String getCsarId() {
    return csarId;
  }

  public String getProcessState() {
    return processState;
  }

  public void setProcessState(String processState) {
    this.processState = processState;
  }

}
