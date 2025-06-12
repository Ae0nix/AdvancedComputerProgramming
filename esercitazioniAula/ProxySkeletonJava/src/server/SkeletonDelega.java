package src.server;

import src.service.ICounter;

import java.io.IOException;
import java.net.ServerSocket;

public class SkeletonDelega implements ICounter {
    // devo avere un riferimento al counter stesso perché altrimenti non posso invocare l'implementatore

    private ICounter count; //passo un implementatore generico perché non so chi sarà ad implementare

    public SkeletonDelega(ICounter count) {
        this.count = count;
    }

    public void runSkeleton(){
        try {
            ServerSocket serverSocket = new ServerSocket(2500);

        }
        catch (IOException e){

        }
    }

    @Override
    public void sum(int value) {
        count.sum(value);
    }

    @Override
    public void inc() {
        count.inc();
    }

    @Override
    public int get() {
        return count.get();
    }
}
