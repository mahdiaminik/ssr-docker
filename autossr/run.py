
import os
import shutil
import re
import base64


AUTH_FILE_PATH='auth.txt'


def base64_encode(text):

        ret = base64.urlsafe_b64encode(text.encode('utf-8')).decode()
        ret = ret.replace("/", "_")
        ret = ret.replace('+', '-')
        while ret[-1] == '=' :
                ret = ret[:-1]
        return ret




def ssrlink(server :str , port:int , password:str , name:str):
        basetxt = '{SERVER_PLAIN}:{PORT_PLAIN}:origin:chacha20:http_simple:{PASSWORD_B64}/?obfsparam=&protoparam=&remarks={NAME_B64}&group=U1NS'
        formatedtxt = basetxt.format(SERVER_PLAIN=server,
                                 PORT_PLAIN=str(port),
                                 PASSWORD_B64=base64_encode(password),
                                 NAME_B64=base64_encode(name))
        return base64_encode(formatedtxt)


run_list = []
direct_list = []
indirect_list = []

def main():
        with open(AUTH_FILE_PATH) as file:
            for line in file:
                line = re.sub(' +', ' ',line).strip()
                if line[0] == '#' :
                    continue

                linesplit = line.split(' ')

                id=linesplit[0].rstrip()
                password=linesplit[1].rstrip()
                username=linesplit[2].rstrip()

                dirpath = f'{id}_{username}'

                port1 = 40000 + int(id)
                port2 = 50000 + int(id)

                envs = {'LOCAL_PORT1' : port1 , 'LOCAL_PORT2' : port2 , 'PASSWORD' : password}
                os.makedirs(dirpath, exist_ok=True)

                content = ''
                with open('docker-compose.yml.template', 'r') as content_file:
                        content = content_file.read()

                content = content.format(**envs)
                with open(f"{dirpath}/docker-compose.yml", "w") as content_file:
                        content_file.write(content)

                run_list.append(f'docker-compose -f {dirpath}/docker-compose.yml up -d;')
                server1 = f'{username}{id}.direct.swaves.ir'
                server2 = f'{username}{id}.indirect.swaves.ir'
                name1   = f'{id}_amini_{username}_direct'
                name2   = f'{id}_amini_{username}_indirect'

                direct_list.append(  f'{id} {username} direct   ssr://{ssrlink(server=server1 , port=port1 , password=password , name=name1)}')
                indirect_list.append(f'{id} {username} indirect ssr://{ssrlink(server=server2 , port=port2 , password=password , name=name2)}')

                #shutil.rmtree(dirpath, ignore_errors=True)

        for v in run_list:
               print(v + " \\")
        #for v in direct_list:
        #       print(v)
        #for v in indirect_list:
        #       print(v)
        for i in range(0,len(direct_list)):
            print("")
            print(direct_list[i])
            print(indirect_list[i])

        
if __name__ == '__main__':
       main()
