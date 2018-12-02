# Author: Mohsen Hatami





import os






def get_overflow_users(log_dir, home_sizes_filename, quota):
    '''
    parameters: log_dir <string>, home_sizes_filename <string>, quota <integer>
    checks that homes sizes is over 50G or not
    returns list of overflow users
    '''
    
    with open(log_dir + "/" + home_sizes_filename) as file:
        homes = file.readlines()
    homes = [h.strip('\n') for h in homes]

    overflow_users = []
    for home in homes:
        # get username
        username = home.split('\t')[-1].split('/')[-1]
        # get usage
        disk_usage = home.split('\t')[0]
        # Its Gigabyte or not
        meter = disk_usage[-1]
        if meter == 'T':
            overflow_users.append(username)
        elif meter == 'G' and int(disk_usage[:-1]) > quota:
            overflow_users.append(username)
        
    return overflow_users







def is_ignored(ignored_users_filepath, users):
    '''
    parameters: ignored_users_filepath <string>, users <list>
    removes users in the ignore list from users list
    returns list of not ignored users
    '''

    with open(ignored_users_filepath) as file:
        ignored_users = file.readlines()
    ignored_users = [u.strip('\n').strip() for u in ignored_users]

    not_ignored_users = []
    for user in users:
        if not user in ignored_users:
            not_ignored_users.append(user)

    return not_ignored_users






if __name__ == "__main__":
    homes_dir = "/home"
    log_dir = "/var/log/disk_quota"
    home_sizes_filename = "disk_usages.txt"
    os.system("rm -rf " + log_dir + "/" + home_sizes_filename)
    os.system("find " + homes_dir + " -maxdepth 1 -exec du -sh {} >> " + log_dir + "/" + home_sizes_filename + " \;")
    users = get_overflow_users(log_dir, home_sizes_filename, 50)
    ignored_users_filepath = "/etc/ignored_users.txt"
    overflow_users = is_ignored(ignored_users_filepath, users)
    print(overflow_users)