# hesiod53-jumpcloud

Create a hesiod53 configuration file populated via jumpcloud. See the
example_configuration.yml

Only dumps users who have an SSH key.

# Installation

This library depends on python-ldap which requires installing some system libraries

* libldap2-dev
* libsasl2-dev
* libssl-dev

Now you can install this library

`pip install hesiod53-jumpcloud`

# Usage

`jumpcloud myconfig.yml > myusers.yml`
