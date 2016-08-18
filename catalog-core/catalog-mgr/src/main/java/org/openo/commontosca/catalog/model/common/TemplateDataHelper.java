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
package org.openo.commontosca.catalog.model.common;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import org.openo.commontosca.catalog.db.entity.ServiceTemplateMappingData;
import org.openo.commontosca.catalog.db.entity.TemplateData;
import org.openo.commontosca.catalog.model.entity.ServiceTemplate;
import org.openo.commontosca.catalog.model.entity.ServiceTemplateOperation;
import org.openo.commontosca.catalog.model.entity.SubstitutionMapping;
import org.openo.commontosca.catalog.common.ToolUtil;
import org.openo.commontosca.catalog.db.entity.NodeTemplateData;
import org.openo.commontosca.catalog.db.entity.ServiceTemplateData;
import org.openo.commontosca.catalog.model.entity.InputParameter;
import org.openo.commontosca.catalog.model.entity.NodeTemplate;
import org.openo.commontosca.catalog.model.entity.RelationShip;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonPrimitive;

/**
 * @author 10090474
 *
 */
public class TemplateDataHelper {

    /**
     * @param st
     * @param ntList
     * @return
     */
    public static TemplateData convert2TemplateData(ServiceTemplate st,
                                                    String rawData, List<NodeTemplate> ntList) {
        TemplateData td = new TemplateData();
        td.setServiceTemplate(convert2ServiceTemplateData(st, rawData));
        td.setNodeTemplates(convert2NodeTemplateDataList(ntList,
                st.getServiceTemplateId()));
        return td;
    }

    /**
     * @param st
     * @return
     */
    private static ServiceTemplateData convert2ServiceTemplateData(
            ServiceTemplate st, String rawData) {
        ServiceTemplateData std = new ServiceTemplateData();
        std.setServiceTemplateId(st.getServiceTemplateId());
        std.setTemplateName(st.getTemplateName());
        std.setVendor(st.getVendor());
        std.setVersion(st.getVersion());
        std.setCsarId(st.getCsarid());
        std.setType(st.getType());
        std.setDownloadUri(st.getDownloadUri());
        std.setInputs(ToolUtil.toJson(st.getInputs()));
        std.setOperations(ToolUtil.toJson(st.getOperations()));
        std.setRowData(rawData);
        return std;
    }

    /**
     * @param ntList
     * @param serviceTemplateId
     * @return
     */
    private static ArrayList<NodeTemplateData> convert2NodeTemplateDataList(
            List<NodeTemplate> ntList, String serviceTemplateId) {
        ArrayList<NodeTemplateData> ntdList = new ArrayList<>();
        for (NodeTemplate nt : ntList) {
            ntdList.add(convert2NodeTemplateData(nt, serviceTemplateId));

        }
        return ntdList;
    }


    /**
     * @param nt
     * @param serviceTemplateId
     * @return
     */
    private static NodeTemplateData convert2NodeTemplateData(NodeTemplate nt,
            String serviceTemplateId) {
        NodeTemplateData ntd = new NodeTemplateData();

        ntd.setNodeTemplateId(nt.getId());
        ntd.setName(nt.getName());
        ntd.setType(nt.getType());
        ntd.setServiceTemplateId(serviceTemplateId);
        ntd.setProperties(ToolUtil.toJson(nt.getProperties()));
        ntd.setRelationShips(ToolUtil.toJson(nt.getRelationShips()));

        return ntd;
    }


    /**
     * @param stdList
     * @return
     */
    public static ServiceTemplate[] convert2ServiceTemplates(
            List<ServiceTemplateData> stdList) {
        List<ServiceTemplate> stList = new ArrayList<>();
        for (ServiceTemplateData std : stdList) {
            stList.add(convert2ServiceTemplate(std));
        }

        return stList.toArray(new ServiceTemplate[0]);
    }

    /**
     * @param std
     * @return
     */
    public static ServiceTemplate convert2ServiceTemplate(
            ServiceTemplateData std) {
        InputParameter[] inputs = ToolUtil.fromJson(std.getInputs(),
                InputParameter[].class);
        ServiceTemplateOperation[] operations = ToolUtil.fromJson(
                std.getOperations(), ServiceTemplateOperation[].class);

        return new ServiceTemplate(std.getServiceTemplateId(),
                std.getTemplateName(), std.getVendor(), std.getVersion(),
                std.getCsarId(), std.getType(), std.getDownloadUri(), inputs,
                operations);
    }

    /**
     * 
     * @param ntdList
     * @return
     */
    public static NodeTemplate[] convert2NodeTemplates(
            List<NodeTemplateData> ntdList) {
        List<NodeTemplate> ntList = new ArrayList<>();
        for (NodeTemplateData ntd : ntdList) {
            ntList.add(convert2NodeTemplate(ntd));
        }
        return ntList.toArray(new NodeTemplate[0]);
    }

    /**
     * @param ntd
     * @return
     */
    public static NodeTemplate convert2NodeTemplate(NodeTemplateData ntd) {
        List<RelationShip> relationShips = convert2RelationShipList(ntd
                .getRelationShips());
        return new NodeTemplate(ntd.getNodeTemplateId(), ntd.getName(),
                ntd.getType(), convert2Property(ntd.getProperties()),
                relationShips);
    }

    /**
     * @param sRelationShips
     * @return
     */
    private static List<RelationShip> convert2RelationShipList(
            String sRelationShips) {
        RelationShip[] relationShips = ToolUtil.fromJson(sRelationShips,
                RelationShip[].class);
        return Arrays.asList(relationShips);
    }

    /**
     * @param properties
     * @return
     */
    private static Map<String, Object> convert2Property(String properties) {
        JsonObject jsonObject = new Gson().fromJson(properties,
                JsonObject.class);
        return parseMapValue(jsonObject);
    }

    private static Map<String, Object> parseMapValue(JsonObject jsonObject) {
        Map<String, Object> map = new HashMap<>();

        Iterator<Entry<String, JsonElement>> iterator = jsonObject.entrySet()
                .iterator();
        while (iterator.hasNext()) {
            Entry<String, JsonElement> next = iterator.next();
            if (next.getValue() instanceof JsonPrimitive) {
                map.put(next.getKey(), next.getValue().getAsString());
                continue;
            }

            if (next.getValue() instanceof JsonObject) {
                map.put(next.getKey(),
                        parseMapValue((JsonObject) next.getValue()));
                continue;
            }
        }
        return map;
    }


    /**
     * @param stm
     * @return
     */
    public static ServiceTemplateMappingData convert2TemplateMappingData(
            SubstitutionMapping stm) {
        ServiceTemplateMappingData stmd = new ServiceTemplateMappingData();

        stmd.setMappingId(ToolUtil.generateId());
        stmd.setServiceTemplateId(stm.getServiceTemplateId());
        stmd.setNodeType(stm.getNode_type());
        stmd.setRequirements(ToolUtil.toJson(stm.getRequirements()));
        stmd.setCapabilities(ToolUtil.toJson(stm.getCapabilities()));

        return stmd;
    }

    /**
     * @param stmData
     * @return
     */
    public static SubstitutionMapping convert2SubstitutionMapping(
            ServiceTemplateMappingData stmData) {
        return new SubstitutionMapping(stmData.getServiceTemplateId(),
                stmData.getNodeType());
    }

}
