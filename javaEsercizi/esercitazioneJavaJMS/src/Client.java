import java.util.Hashtable;
import java.util.Random;

import javax.jms.*;
import javax.naming.*;

public class Client {
    static Hashtable<String, String> prop = new Hashtable<String, String>();
    final static int MESSAGE_NUMBER = 10;

    public static void main(String[] args) {
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");
        
        prop.put( "queue.request", "request" );
        prop.put( "queue.response", "response" );

        try {
            Context jndiContext = new InitialContext(prop);

            QueueConnectionFactory queueConnFactory = (QueueConnectionFactory) jndiContext.lookup("QueueConnectionFactory");

            Queue queueRequest = (Queue)jndiContext.lookup("request");
            Queue queueResponse = (Queue)jndiContext.lookup("response");

            try {
                QueueConnection queueRequestConn = queueConnFactory.createQueueConnection();
                QueueConnection queueResponseConn = queueConnFactory.createQueueConnection();

                QueueSession queueRequestSession = queueRequestConn.createQueueSession(false,Session.AUTO_ACKNOWLEDGE);
                QueueSession queueResponseSession = queueResponseConn.createQueueSession(false, Session.AUTO_ACKNOWLEDGE);

                QueueSender sender = queueRequestSession.createSender(queueRequest);

                MapMessage message = queueRequestSession.createMapMessage();

                for (int i = 0; i < MESSAGE_NUMBER; i++) {
                    //messaggi di tipo deposito 
                    if(i <5){
                        message.setString("operazione", "deposita");
                        Random random = new Random();
                        int id_articolo = random.nextInt(10);
                        
                        message.setInt("id_articolo", id_articolo);

                        System.out.println("[CLIENT] Richiesta generata correttamente: " + message.toString());

                        sender.send(message);
                    }
                    //messaggi di tipo preleva
                    else{
                        message.setString("operazione", "preleva");

                        System.out.println("[CLIENT] Richiesta generata correttamente: " + message.toString());
                        sender.send(message);
                    }
                }
                
                sender.close();
                queueRequestConn.close();
                queueRequestSession.close();

                //sezione di receive asincrona
                queueResponseConn.start(); //abilitiamo la ricezione
                QueueReceiver receiver = queueResponseSession.createReceiver(queueResponse);

                MapMessageListenerClient mapMsgListener = new MapMessageListenerClient();

                receiver.setMessageListener(mapMsgListener);


            } catch (JMSException e) {
                e.printStackTrace();
            }
            

        } catch (NamingException e) {
            e.printStackTrace();
        }

    }
    
}
