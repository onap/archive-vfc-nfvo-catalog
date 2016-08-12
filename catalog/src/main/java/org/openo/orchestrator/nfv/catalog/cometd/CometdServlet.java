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

import javax.servlet.GenericServlet;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.UnavailableException;
import javax.servlet.http.HttpServletResponse;

import org.cometd.annotation.Listener;
import org.cometd.annotation.ServerAnnotationProcessor;
import org.cometd.annotation.Service;
import org.cometd.bayeux.Message;
import org.cometd.bayeux.server.BayeuxServer;
import org.cometd.bayeux.server.ServerChannel;
import org.cometd.bayeux.server.ServerMessage;
import org.cometd.bayeux.server.ServerSession;
import org.cometd.server.authorizer.GrantAuthorizer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * @author 10189609
 * 
 */
public class CometdServlet extends GenericServlet {

    private static final long serialVersionUID = 1L;

    private static final Logger logger = LoggerFactory.getLogger(CometdServlet.class);

    @Override
    public void init() throws ServletException {
        super.init();

        final BayeuxServer bayeux =
                (BayeuxServer) getServletContext().getAttribute(BayeuxServer.ATTRIBUTE);
        if (bayeux == null) {
            throw new UnavailableException("No BayeuxServer!");
        }

        // Allow anybody to handshake
        bayeux.getChannel(ServerChannel.META_HANDSHAKE)
                .addAuthorizer(GrantAuthorizer.GRANT_PUBLISH);

        // start server processor
        ServerAnnotationProcessor processor = new ServerAnnotationProcessor(bayeux);
        processor.process(new Monitor());

        CometdUtil.setBayeuxServer(bayeux);
    }

    @Override
    public void service(ServletRequest paramServletRequest, ServletResponse paramServletResponse)
            throws ServletException, IOException {
        ((HttpServletResponse) paramServletResponse).sendError(503);
    }

    @Service("monitor")
    public static class Monitor {
        @Listener("/meta/subscribe")
        public void monitorSubscribe(ServerSession session, ServerMessage message) {
            logger.info("Monitored subscribe from " + session + " for "
                    + message.get(Message.SUBSCRIPTION_FIELD));
        }

        @Listener("/meta/unsubscribe")
        public void monitorUnsubscribe(ServerSession session, ServerMessage message) {
            logger.info("Monitored unsubscribe from " + session + " for "
                    + message.get(Message.SUBSCRIPTION_FIELD));
        }

        @Listener("/meta/*")
        public void monitorMeta(ServerSession session, ServerMessage message) {
            logger.debug(message.toString());
        }
    }
}
