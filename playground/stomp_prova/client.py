import stomp
import logging

# 🔧 Configurazione logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(message)s'
)


def main():
    conn = stomp.Connection([("127.0.0.1", 61613)])

    conn.connect(wait=True)

    conn.send("/queue/test", "Ciao sono il client Gigi")

    logging.info(f"Message sent")

    conn.disconnect()




if __name__ == "__main__":
    main()