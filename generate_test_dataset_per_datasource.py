# Assisted by WCA for GP
# Latest GenAI contribution: granite-20B-code-instruct-v2 model
'''
# How to run
$ python3 generate_test_dataset_per_datasource.py

# Capabilities
This script is targeted to ONE data source only. It can be used to generate events for 3 options

# Logs (low level category = llc)
Log #1: llc = 4002
<13>Aug 06 11:28:31 CheckPointSource1 06Aug2018 11:28:31 accept 10.94.82.7 product: FG; src: 10.94.83.97; s_port: 52518; dst: 10.10.9.172; service: 123; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];dst_machine_name: admin1@qradar.ibm.test;has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 96b6d43a;src_user_name: testSourceUser

Log #2: llc = 3087
<13>Jan 25 22:44:01 CheckPointSource1 25Jan2018 22:44:01 authcrypt 10.0.0.1 product: Linux OS; src: ; s_port: ; dst: ; service: ; proto: ; rule: ;Src: 10.0.0.1;default_device_message: <85>sshd[20132]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=10.0.0.1  user=admin1 ;facility: security/authorization messages;has_accounting: 0;i/f_dir: inbound;is_first_for_luuid: 131072;logId: -1;log_sequence_num: 5;log_type: log;log_version: 5;login_status: failed;product_category: OS;syslog_severity: Notice;user: admin1;

Log #3: llc = 8052 with sent_byte value
<13>Feb 02 11:38:01 CheckPointSource1 02Feb2018 11:38:01 allow 192.168.0.1 product: URL Filtering; src: 192.168.0.2; s_port: 51025; dst: 192.168.0.3; service: 80; proto: tcp; rule: ;Suppressed logs: 2;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={1D408E4A-5B33-824C-9F61-F2DD7E497DF9};mgmt=qradar01;date=1517574134;policy_name=nypa_05012014];app_id: 647297687;app_properties: Business / Economy,Computers / Internet,URL Filtering;app_risk: 0;app_rule_id: {B12F2AF7-D7C3-4F9A-9B4E-669E6B96C899};app_rule_name: Whitelisted Apps/Sites;appi_name: qradar.test;browse_time: 0:00:07;bytes: 862;has_accounting: 0;i/f_dir: outbound;i/f_name: bond1;matched_category: Business / Economy;origin_sic_name: CN=wally,O=qradar..ibm;proxy_src_ip: 192.168.0.2;received_bytes: 426;resource: http://qradar.ibm.test/;sent_bytes: 436;snid: 2e49b566;src_machine_name: qradar@ibm.test;src_user_name: qradar, ibm (user) ;user: qradar, ibm (user) ;web_client_type: Other: Endpoint Management System Agent/3.81.000.003;web_server_type: Apache;

Log #4: llc = 8052 with sent_bytes value
<13>Mar 29 12:25:02 CheckPointSource1 29Mar2021 12:25:02  10.1.2.100 product: SmartDefense; src: ; s_port: ; dst: ; service: ; proto: ; rule: ;Suppressed logs: 1;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={AAAA1111-A1B2-A3D3-BB22-AAABBBXXX111};mgmt=TESTTESTTEST1GMT;date=1616143020;policy_name=Test_Azure_Prod_Policy.30];has_accounting: 0;i/f_dir: inbound;is_first_for_luuid: 0;logId: -1;log_id: 2;log_sequence_num: 15;log_type: log;log_version: 5;origin_sic_name: CN=TESTTESTTEST18,O=TESTTESTTEST1MGMT..ttsv4a;received_bytes: 0;sent_bytes: 0;

---------------------------
# 1. By Low Level Category
---------------------------
There are built-in logs with 3 low level category, 4002, 3087, 8052. Below is the sample of how to create logs with different ratio for each low level category
```
    Generate events for anomalous low level category (llc), users or src_byte_count? llc
    # events per hour for each low level category = 10  
    Anomalous Ratio Rate for Log #1 = 1   ----> all normal, log#1 has 10 events
    Anomalous Ratio Rate for Log #2 = 1   ----> all normal, log#2 has 10 events
    Anomalous Ratio Rate for Log #3 = 1   ----> all normal, log#3 has 10 events
    Generate events for anomalous low level category (llc), users or src_byte_count? llc
    # events per hour for each low level category? 10
    Anomalous Ratio Rate for Log #1 = 2   ----> log#1 has 20 events           
    Anomalous Ratio Rate for Log #2 = 0.5 ----> log#2 has 5 events     
    Anomalous Ratio Rate for Log #3 = 0.5 ----> log#3 has 5 events  
```
---------------------------
# 2. By Users
---------------------------
We can also generate logs for anomalous user. Below is the sample of how to create logs with xxx user which has no events
```
    Generate events for anomalous low level category (llc), users or src_byte_count? users
    # events do you want per hour for each 'normal' user = 10
    # users should misbehave (anomalous users) in this segment = 1
    Ratio is applied to the rate for the anomalous users = 1   ----> all users has 10 events   
    Generate events for anomalous low level category (llc), users or src_byte_count? users
    # events do you want per hour for each 'normal' user = 10
    # users should misbehave (anomalous users) in this segment = 1
    Ratio is applied to the rate for the anomalous users = 0  ----> one user has no event
```
---------------------------
# 3. By source_byte_count
---------------------------
We have predefined 2 logs which you can specify the sent_byte value for each
To meet the case as below
* First 4 weeks:
  - log#111 (sent_bytes = 111): 10 events/hr
  - log#222 (sent_bytes = 111)  : 10 events/hr
* Then 1 hour:
  - log#111 (sent_bytes = 111): 10 events/hr
  - log#222 (sent_bytes = 10000)  : 10 events/hr

Below is the sample
```
    Generate events for anomalous low level category (llc), users or src_byte_count? src_byte_count
    # events do you want per hour for normal src_byte value = 10
    We have provide 2 logs to set sent_byte value.

    Please specify the sent_byte value you would like to apply to the first log.
    log #1 sent_byte = 111

    Please specify the sent_byte value you would like to apply to the second log.
    log #2 sent_byte = 10000

    
```


'''

