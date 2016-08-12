/**
 *     Copyright (C) 2016 ZTE, Inc. and others. All rights reserved. (ZTE)
 *
 *     Licensed under the Apache License, Version 2.0 (the "License");
 *     you may not use this file except in compliance with the License.
 *     You may obtain a copy of the License at
 *
 *             http://www.apache.org/licenses/LICENSE-2.0
 *
 *     Unless required by applicable law or agreed to in writing, software
 *     distributed under the License is distributed on an "AS IS" BASIS,
 *     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *     See the License for the specific language governing permissions and
 *     limitations under the License.
 */
package org.openo.orchestrator.nfv.catalog.cometd;

import java.io.IOException;

import org.cometd.bayeux.server.BayeuxServer;
import org.cometd.bayeux.server.ConfigurableServerChannel;
import org.cometd.bayeux.server.LocalSession;
import org.cometd.bayeux.server.ServerChannel;

/**
 * @author 10189609
 * 
 */
public class CometdService {
    private BayeuxServer bayeux;
    private LocalSession session;

    /**
     * meta channel.
     */
    private static final String bayeuxChannel = "/meta/";

    /**
     * service channel.
     */
    private static final String serviceChannel = "/service/";

    private static CometdService cometdService = null;

    public static CometdService getInstance() {
        if (cometdService == null) {
            cometdService = new CometdService();
        }
        return cometdService;
    }

    public void publish(String channel, Object message) throws CometdException {
        if (bayeux == null) {
            this.bayeux = CometdUtil.getBayeuxServer();
            checkBayeuxServer();
            this.session = this.bayeux.newLocalSession("openo_catalogue_local_session");
            this.session.handshake();
        }
        String jsonMsg;
        try {
            jsonMsg = CometdUtil.convertBean2Json(message);
        } catch (IOException e) {
            throw new CometdException(e);
        }

        checkAndInit(channel);
        ServerChannel serverChannel = this.bayeux.getChannel(channel);
        serverChannel.publish(this.session, jsonMsg);
    }

    private void checkBayeuxServer() throws CometdException {
        if (this.bayeux == null) {
            throw new CometdException(CometdException.ERROR_CODE_BAYEUX, "bayeux is null.");
        }
    }

    private void checkAndInit(String channel) throws CometdException {
        checkBayeuxServer();
        checkSession();
        checkChannel(channel);
        bayeux.createChannelIfAbsent(channel, new ConfigurableServerChannel.Initializer() {
            @Override
            public void configureChannel(ConfigurableServerChannel channel) {
                channel.setPersistent(true);
                channel.setLazy(true);
            }
        });
    }

    private void checkSession() throws CometdException {
        if (session == null || !session.isConnected()) {
            throw new CometdException(CometdException.ERROR_CODE_SESSION_ERROR,
                    "session is invalid.");
        }
    }

    private void checkChannel(String channel) throws CometdException {
        if (channel == null || "".equals(channel)) {
            throw new CometdException(CometdException.ERROR_CODE_PRARM_ERROR, "channel is null.");
        }
        if (channel.startsWith(bayeuxChannel)) {
            throw new CometdException(CometdException.ERROR_CODE_PRARM_ERROR, "channel [" + channel
                    + "] is bayeuxChannel.");
        }
        if (channel.startsWith(serviceChannel)) {
            throw new CometdException(CometdException.ERROR_CODE_PRARM_ERROR, "channel [" + channel
                    + "] is serviceChannel.");
        }
    }
}
