import javax.jms.JMSException;
import javax.jms.MapMessage;
import javax.jms.Message;
import javax.jms.MessageListener;

public class MapMessageListenerClient implements MessageListener{

    @Override
    public void onMessage(Message m) {
        try {
            System.out.println("Messaggio ricevuto: " + ((MapMessage)m).getInt("id_articolo"));
        } catch (JMSException e) {
            e.printStackTrace();
        }

    }
    
    
}