import random
import string
import os
from datetime import datetime, timedelta
import dateutil.parser

def gather_user_inputs_for_segment_user(select, schedule):
    config = {}

    if schedule == "hour":
        config['start_time_str'] = input("What is the start time for the segment, specify hour? (ex: 2024-03-01 09:00) ").strip()
        config['num_hours'] = int(input("How many hours do you want to generate events? (ex: 2) "))
        print ("")

    if schedule == "day":
        start_date_str = input("What is the start date for the segment? (ex: 2024-03-01) ").strip()
        config['start_date'] = dateutil.parser.parse(start_date_str, dayfirst=False)
        end_date_str = input("What is the end date for the segment? (ex: 2024-03-01) " ).strip()
        config['end_date'] = dateutil.parser.parse(end_date_str, dayfirst=False)

    if select == "users":
        config['event_rate_per_hr_per_user'] = int(input("Approximately how many events do you want per hour for each 'normal' user? ")) 
        config['num_anomalous_users'] = int(input("How many users should misbehave (anomalous users) in this segment? ") or "0")
        
        if config['num_anomalous_users'] > 0:
            config['anomaly_change_ratio_user'] = int(input("Please specify the anomalous ratio.\nIf you want to keep the log in normal rate, please input 1. \nIf you want to have a user without any events, please input 0\n What ratio should be applied to the rate for the anomalous users? "))
    
    if select == "src_byte":
        config['event_rate_per_hr_per_src_byte'] = int(input("Approximately how many events do you want per hour for normal src_byte value? "))
        config['sent_byte_1'] = int(input("\nWe have provide 2 logs to set sent_byte value.\n\nPlease specify the sent_byte value you would like to apply to the first log.\n log #1 sent_byte = "))
        config['sent_byte_2'] = int(input("\nPlease specify the sent_byte value you would like to apply to the second log.\n log #2 sent_byte = "))
        
        #config['anomaly_change_ratio_src_byte'] = float(input("Please specify *anomalous* ratio to the large src_byte events.\nIf you want to keep the log in normal rate, please input 1\nAnomalous Ratio Rate for large src_byte = "))
        #config['num_anomalous_data_sources'] = int(input("How many data sources should misbehave (anomalous data sources) in this segment? ") or "0")
        #if config['num_anomalous_data_sources'] > 0:
        #    config['anomaly_change_ratio_datasource'] = float(input("What ratio should be applied to the rate for the anomalous data? "))

    if select == "llc": # low level category
        config['event_rate_per_hr_per_llc'] = int(input("Approximately how many events do you want per hour for each low level category? "))
        config['anomaly_change_ratio_llc_1'] = float(input("We have 3 built-in logs, Please specify the *anomalous* ratio to the rate for each log. \nIf you want to keep the normal rate, please input 1. \nAnomalous Ratio Rate for Log #1 = "))
        config['anomaly_change_ratio_llc_2'] = float(input("Anomalous Ratio Rate for Log #2 = "))
        config['anomaly_change_ratio_llc_3'] = float(input("Anomalous Ratio Rate for Log #3 = "))
        
    return config


