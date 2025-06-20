import java.io.*;
import java.net.*;

public class TCPClient {
    public static void main(String[] args) {
        try {
            // Si connette al server su localhost porta 8080
            Socket socket = new Socket("localhost", 8080);
            System.out.println("Connesso al server!");
            
            // Stream per scrivere al server
            PrintWriter out = new PrintWriter(
                socket.getOutputStream(), true
            );
            
            // Stream per leggere dal server
            BufferedReader in = new BufferedReader(
                new InputStreamReader(socket.getInputStream())
            );
            
            // Invia un messaggio al server
            out.println("Ciao server!");
            
            // Legge la risposta dal server
            String risposta = in.readLine();
            System.out.println("Risposta dal server: " + risposta);
            
            // Chiude la connessione
            socket.close();
            
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}