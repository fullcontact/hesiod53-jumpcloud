import sys
import argparse

import yaml
import ldap


class Parser(object):

    def __init__(self, config):
        self.config = config

    def parse_all_groups(self, raw_groups):
        groups = []
        for raw_group in raw_groups:
            groups.append(self.parse_group(raw_group[1]))

        return groups

    def parse_group(self, group):
        return {
            'name': group['cn'][0],
            'gid': int(group['gidNumber'][0])
        }

    def parse_all_users(self, groups, raw_users):
        users = []
        for raw_user in raw_users:
            user = None
            if self.should_add_user(raw_user[1], [group[1] for group in groups]):
                user = self.parse_user(raw_user[1], [group[1] for group in groups])
                if user:
                    users.append(user)

        return users

    def parse_user(self, entry, groups):
        user = None
        try:
            if entry.get('sshKey'):
                user = {
                    'name': entry['cn'][0],
                    'username': entry['uid'][0],
                    'uid': int(entry['uidNumber'][0]),
                    'groups': self.get_associated_groups(entry, groups),
                    'homedir': entry['homeDirectory'][0],
                    'shell': entry['loginShell'][0],
                    'ssh_keys': entry.get('sshKey', [])[:]
                }
        except KeyError as e:
            print 'Failed on user {} with key {}'.format(entry, e)

        return user

    def get_associated_groups(self, user, groups):
        group_names = []
        for group in groups:
            if user['uid'][0] in group['memberUid']:
                group_names.append(group['cn'][0])
        return group_names

    def should_add_user(self, user, groups):
        return user.get('sshKey') and self.user_has_any_group(user, groups)

    def user_has_any_group(self, user, groups):
        for group in groups:
            if user['uid'][0] in group['memberUid']:
                return True
        return False

# modifies usernames of the users using the username_map
# if a username is not in the map, then the username is not modified
def map_usernames(users, username_map):
    for user in users:
        username = user['username']
        if username in username_map:
            mapped_username = username_map[username]
            # homedir is optional, username is not
            user['username'] = mapped_username
            if "homedir" in user:
                user['homedir'] = user['homedir'].replace(username, mapped_username)

def main():
    parser = argparse.ArgumentParser(
        description="""
        Dump JumpCloud users and groups into yaml format for hesiod53.


        jumpcloud configfile > myusers.yml
        """
    )
    parser.add_argument(
        'config_file',
        metavar='CONFIG_FILE',
        help='The configuration file to use. See example_config.yml for an example.'
    )

    args = parser.parse_args()
    with open(args.config_file, 'rb') as config_file:
        config = yaml.load(config_file)

    hesiod = {
        'route53_zone': config['route53_zone'],
        'hesiod_domain': config['hesiod_domain'],
        'groups': [],
        'users': []
    }

    jumpcloud_conn = ldap.initialize(config['ldap_server'])
    jumpcloud_conn.simple_bind_s(config['ldap_dn'], config['ldap_password'])

    groups = jumpcloud_conn.search_s(config['ldap_base_search'], ldap.SCOPE_SUBTREE, config['ldap_group_filter'])
    jumpcloud_users = jumpcloud_conn.search_s(config['ldap_base_search'], ldap.SCOPE_SUBTREE, config['ldap_user_filter'])

    parser = Parser(config)
    hesiod['users'] = parser.parse_all_users(groups, jumpcloud_users)
    hesiod['groups'] = parser.parse_all_groups(groups)

    if "username_map" in config:
        map_usernames(hesiod["users"], config["username_map"])

    print yaml.dump(hesiod)

if __name__ == '__main__':
    main()
