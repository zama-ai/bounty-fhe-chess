import socket
import struct
import pickle
import argparse

from infer_clear import Inference_clear

from compile_fhe_inprod import CompileModel
from infer_simfhe import Inference_simfhe

from infer_deepfhe import Inference_deepfhe

parser = argparse.ArgumentParser()
parser.add_argument('-i','--inference', type=str, default='simfhe', help='type of inference clear, simfhe, deepfhe', required=True)
args = parser.parse_args()

def main():

    HOST = ""  # Standard loopback interface address (localhost)
    PORT = 3389  # Port to listen on (non-privileged ports are > 1023)

    if args.inference == "clear":
        inference = Inference_clear()
    elif args.inference == "simfhe":
        compiled_models = CompileModel()
        inference = Inference_simfhe(compiled_models.compiled_source, compiled_models.compiled_target)
    elif args.inference == "deepfhe":
        inference = Inference_deepfhe()
    else:
        print("pls, provide --inference option (clear, simfhe or deepfhe)")

    def recvall(conn, size):
        """letting all bytes to be received as small parts of bytes."""
        buffer = bytes()
        
        remain = size
        while remain  > 0:
            
            data_received  = conn.recv(remain)
            
            if not data_received:
                raise Exception('unexpected EOF')
            buffer += data_received
            remain -= len(data_received)

        return buffer


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        print("socket binded to %s" %(PORT))

        s.listen(5)
        print("socket is listening, server started")

        while True:

            conn, addr = s.accept()
            print(f"Connected by {addr}")
            while True:
                try:
                
                    data_size = struct.unpack('I', conn.recv(4))[0] 
                    byte_data = recvall(conn, data_size)

                
                    #print("Server side len data:",len(byte_data))

                    data = pickle.loads(byte_data)
                    #print("chessboard\n",data)
                    reply = inference.predict(data, 5, 3)
                    #print("inference\n",reply)

                    if not data:
                        print("failed at data --> disconnected")
                        break
                    # elif not reply:
                    #     print("input chessboard before failed at reply\n",data)
                        #print("failed at reply --> disconnected")

                    else:
                        print("\ninput_data as chessboard\n")
                        print(data)
                        print("\ninference list of moves\n")
                        print(reply)

                        conn.sendall(pickle.dumps(reply))

                except :#socket.error as e:
                    #print(e)
                    break
            
            print("Lost connection")
            conn.close()

if __name__ == "__main__":
    main()