def validate_user_inputs(num_user, config):
    
    #if config.get('num_anomalous_data_sources') and config['num_anomalous_data_sources'] > num_data_sources:
    #    exit('Number of anomalous data sources (' + str(config['num_anomalous_data_sources']) + ') cannot exceed the number of data sources available (' + str(num_data_sources) + ')')
    #    #exit(0)
    if config.get('num_anomalous_users') and config['num_anomalous_users'] > num_user:
        exit('Number of anomalous user (' + str(config['num_anomalous_users']) + ') cannot exceed the number of users available (' + str(num_user) + ')')
        #exit(0)    

def main():
 
    print ("") 
    # Prompt the user for the number of different data source names they want
    # Generate a list of random data source names
    '''
    num_data_sources = int(input("How many different data source names do you want? "))
    data_source_names = ["testdatasource_" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10)) for _ in range(num_data_sources)]
    print (data_source_names)
    '''
    
    # Generate one random data source names
    single_data_source = "testdatasource_" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    print (single_data_source)
    print ("")

    num_users = int(input("How many different user names do you want? "))
    # Generate a list of random data source names
    user_names = ["user_" + ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 5))) for _ in range(num_users)]
    print (user_names)                  
    print ("")

    create_segment = bool(input("Do you want to start creating log segments? (yes/no) ") == "yes")

    # Open a file for writing
    filename = "test_dataset_1.syslog"
    with open(filename, "w") as f:
        while create_segment:
            anomalous_select = ""
            anomalous_schedule = ""

            # Prompt the user for the choices of events bases on hourly or day
            while anomalous_select not in ["llc", "users", "src_byte"]:
                anomalous_select = input("Do you want to generate events for anomalous low level category (llc), users or src_byte? (llc, users, src_byte) ").strip()
                if anomalous_select not in ["llc, ""users", "src_byte"]:
                    print ("Please input either llc, users, src_byte")

            while anomalous_schedule not in ["hour", "day"]: #  hour YYYY-MM-DD HH:MM, day YYYY-MM-DD
                anomalous_schedule = input("Do you want to generate events in hour or day basis? (hour or day) ").strip()
                if anomalous_schedule not in ["hour", "day"]:
                    print ("Please input either hour or day")
            
            print("")
   
            segment_config = gather_user_inputs_for_segment_user(anomalous_select, anomalous_schedule)
            #validate_user_inputs(num_data_sources, num_users, segment_config)
            validate_user_inputs(num_users, segment_config)

            match (anomalous_select, anomalous_schedule): 

                # generate events with 3 low level category per data source
                case ("llc" ,"hour"):
                    print ("--------------------------------------------------------------------------")
                   
                    # Fetch end time, type is datetime
                    dt = datetime.strptime(segment_config['start_time_str'], '%Y-%m-%d %H:%M') # change to datetime format
                    count = 0

                    for num_hour in range(0, segment_config['num_hours']):
                        print (type(random.choice(user_names)))
                        # Do anomalous data sources first
                        #for data_source_name in data_source_names:
                        for record_count in range(0,int(segment_config['event_rate_per_hr_per_llc'] * segment_config['anomaly_change_ratio_llc_1'])):
                            random_date = dt + timedelta(hours=num_hour, minutes=random.randint(0, 59), seconds=random.randint(0, 59))
                            # Write the log line to the file
                            # Log #1: llc = 4002, with anomaly_change_ratio_llc_1
                            line = "<13>" + random_date.strftime("%b %d %H:%M:%S") + " " + single_data_source + " " + random_date.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.83.97; s_port: 52518; dst: 10.10.9.172; service: 123; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];dst_machine_name: admin1@qradar.ibm.test;has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 96b6d43a;src_user_name: " + random.choice(user_names) + "\n"
                            f.write(line)
                            count += 1
                        for record_count in range(0,int(segment_config['event_rate_per_hr_per_llc'] * segment_config['anomaly_change_ratio_llc_2'])):
                            random_date = dt + timedelta(hours=num_hour, minutes=random.randint(0, 59), seconds=random.randint(0, 59))
                            # Write the log line to the file
                            # Log #2: llc = 3087, with anomaly_change_ratio_llc_2
                            line = "<13>" + random_date.strftime("%b %d %H:%M:%S") + " " + single_data_source + " " + random_date.strftime("%b%d%Y %H:%M:%S") + " authcrypt 10.0.0.1 product: Linux OS; src: ; s_port: ; dst: ; service: ; proto: ; rule: ;Src: 10.0.0.1;default_device_message: <85>sshd[20132]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=10.0.0.1  user=admin1 ;facility: security/authorization messages;has_accounting: 0;i/f_dir: inbound;is_first_for_luuid: 131072;logId: -1;log_sequence_num: 5;log_type: log;log_version: 5;login_status: failed;product_category: OS;syslog_severity: Notice;user: " + random.choice(user_names) +"\n"
                            f.write(line)
                            count += 1
                        for record_count in range(0,int(segment_config['event_rate_per_hr_per_llc'] * segment_config['anomaly_change_ratio_llc_3'])):
                            random_date = dt + timedelta(hours=num_hour, minutes=random.randint(0, 59), seconds=random.randint(0, 59))
                            # Write the log line to the file
                            # Log #3: llc = 8052, with anomaly_change_ratio_llc_3
                            line = "<13>" + random_date.strftime("%b %d %H:%M:%S") + " " + single_data_source + " " + random_date.strftime("%b%d%Y %H:%M:%S") + " allow 192.168.0.1 product: URL Filtering; src: 192.168.0.2; s_port: 51025; dst: 192.168.0.3; service: 80; proto: tcp; rule: ;Suppressed logs: 2;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={1D408E4A-5B33-824C-9F61-F2DD7E497DF9};mgmt=qradar01;date=1517574134;policy_name=nypa_05012014];app_id: 647297687;app_properties: Business / Economy,Computers / Internet,URL Filtering;app_risk: 0;app_rule_id: {B12F2AF7-D7C3-4F9A-9B4E-669E6B96C899};app_rule_name: Whitelisted Apps/Sites;appi_name: qradar.test;browse_time: 0:00:07;bytes: 862;has_accounting: 0;i/f_dir: outbound;i/f_name: bond1;matched_category: Business / Economy;origin_sic_name: CN=wally,O=qradar..ibm;proxy_src_ip: 192.168.0.2;received_bytes: 426;resource: http://qradar.ibm.test/;sent_bytes: 123;snid: 2e49b566;src_machine_name: qradar@ibm.test;src_user_name: qradar, ibm (" + random.choice(user_names) + ") " + ";user: qradar, ibm (user) ;web_client_type: Other: Endpoint Management System Agent/3.81.000.003;web_server_type: Apache;"+"\n"
                            f.write(line)
                            count += 1           
                    print ("total event count = " + str(count))    
                    create_segment = bool(input("Do you want to create another log segment? (yes/no) ") == "yes")
                    print ("--------------------------------------------------------------------------")

                case ("llc" ,"day"):
                    print ("Generating events depend on low level category in DAY basis ....")
                    
                    # Loop through each day in the specified date range
                    current_date = segment_config['start_date']
                    count = 0
                    while current_date <= segment_config['end_date']:
                        # Get the timestamp for the start of the day
                        day_start = datetime(current_date.year, current_date.month, current_date.day)

                        print ("--------------------------------------------------------------------------")
                        # Generate log lines for the current day
                        for hour_of_day in range(0, 24):
                            # Do anomalous data sources first
                            #for data_source_name in data_source_names:
                            for record_count in range(0,int(segment_config['event_rate_per_hr_per_llc'] * segment_config['anomaly_change_ratio_llc_1'])):
                                # Calculate a random timestamp within the current hour
                                seconds_so_far = hour_of_day * 60 * 60
                                delta = timedelta(seconds=(random.randint(0, 60 * 60) + seconds_so_far)) 
                                timestamp = day_start + delta

                                # Write the log line to the file
                                # Log #1: llc = 4002, with anomaly_change_ratio_llc_1
                                line = "<13>" + timestamp.strftime("%b %d %H:%M:%S") + " " + single_data_source + " " + timestamp.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.83.97; s_port: 52518; dst: 10.10.9.172; service: 123; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];dst_machine_name: admin1@qradar.ibm.test;has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 96b6d43a;src_user_name: " + random.choice(user_names) +"\n"
                                f.write(line)
                                count += 1
                            for record_count in range(0,int(segment_config['event_rate_per_hr_per_llc'] * segment_config['anomaly_change_ratio_llc_2'])):
                                # Calculate a random timestamp within the current hour
                                seconds_so_far = hour_of_day * 60 * 60
                                delta = timedelta(seconds=(random.randint(0, 60 * 60) + seconds_so_far)) 
                                timestamp = day_start + delta

                                # Write the log line to the file
                                # Log #2: llc = 3087, with anomaly_change_ratio_llc_2
                                line = "<13>" + timestamp.strftime("%b %d %H:%M:%S") + " " + single_data_source + " " + timestamp.strftime("%b%d%Y %H:%M:%S") + " authcrypt 10.0.0.1 product: Linux OS; src: ; s_port: ; dst: ; service: ; proto: ; rule: ;Src: 10.0.0.1;default_device_message: <85>sshd[20132]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=10.0.0.1  user=admin1 ;facility: security/authorization messages;has_accounting: 0;i/f_dir: inbound;is_first_for_luuid: 131072;logId: -1;log_sequence_num: 5;log_type: log;log_version: 5;login_status: failed;product_category: OS;syslog_severity: Notice;user: " + random.choice(user_names) +"\n"
                                f.write(line)
                                count += 1
                            for record_count in range(0,int(segment_config['event_rate_per_hr_per_llc'] * segment_config['anomaly_change_ratio_llc_3'])):
                                # Calculate a random timestamp within the current hour
                                seconds_so_far = hour_of_day * 60 * 60
                                delta = timedelta(seconds=(random.randint(0, 60 * 60) + seconds_so_far)) 
                                timestamp = day_start + delta

                                # Write the log line to the file
                                # Log #3: llc = 8052, with anomaly_change_ratio_llc_3
                                line = "<13>" + timestamp.strftime("%b %d %H:%M:%S") + " " + single_data_source + " " + timestamp.strftime("%b%d%Y %H:%M:%S") + " allow 192.168.0.1 product: URL Filtering; src: 192.168.0.2; s_port: 51025; dst: 192.168.0.3; service: 80; proto: tcp; rule: ;Suppressed logs: 2;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={1D408E4A-5B33-824C-9F61-F2DD7E497DF9};mgmt=qradar01;date=1517574134;policy_name=nypa_05012014];app_id: 647297687;app_properties: Business / Economy,Computers / Internet,URL Filtering;app_risk: 0;app_rule_id: {B12F2AF7-D7C3-4F9A-9B4E-669E6B96C899};app_rule_name: Whitelisted Apps/Sites;appi_name: qradar.test;browse_time: 0:00:07;bytes: 862;has_accounting: 0;i/f_dir: outbound;i/f_name: bond1;matched_category: Business / Economy;origin_sic_name: CN=wally,O=qradar..ibm;proxy_src_ip: 192.168.0.2;received_bytes: 426;resource: http://qradar.ibm.test/;sent_bytes: 436;snid: 2e49b566;src_machine_name: qradar@ibm.test;src_user_name: qradar, ibm (" + random.choice(user_names) + ") " + ";user: qradar, ibm (user) ;web_client_type: Other: Endpoint Management System Agent/3.81.000.003;web_server_type: Apache;"+"\n"
                                f.write(line)
                                count += 1       
                        # Increment the current date by one day
                        current_date += timedelta(days=1)
                        print ("total event count = " + str(count))    

                    print(f"Log file written to {filename}")

                    create_segment = bool(input("Do you want to create another log segment? (yes/no) ") == "yes")
                    print ("--------------------------------------------------------------------------")

                case ("users" ,"hour"):
                    print ("Generating events for user in HOUR basis ....")
                    
                    # Fetch end time, type is datetime
                    dt = datetime.strptime(segment_config['start_time_str'], '%Y-%m-%d %H:%M') # change to datetime format
                    count = 0
                    
                    print ("--------------------------------------------------------------------------")
                    for num_hour in range(0, segment_config['num_hours']):
                        print ("hour count = " + str(num_hour))
                        # Do anomalous user first, events rate * anomalous ratio
                        for user_name in user_names[:segment_config['num_anomalous_users']]:
                            print ("anomalous_user name = " + user_name)
                            for record in range (0,int(segment_config['event_rate_per_hr_per_user']) * segment_config['anomaly_change_ratio_user']):
                                random_date = dt + timedelta(hours=num_hour, minutes=random.randint(0, 59), seconds=random.randint(0, 59))
                                # Write the log line to the file
                                # Log #1: llc = 4002
                                line = "<10>" + random_date.strftime("%b %d %H:%M:%S") + " " + single_data_source + " " + random_date.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.85.141; s_port: 53049; dst: 192.168.151.175; service: 443; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 9096cbb1;src_user_name: " + user_name +"\n"
                                f.write(line)
                                count += 1
                       
                        # Normal user first, generate events
                        for user_name in user_names[segment_config['num_anomalous_users']:]:
                            print ("normal_user name = " + user_name)
                            for record in range (0,int(segment_config['event_rate_per_hr_per_user'])):
                                random_date = dt + timedelta(hours=num_hour, minutes=random.randint(0, 59), seconds=random.randint(0, 59))
                                # Write the log line to the file
                                # Log #1: llc = 4002
                                line = "<10>" + random_date.strftime("%b %d %H:%M:%S") + " " + single_data_source + " " + random_date.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.85.141; s_port: 53049; dst: 192.168.151.175; service: 443; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 9096cbb1;src_user_name: " + user_name +"\n"
                                f.write(line)   
                                count += 1
                    print ("total event count = " + str(count))            
                    create_segment = bool(input("Do you want to create another log segment? (yes/no) ") == "yes")
                    print ("--------------------------------------------------------------------------")

                case ("users" ,"day"):
                    print ("Generating events for anomalous *users* in DAY basis ....")
                    print ("--------------------------------------------------------------------------")
                    count = 0
                    # Loop through each day in the specified date range
                    current_date = segment_config['start_date']
                    while current_date <= segment_config['end_date']:
                        # Get the timestamp for the start of the day
                        day_start = datetime(current_date.year, current_date.month, current_date.day)

                        print ("--------------------------------------------------------------------------")
                        # Generate log lines for the current day
                        for hour_of_day in range(0, 24):
                            # Do anomalous user first, generate events * ratio
                            for user_name in user_names[:segment_config['num_anomalous_users']]:
                                print ("anomalous_user name = " + user_name)
                                for record in range (0,int(segment_config['event_rate_per_hr_per_user']) * segment_config['anomaly_change_ratio_user']):
                                    # Calculate a random timestamp within the current hour
                                    seconds_so_far = hour_of_day * 60 * 60
                                    delta = timedelta(seconds=(random.randint(0, 60 * 60) + seconds_so_far)) 
                                    timestamp = day_start + delta

                                    # Write the log line to the file
                                    # Log #1: llc = 4002
                                    line = "<10>" + timestamp.strftime("%b %d %H:%M:%S") + " " + single_data_source + " " + timestamp.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.85.141; s_port: 53049; dst: 192.168.151.175; service: 443; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 9096cbb1;src_user_name: " + user_name +"\n"
                                    f.write(line)
                                    count += 1

                            # Normal user first, generate events
                            for user_name in user_names[segment_config['num_anomalous_users']:]:
                                print ("normal_user name = " + user_name)
                                for record in range (0,int(segment_config['event_rate_per_hr_per_user'])):
                                    # Calculate a random timestamp within the current hour
                                    seconds_so_far = hour_of_day * 60 * 60
                                    delta = timedelta(seconds=(random.randint(0, 60 * 60) + seconds_so_far)) 
                                    timestamp = day_start + delta

                                    # Write the log line to the file
                                    # Log #1: llc = 4002
                                    line = "<11>" + timestamp.strftime("%b %d %H:%M:%S") + " " + single_data_source + " " + timestamp.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.85.141; s_port: 53049; dst: 192.168.151.175; service: 443; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 9096cbb1;src_user_name: " + user_name +"\n"
                                    f.write(line)
                                    count += 1
                            
                        # Increment the current date by one day
                        current_date += timedelta(days=1)
                        print ("total event count = " + str(count))    

                    print(f"Log file written to {filename}")

                    create_segment = bool(input("Do you want to create another log segment? (yes/no) ") == "yes")

                    print ("--------------------------------------------------------------------------")

                case ("src_byte" ,"hour"):
                    print ("Generating events for src_byte_count in HOUR basis ....")
                    print ("--------------------------------------------------------------------------")
                   
                    # Fetch end time, type is datetime
                    dt = datetime.strptime(segment_config['start_time_str'], '%Y-%m-%d %H:%M') # change to datetime format
                    count = 0

                    print ("--------------------------------------------------------------------------")
                    for num_hour in range(0, segment_config['num_hours']):
                        print ("hour count = " + str(num_hour))
                        for record_count in range(0,int(segment_config['event_rate_per_hr_per_src_byte'])):
                            random_date = dt + timedelta(hours=num_hour, minutes=random.randint(0, 59), seconds=random.randint(0, 59))
                            # Write the log line to the file
                            # log #3: 8052
                            line = "<13>" + random_date.strftime("%b %d %H:%M:%S") + " " + single_data_source + " " + random_date.strftime("%b%d%Y %H:%M:%S") + " allow 192.168.0.1 product: URL Filtering; src: 192.168.0.2; s_port: 51025; dst: 192.168.0.3; service: 80; proto: tcp; rule: ;Suppressed logs: 2;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={1D408E4A-5B33-824C-9F61-F2DD7E497DF9};mgmt=qradar01;date=1517574134;policy_name=nypa_05012014];app_id: 647297687;app_properties: Business / Economy,Computers / Internet,URL Filtering;app_risk: 0;app_rule_id: {B12F2AF7-D7C3-4F9A-9B4E-669E6B96C899};app_rule_name: Whitelisted Apps/Sites;appi_name: qradar.test;browse_time: 0:00:07;bytes: 862;has_accounting: 0;i/f_dir: outbound;i/f_name: bond1;matched_category: Business / Economy;origin_sic_name: CN=wally,O=qradar..ibm;proxy_src_ip: 192.168.0.2;received_bytes: 426;resource: http://qradar.ibm.test/;sent_bytes: " + str(segment_config['sent_byte_1']) + ";snid: 2e49b566;src_machine_name: qradar@ibm.test;src_user_name: qradar, ibm (" + random.choice(user_names) + ") " + ";user: qradar, ibm (user) ;web_client_type: Other: Endpoint Management System Agent/3.81.000.003;web_server_type: Apache;"+"\n"
                            f.write(line)
                            count += 1 
                            # log #4: 8052
                            line = "<13>" + random_date.strftime("%b %d %H:%M:%S") + " " + single_data_source + " " + random_date.strftime("%b%d%Y %H:%M:%S") + " 10.1.2.100 product: SmartDefense; src: ; s_port: ; dst: ; service: ; proto: ; rule: ;Suppressed logs: 1;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={AAAA1111-A1B2-A3D3-BB22-AAABBBXXX111};mgmt=TESTTESTTEST1GMT;date=1616143020;policy_name=Test_Azure_Prod_Policy.30];has_accounting: 0;i/f_dir: inbound;is_first_for_luuid: 0;logId: -1;log_id: 2;log_sequence_num: 15;log_type: log;log_version: 5;origin_sic_name: CN=TESTTESTTEST18,O=TESTTESTTEST1MGMT..ttsv4a;received_bytes: 0;sent_bytes: " + str(segment_config['sent_byte_2']) +";"+"\n"
                            f.write(line)
                            count += 1    
                    print ("total event count = " + str(count))    
                    create_segment = bool(input("Do you want to create another log segment? (yes/no) ") == "yes")
                    print ("--------------------------------------------------------------------------")

                case ("src_byte" ,"day"):
                    print ("Generating events for src_byte_count in DAY basis ....")    
                    
                    # Loop through each day in the specified date range
                    current_date = segment_config['start_date']
                    count = 0
                    while current_date <= segment_config['end_date']:
                        # Get the timestamp for the start of the day
                        day_start = datetime(current_date.year, current_date.month, current_date.day)

                        print ("--------------------------------------------------------------------------")
                        # Generate log lines for the current day
                        for hour_of_day in range(0, 24):
                            for record_count in range(0,segment_config['event_rate_per_hr_per_src_byte']):
                                # Calculate a random timestamp within the current hour
                                seconds_so_far = hour_of_day * 60 * 60
                                delta = timedelta(seconds=(random.randint(0, 60 * 60) + seconds_so_far)) 
                                timestamp = day_start + delta

                                # Write the log line to the file
                                # log #3: 8052
                                line = "<13>" + timestamp.strftime("%b %d %H:%M:%S") + " " + single_data_source + " " + timestamp.strftime("%b%d%Y %H:%M:%S") + " allow 192.168.0.1 product: URL Filtering; src: 192.168.0.2; s_port: 51025; dst: 192.168.0.3; service: 80; proto: tcp; rule: ;Suppressed logs: 2;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={1D408E4A-5B33-824C-9F61-F2DD7E497DF9};mgmt=qradar01;date=1517574134;policy_name=nypa_05012014];app_id: 647297687;app_properties: Business / Economy,Computers / Internet,URL Filtering;app_risk: 0;app_rule_id: {B12F2AF7-D7C3-4F9A-9B4E-669E6B96C899};app_rule_name: Whitelisted Apps/Sites;appi_name: qradar.test;browse_time: 0:00:07;bytes: 862;has_accounting: 0;i/f_dir: outbound;i/f_name: bond1;matched_category: Business / Economy;origin_sic_name: CN=wally,O=qradar..ibm;proxy_src_ip: 192.168.0.2;received_bytes: 426;resource: http://qradar.ibm.test/;sent_bytes: " + str(segment_config['sent_byte_1']) + ";snid: 2e49b566;src_machine_name: qradar@ibm.test;src_user_name: qradar, ibm (" + random.choice(user_names) + ") " + ";user: qradar, ibm (user) ;web_client_type: Other: Endpoint Management System Agent/3.81.000.003;web_server_type: Apache;"+"\n"
                                f.write(line)
                                count += 1 
                                # log #4: 8052
                                line = "<13>" + timestamp.strftime("%b %d %H:%M:%S") + " " + single_data_source + " " + timestamp.strftime("%b%d%Y %H:%M:%S") + " 10.1.2.100 product: SmartDefense; src: ; s_port: ; dst: ; service: ; proto: ; rule: ;Suppressed logs: 1;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={AAAA1111-A1B2-A3D3-BB22-AAABBBXXX111};mgmt=TESTTESTTEST1GMT;date=1616143020;policy_name=Test_Azure_Prod_Policy.30];has_accounting: 0;i/f_dir: inbound;is_first_for_luuid: 0;logId: -1;log_id: 2;log_sequence_num: 15;log_type: log;log_version: 5;origin_sic_name: CN=TESTTESTTEST18,O=TESTTESTTEST1MGMT..ttsv4a;received_bytes: 0;sent_bytes: " + str(segment_config['sent_byte_2']) +";"+"\n"
                                f.write(line)
                                count += 1
                        # Increment the current date by one day
                        current_date += timedelta(days=1)
                        print ("total event count = " + str(count))    

                    print(f"Log file written to {filename}")

                    create_segment = bool(input("Do you want to create another log segment? (yes/no) ") == "yes")
                    print ("--------------------------------------------------------------------------")
                case _:
                    exit(0)    

if __name__ == "__main__":
    main()