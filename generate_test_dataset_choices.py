# Assisted by WCA for GP
# Latest GenAI contribution: granite-20B-code-instruct-v2 model
'''
How to run
$ python3 generate_test_dataset_choices.py
'''

import random
import string
import os
from datetime import datetime, timedelta
import dateutil.parser

def gather_user_inputs_for_segment_user(select, schedule):
    config = {}

    if schedule == "hour":
        config['start_time_str'] = input("What is the start time for the segment, specify hour? (ex: 2024-01-01 09:00) ").strip()
        config['num_hours'] = int(input("How many hours do you want to generate events? (ex: 2) "))
        print ("")

    if schedule == "day":
        start_date_str = input("What is the start date for the segment? (ex: 2024-01-01) ").strip()
        config['start_date'] = dateutil.parser.parse(start_date_str, dayfirst=True)
        end_date_str = input("What is the end date for the segment? (ex: 2024-01-01) " ).strip()
        config['end_date'] = dateutil.parser.parse(end_date_str, dayfirst=True)

    if select == "users":
        config['record_rate_per_hr_per_user'] = int(input("Approximately how many events do you want per hour per 'normal' user? ")) 
        config['num_anomalous_users'] = int(input("How many users should misbehave (anomalous users) in this segment? ") or "0")
        
        if config['num_anomalous_users'] > 0:
            config['anomaly_change_ratio_user'] = int(input("What ratio should be applied to the rate for the anomalous users? "))
    
    if select == "datasources":
        config['record_rate_per_hr_per_datasource'] = int(input("Approximately how many records do you want per hour per 'normal' data source? "))
        config['num_anomalous_data_sources'] = int(input("How many data sources should misbehave (anomalous data sources) in this segment? ") or "0")
        if config['num_anomalous_data_sources'] > 0:
            config['anomaly_change_ratio_datasource'] = float(input("What ratio should be applied to the rate for the anomalous data? "))
    
    return config


def validate_user_inputs(num_data_sources, num_user, config):
    
    if config.get('num_anomalous_data_sources') and config['num_anomalous_data_sources'] > num_data_sources:
        exit('Number of anomalous data sources (' + str(config['num_anomalous_data_sources']) + ') cannot exceed the number of data sources available (' + str(num_data_sources) + ')')
        #exit(0)
    if config.get('num_anomalous_users') and config['num_anomalous_users'] > num_user:
        exit('Number of anomalous user (' + str(config['num_anomalous_users']) + ') cannot exceed the number of users available (' + str(num_user) + ')')
        #exit(0)    
