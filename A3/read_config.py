import configparser

config = configparser.ConfigParser(strict=False)
config.sections()

# config.read('config.txt')
config.read('config.txt')
docker_compose = "version: '3'\n"
docker_compose += "services:\n"
c=True
volumenes=[]
def workers_create(y,id,port,tipo):
    docker_compose=""
    aux=""
    c=True
    c2=False
    for ite in y.items():
        if (ite[0]=='name'):
            docker_compose += "  W_"+str(port)+ite[1]+"_work_"+str(id)+":"+"\n"
        if (ite[0]=='images'):
            docker_compose += "    image: "+ ite[1]+"\n"
        if (ite[0]=='context'):
            if (c==True):
                docker_compose += "    build:\n"
                c=False
            docker_compose += "      context: "+ ite[1]+"\n"
        if (ite[0]=='dockerfile'):
            if (c==True):
                docker_compose += "   build:\n"
                c=False
            docker_compose += "      dockerfile: "+ ite[1]+"\n"
        if (ite[0]=='volumes'):
            docker_compose += "    volumes:\n      - "+ ite[1]+"\n"
        if (ite[0]=='workers'):
            wor=int(ite[1])
            c2=True
        if (ite[0]=='ip'):
            docker_compose += "    ports:\n      - "+ str(port)+str(id)+":5000"+"\n"
            docker_compose+="    networks:\n      - clus_net\n"
            ip=ite[1]
        if (ite[0]=="params"):
            params=ite[1]
        if (ite[0]=='cmd'):
            if (c2==True):
                docker_compose+='    command: '+ite[1]+" "+str(wor)+" "+ip+" " + str(port)+str(id)+" "+params+"\n"
            elif(c2==False):
                docker_compose+='    command: '+ite[1]+" "+ip+" " + str(port)+str(id)+" "+params+"\n"
            
        if (ite[0]=='type'):
            
            name_worker=ite[1].split(",")
            # Despleado de workers
            aux="\n"
            for wrk in range(wor):
                if ('type' in config.items(tipo)):
                    tipo_2 = config[tipo]['type'].split(',')
                    pos = wrk % len(tipo_2)
                    aux+=workers_create(config[tipo],wrk,str(port)+str(id),tipo_2[pos])
                else:
                    aux+=workers_create(config[tipo],wrk,str(port)+str(id),'')
                aux+="\n"
                    
    docker_compose+=aux
    return docker_compose


for section in config.sections():
    print("\n[%s]" % section)
    c=True
    if (section=='PRE'):
        load='-'
        for item in config.items(section):
            if (item[0]=='name'):
                docker_compose += "  "+item[1]+":"+"\n"
            if (item[0]=='images'):
                docker_compose += "    image: "+ item[1]+"\n"
            if (item[0]=='context'):
                if (c==True):
                    docker_compose += "    build:\n"
                    c=False
                docker_compose += "      context: "+ item[1]+"\n"
            if (item[0]=='dockerfile'):
                if (c==True):
                    docker_compose += "   build:\n"
                    c=False
                docker_compose += "      dockerfile: "+ item[1]+"\n"
            if (item[0]=='ports'):
                docker_compose += "    ports:\n      - "+ item[1]+":5000"+"\n"
                docker_compose+="    networks:\n      - clus_net\n"                
            if (item[0]=='volumes'):
                docker_compose += "    volumes:\n      - "+ item[1]+"\n"
            if (item[0]=='ip'):
                ip=item[1]
            if (item[0]=='cmd'):
                docker_compose+='    command: '+item[1]+" "+ip+"\n"
    if (section=='LOADBALANCEK'):
        for item in config.items(section):
            if (item[0]=='name'):
                docker_compose += "  "+item[1]+":"+"\n"
            if (item[0]=='images'):
                docker_compose += "    image: "+ item[1]+"\n"
            if (item[0]=='context'):
                if (c==True):
                    docker_compose += "    build:\n"
                    c=False
                docker_compose += "      context: "+ item[1]+"\n"
            if (item[0]=='dockerfile'):
                if (c==True):
                    docker_compose += "   build:\n"
                    c=False
                docker_compose += "      dockerfile: "+ item[1]+"\n"
            if (item[0]=='ports'):
                docker_compose += "    ports:\n      - "+ item[1]+":5000"+"\n"
                docker_compose+="    networks:\n      - clus_net\n"
                port=item[1]
            if (item[0]=='volumes'):
                docker_compose += "    volumes:\n      - "+ item[1]+"\n"
            if (item[0]=='workers'):
                workers=int(item[1])
            if (item[0]=='ip'):
                ip=item[1]
            if (item[0]=='cmd'):
                docker_compose+='    command: '+item[1]+" "+str(workers)+" "+ip+" " + port+"\n"
            if (item[0]=='type'):
                name_worker=item[1]
                # Despleado de workers
                docker_aux="\n"
                tipo = config[name_worker]['type'].split(',')
                for wrk in range(workers):
                    pos = wrk % len(tipo)
                    
                    docker_aux+=workers_create(config[name_worker],wrk,port,tipo[pos])
                    docker_aux+="\n"
        docker_compose+=docker_aux
    docker_compose+="\n"

# Volumes
# docker_compose+="volumes:\n"
# for i in volumenes:
#     docker_compose+="  "+i+":\n"
docker_compose+="\nnetworks:\n  clus_net:\n"
f = open("docker-compose.yml", "w")
f.write(docker_compose)
f.close()