"""
def validate_user_inputs_datasource(num_data_sources, config):
    if config['num_anomalous_data_sources'] > num_data_sources:
        print('Number of anomalous data sources (' + str(config['num_anomalous_data_sources']) + ') cannot exceed the number of data sources available (' + str(num_data_sources) + ')')
        exit(0)

def validate_user_inputs_user(num_user, config):
    if config['num_anomalous_users'] > num_user:
        print('Number of anomalous user (' + str(config['num_anomalous_users']) + ') cannot exceed the number of users available (' + str(num_user) + ')')
        exit(0)        
"""
def main():
 
    print ("") 
    # Prompt the user for the number of different data source names they want
    num_data_sources = int(input("How many different data source names do you want? "))
    # Generate a list of random data source names
    data_source_names = ["testdatasource_" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10)) for _ in range(num_data_sources)]
    print (data_source_names)
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
            while anomalous_select not in ["users", "datasources"]:
                anomalous_select = input("Do you want to generate events for anomalous users or datasources? (users or datasources) ").strip()
                if anomalous_select not in ["users", "datasources"]:
                    print ("Please input either users or datasources")

            while anomalous_schedule not in ["hour", "day"]:
                anomalous_schedule = input("Do you want to generate events in hour YYYY-MM-DD HH:MM or day YYYY-MM-DD basis? (hour or day) ").strip()
                if anomalous_schedule not in ["hour", "day"]:
                    print ("Please input either hour or day")
            
            print("")
   
            segment_config = gather_user_inputs_for_segment_user(anomalous_select, anomalous_schedule)
            validate_user_inputs(num_data_sources, num_users, segment_config)

            match (anomalous_select, anomalous_schedule): 
                case ("users" ,"hour"):
                    print ("Generating events for anomalous *users* in *hour* basis ....")
                    
                    # Fetch end time, type is datetime
                    dt = datetime.strptime(segment_config['start_time_str'], '%Y-%m-%d %H:%M') # change to datetime format
                    count = 0
                    
                    print ("--------------------------------------------------------------------------")
                    for num_hour in range(0, segment_config['num_hours']):
                        print ("hour count = " + str(num_hour))
                        # Do anomalous user first, generate events * ratio
                        for user_name in user_names[:segment_config['num_anomalous_users']]:
                            print ("anomalous_user name = " + user_name)
                            for record in range (0,int(segment_config['record_rate_per_hr_per_user']) * segment_config['anomaly_change_ratio_user']):
                                random_date = dt + timedelta(hours=num_hour, minutes=random.randint(0, 59), seconds=random.randint(0, 59))
                                # Write the log line to the file
                                line = "<10>" + random_date.strftime("%b %d %H:%M:%S") + " " + random.choice(data_source_names) + " " + random_date.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.85.141; s_port: 53049; dst: 192.168.151.175; service: 443; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 9096cbb1;src_user_name: " + user_name +"\n"
                                f.write(line)
                                count += 1
                       
                        # Normal user first, generate events
                        for user_name in user_names[segment_config['num_anomalous_users']:]:
                            print ("normal_user name = " + user_name)
                            for record in range (0,int(segment_config['record_rate_per_hr_per_user'])):
                                random_date = dt + timedelta(hours=num_hour, minutes=random.randint(0, 59), seconds=random.randint(0, 59))
                                # Write the log line to the file
                                line = "<10>" + random_date.strftime("%b %d %H:%M:%S") + " " + random.choice(data_source_names) + " " + random_date.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.85.141; s_port: 53049; dst: 192.168.151.175; service: 443; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 9096cbb1;src_user_name: " + user_name +"\n"
                                f.write(line)   
                                count += 1
                    print ("total event count = " + str(count))            
                    create_segment = bool(input("Do you want to create another log segment? (yes/no) ") == "yes")
                    print ("--------------------------------------------------------------------------")

                case ("users" ,"day"):
                    print ("Generating events for anomalous *users* in *day* basis ....")
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
                                for record in range (0,int(segment_config['record_rate_per_hr_per_user']) * segment_config['anomaly_change_ratio_user']):
                                    # Calculate a random timestamp within the current hour
                                    seconds_so_far = hour_of_day * 60 * 60
                                    delta = timedelta(seconds=(random.randint(0, 60 * 60) + seconds_so_far)) 
                                    timestamp = day_start + delta

                                    # Write the log line to the file
                                    line = "<10>" + timestamp.strftime("%b %d %H:%M:%S") + " " + random.choice(data_source_names) + " " + timestamp.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.85.141; s_port: 53049; dst: 192.168.151.175; service: 443; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 9096cbb1;src_user_name: " + user_name +"\n"
                                    f.write(line)
                                    count += 1

                            # Normal user first, generate events
                            for user_name in user_names[segment_config['num_anomalous_users']:]:
                                print ("normal_user name = " + user_name)
                                for record in range (0,int(segment_config['record_rate_per_hr_per_user'])):
                                    # Calculate a random timestamp within the current hour
                                    seconds_so_far = hour_of_day * 60 * 60
                                    delta = timedelta(seconds=(random.randint(0, 60 * 60) + seconds_so_far)) 
                                    timestamp = day_start + delta

                                    # Write the log line to the file
                                    line = "<11>" + timestamp.strftime("%b %d %H:%M:%S") + " " + random.choice(data_source_names) + " " + timestamp.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.85.141; s_port: 53049; dst: 192.168.151.175; service: 443; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 9096cbb1;src_user_name: " + user_name +"\n"
                                    f.write(line)
                                    count += 1
                            
                            # TODO 'for data_source_name in anomalous_data_source_names[:segment_config.num_anomalous_data_sources]' - also generate the normal data and the abnormal data for the anomalous sources
                            # Need to make sure you are generating the anomaly only in one place, and the rest of the time is fine        

                        # Increment the current date by one day
                        current_date += timedelta(days=1)
                        print ("total event count = " + str(count))    

                    print(f"Log file written to {filename}")

                    create_segment = bool(input("Do you want to create another log segment? (yes/no) ") == "yes")

                    print ("--------------------------------------------------------------------------")

                case ("datasources" ,"hour"):
                    print ("Generating events for anomalous *datasources* in *hour* basis ....")
                    print ("--------------------------------------------------------------------------")
                   
                    # Fetch end time, type is datetime
                    dt = datetime.strptime(segment_config['start_time_str'], '%Y-%m-%d %H:%M') # change to datetime format
                    count = 0

                    print ("--------------------------------------------------------------------------")
                    for num_hour in range(0, segment_config['num_hours']):
                        print ("hour count = " + str(num_hour))
                        # Do anomalous data sources first
                        for data_source_name in data_source_names[:segment_config['num_anomalous_data_sources']]:
                            print ("anomalous_datasource name = " + data_source_name)
                            for record_count in range(0,int(segment_config['record_rate_per_hr_per_datasource'] * segment_config['anomaly_change_ratio_datasource'])):
                                random_date = dt + timedelta(hours=num_hour, minutes=random.randint(0, 59), seconds=random.randint(0, 59))
                                # Write the log line to the file
                                line = "<13>" + random_date.strftime("%b %d %H:%M:%S") + " " + data_source_name + " " + random_date.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.85.141; s_port: 53049; dst: 192.168.151.175; service: 443; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 9096cbb1;src_user_name: " + random.choice(user_names) +"\n"
                                f.write(line)
                                count += 1
                       
                        # Now the rest of the data sources
                        for data_source_name in data_source_names[segment_config['num_anomalous_data_sources']:]:
                            print ("normal_datasource name = " + data_source_name)
                            for record_count in range(0,segment_config['record_rate_per_hr_per_datasource']):
                                random_date = dt + timedelta(hours=num_hour, minutes=random.randint(0, 59), seconds=random.randint(0, 59))
                                # Write the log line to the file
                                line = "<13>" + random_date.strftime("%b %d %H:%M:%S") + " " + data_source_name + " " + random_date.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.85.141; s_port: 53049; dst: 192.168.151.175; service: 443; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 9096cbb1;src_user_name: " + random.choice(user_names) +"\n"
                                f.write(line)
                                count += 1   

                    print ("total event count = " + str(count))    
                    create_segment = bool(input("Do you want to create another log segment? (yes/no) ") == "yes")
                    print ("--------------------------------------------------------------------------")

                case ("datasources" ,"day"):
                    print ("Generating events for anomalous *datasources* in *day* basis ....")    
                    
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
                            for data_source_name in data_source_names[:segment_config['num_anomalous_data_sources']]:
                                print ("anomalous_datasource name = " + data_source_name)
                                for record_count in range(0,int(segment_config['record_rate_per_hr_per_datasource'] * segment_config['anomaly_change_ratio_datasource'])):
                                    # Calculate a random timestamp within the current hour
                                    seconds_so_far = hour_of_day * 60 * 60
                                    delta = timedelta(seconds=(random.randint(0, 60 * 60) + seconds_so_far)) 
                                    timestamp = day_start + delta

                                    # Write the log line to the file
                                    line = "<13>" + timestamp.strftime("%b %d %H:%M:%S") + " " + data_source_name + " " + timestamp.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.85.141; s_port: 53049; dst: 192.168.151.175; service: 443; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 9096cbb1;src_user_name: " + random.choice(user_names) +"\n"
                                    f.write(line)
                                    count += 1

                            # Now the rest of the data sources
                            for data_source_name in data_source_names[segment_config['num_anomalous_data_sources']:]:
                                print ("normal_datasource name = " + data_source_name)
                                for record_count in range(0,segment_config['record_rate_per_hr_per_datasource']):
                                    # Calculate a random timestamp within the current hour
                                    seconds_so_far = hour_of_day * 60 * 60
                                    delta = timedelta(seconds=(random.randint(0, 60 * 60) + seconds_so_far)) 
                                    timestamp = day_start + delta

                                    # Write the log line to the file
                                    line = "<13>" + timestamp.strftime("%b %d %H:%M:%S") + " " + data_source_name + " " + timestamp.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.85.141; s_port: 53049; dst: 192.168.151.175; service: 443; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 9096cbb1;src_user_name: " + random.choice(user_names) +"\n"
                                    f.write(line)
                                    count += 1
                            
                            # TODO 'for data_source_name in anomalous_data_source_names[:segment_config.num_anomalous_data_sources]' - also generate the normal data and the abnormal data for the anomalous sources
                            # Need to make sure you are generating the anomaly only in one place, and the rest of the time is fine        

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