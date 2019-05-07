#!/usr/bin/env python
# vim: sw=2 ts=2
# Initial author: Patrice LACHANCE, ITisOpen.net
# Credits: highly inspired by openshift-ansible-contrib project.

import click
import os
import sys

@click.command()

### Global option
@click.option('--task', help='Which task would you like to trigger?')
@click.option('--refresh-ansible-cache', default=True, help='Refresh Ansible cache before running the playbooks?',
              show_default=True)

### AWS options
@click.option('--create-infra', default='yes', help='Should this script provision infrastructure?',
              show_default=True)
@click.option('--stack-name', default='OIL', help='Cloudformation stack name. Must be unique',
              show_default=True)
@click.option('--region', default='eu-west-1', help='EC2 region',
              show_default=True)
@click.option('--public-dns-domain', help='Route53 Public DNS domain, it will be created if it does not exist, but will not be deleted at teardown',
              show_default=True)
@click.option('--private-dns-domain', help='Route53 Private DNS domain, it will be created',
              show_default=True)
@click.option('--ciap-nb-subnets', default='2', help='Number of Hosting, Browsing and VPN subnets (1 of each per region)',
              show_default=True)
@click.option('--admin-nb-subnets', default='2', help='Number of Admin subnets (1 per region)',
              show_default=True)
@click.option('--tech-nb-subnets', default='2', help='Number of Tech subnets (1 per region)',
              show_default=True)
@click.option('--project-ocp-nb-subnets', default='3', help='Number of private subnets for OCP (1 per region)',
              show_default=True)
@click.option('--keypair', help='EC2 keypair name',
              show_default=True)
@click.option('--create-key', default='no', help='Create SSH keypair',
              show_default=True)
@click.option('--key-path', default='/dev/null', help='Create SSH keypair',
              show_default=True)
@click.option('--ciap-cidr', default='10.0.0.0/20', help='Specify a CIDR for VPC CIAP',
              show_default=True)
@click.option('--ciap-hosting-subnet1-cidr', default='10.0.0.0/24', help='Specify a CIDR for VPC CIAP Hosting subnet - AZ1',
              show_default=True)
@click.option('--ciap-hosting-subnet2-cidr', default='10.0.1.0/24', help='Specify a CIDR for VPC CIAP Hosting subnet - AZ2',
              show_default=True)
# Reserving default CIDR 10.0.2.0/24 and 10.0.3.0/24 for future use - expansion to other AZs
@click.option('--ciap-browsing-subnet1-cidr', default='10.0.4.0/24', help='Specify a CIDR for VPC CIAP Browsing subnet - AZ1',
              show_default=True)
@click.option('--ciap-browsing-subnet2-cidr', default='10.0.5.0/24', help='Specify a CIDR for VPC CIAP Browsing subnet - AZ2',
              show_default=True)
# Reserving default CIDR 10.0.6.0/24 and 10.0.7.0/24 for future use - expansion to other AZs
@click.option('--ciap-vpn-subnet1-cidr', default='10.0.8.0/24', help='Specify a CIDR for VPC CIAP VPN Concentrator subnet - AZ1',
              show_default=True)
@click.option('--ciap-vpn-subnet2-cidr', default='10.0.9.0/24', help='Specify a CIDR for VPC CIAP VPN Concentrator subnet - AZ2',
              show_default=True)
@click.option('--admin-cidr', default='10.0.16.0/20', help='Specify a CIDR for VPC Admin',
              show_default=True)
@click.option('--admin-subnet1-cidr', default='10.0.16.0/24', help='Specify a CIDR for VPC Admin subnet 1',
              show_default=True)
@click.option('--admin-subnet2-cidr', default='10.0.17.0/24', help='Specify a CIDR for VPC Admin subnet 2',
              show_default=True)
@click.option('--tech-cidr', default='10.0.32.0/20', help='Specify a CIDR for VPC Tech',
              show_default=True)
@click.option('--tech-subnet1-cidr', default='10.0.32.0/24', help='Specify a CIDR for VPC Tech subnet 1',
              show_default=True)
@click.option('--tech-subnet2-cidr', default='10.0.33.0/24', help='Specify a CIDR for VPC Tech subnet 2',
              show_default=True)
@click.option('--project-cidr', default='10.0.128.0/17', help='Specify a CIDR for VPC Project',
              show_default=True)
@click.option('--project-subnet-ocp-pub1-cidr', default='10.0.128.0/24', help='Specify a CIDR for VPC Project subnet - OCP Pub 1',
              show_default=True)
@click.option('--project-subnet-ocp-pub2-cidr', default='10.0.129.0/24', help='Specify a CIDR for VPC Project subnet - OCP Pub 2',
              show_default=True)
@click.option('--project-subnet-ocp-pub3-cidr', default='10.0.130.0/24', help='Specify a CIDR for VPC Project subnet - OCP Pub 3',
              show_default=True)
# Reserving default CIDR 10.0.131.0/24 for future use - expansion to other AZs
@click.option('--project-subnet-ocp-priv1-cidr', default='10.0.132.0/24', help='Specify a CIDR for VPC Project subnet - OCP Priv 1',
              show_default=True)
@click.option('--project-subnet-ocp-priv2-cidr', default='10.0.133.0/24', help='Specify a CIDR for VPC Project subnet - OCP Priv 2',
              show_default=True)
@click.option('--project-subnet-ocp-priv3-cidr', default='10.0.134.0/24', help='Specify a CIDR for VPC Project subnet - OCP Priv 3',
              show_default=True)
# Reserving default CIDR 10.0.135.0/24 for future use - expansion to other AZs
@click.option('--allowed-ssh-cidr', default='0.0.0.0/0', help='Specify the CIDR allowed SSH access to NAT instances',
              show_default=True)
@click.option('--s3-bucket-prefix', help='S3 Bucket Prefix used to create buckets in templates')
@click.option('--s3-username', help='S3 User to access bucket')

### WAF options
@click.option('--waf-instance-type', default='t3.small', help='WAF EC2 instance type',
              show_default=True)

### Squid options
@click.option('--nat-instance-type', default='t3.small', help='NAT EC2 instance type',
              show_default=True)
@click.option('--squid-port', default='3128', help='Specify the Squid network port',
              show_default=True)
@click.option('--squid-dist', default='zip', help='Specify the Squid distribution to install (zip/os)',
              show_default=True)

### VPN options
@click.option('--vpn-instance-type', default='t3.small', help='VPN EC2 instance type',
              show_default=True)

### General options
@click.option('--no-confirm', is_flag=True,
              help='Skip confirmation prompt')
@click.help_option('--help', '-h')
@click.option('-v', '--verbose', count=True)



### Main logic
def launch_oil_env(task=None,
                   create_infra=None,
                   refresh_ansible_cache=None,
                   region=None,
                   stack_name=None,
                   public_dns_domain=None,
                   private_dns_domain=None,
                   ciap_nb_subnets=None,
                   admin_nb_subnets=None,
                   tech_nb_subnets=None,
                   project_ocp_nb_subnets=None,
                   keypair=None,
                   create_key=None,
                   key_path=None,
                   ciap_cidr=None,
                   ciap_hosting_subnet1_cidr=None,
                   ciap_hosting_subnet2_cidr=None,
                   ciap_browsing_subnet1_cidr=None,
                   ciap_browsing_subnet2_cidr=None,
                   ciap_vpn_subnet1_cidr=None,
                   ciap_vpn_subnet2_cidr=None,
                   admin_cidr=None,
                   admin_subnet1_cidr=None,
                   admin_subnet2_cidr=None,
                   tech_cidr=None,
                   tech_subnet1_cidr=None,
                   tech_subnet2_cidr=None,
                   project_cidr=None,
                   project_subnet_ocp_pub1_cidr=None,
                   project_subnet_ocp_pub2_cidr=None,
                   project_subnet_ocp_pub3_cidr=None,
                   project_subnet_ocp_priv1_cidr=None,
                   project_subnet_ocp_priv2_cidr=None,
                   project_subnet_ocp_priv3_cidr=None,
                   allowed_ssh_cidr=None,
                   waf_instance_type=None,
                   nat_instance_type=None,
                   vpn_instance_type=None,
                   s3_bucket_prefix=None,
                   s3_username=None,
                   squid_port=None,
                   squid_dist=None,
                   no_confirm=False,
                   verbose=0):


  # Checking parameters
  if task is None:
    click.echo("'\nERROR: no task provided, must use '--task=launch' or '--task=teardown'\n")
    sys.exit(1)
   
  if task == 'teardown':
    click.echo('\tregion: %s' % region)
    click.echo('\tstack_name: %s' % stack_name)

    if not no_confirm:
      click.confirm('Continue using these values?', abort=True)

    playbooks = ['playbooks/infrastructure.yaml']
    for playbook in playbooks:
      command='ansible-playbook -i inventory/aws/hosts -e \'create_key=no create_infra=tear teardown_infra=yes \
                 task=%s \
                 region=%s \
                 public_dns_domain=%s \
                 private_dns_domain=%s \
                 stack_name=%s \' %s' % (task,
                                         region,
                                         public_dns_domain,
                                         private_dns_domain,
                                         stack_name,
                                         playbook)

    if verbose > 0:
      command += " -" + "".join(['v']*verbose)
      click.echo('We are running: %s' % command)

    status = os.system(command)
    if os.WIFEXITED(status) and os.WEXITSTATUS(status) != 0:
      sys.exit(os.WEXITSTATUS(status))
    sys.exit(os.WEXITSTATUS(status))



  # Current release only supports greenfield deployment
  if create_infra is None:
    click.echo('Greenfield only deployment supported at this time, must use --create-infra=yes')
    sys.exit(1)
   
  # Need to prompt for the R53 zone:
  if public_dns_domain is None:
    public_dns_domain = click.prompt('Public Hosted DNS zone for accessing the environment')

  if private_dns_domain is None:
    private_dns_domain = click.prompt('Private Hosted DNS zone for accessing the environment')

  if s3_bucket_prefix is None:
    s3_bucket_prefix = stack_name

  if s3_username is None:
    s3_username = stack_name + '-s3-openshift-user'

  ciap_nb_subnets = int(ciap_nb_subnets)
  admin_nb_subnets = int(admin_nb_subnets)
  tech_nb_subnets = int(tech_nb_subnets)
  project_ocp_nb_subnets = int(project_ocp_nb_subnets)

  # Create ssh key pair in AWS if none is specified
  if create_key in 'yes' and key_path in 'no':
    key_path = click.prompt('Specify path for ssh public key')
    keypair = click.prompt('Specify a name for the keypair')

  # If no keypair is not specified fail:
  if keypair is None and create_key in 'no':
    click.echo('A SSH keypair must be specified or created')
    sys.exit(1)

  # Name the keypair if a path is defined
  if keypair is None and create_key in 'yes':
    keypair = click.prompt('Specify a name for the keypair')

  # Fail on missing key_path
  if key_path in '/dev/null' and create_key in 'yes':
    key_path = click.prompt('Specify the location of the public key')

  # Checking required parameters
  if keypair is None :
    keypair = click.prompt('Specify a name for the keypair')

 # Name the keypair if a path is defined
  if keypair is None and create_key in 'yes':
    keypair = click.prompt('Specify a name for the keypair')

  # Display information to the user about their choices
  click.echo('Configured values:')
  click.echo('\tcreate_infra: %s' % create_infra)
  click.echo('\tstack_name: %s' % stack_name)
  click.echo('\tregion: %s' % region)
  click.echo('\tpublic_dns_domain: %s' % public_dns_domain)
  click.echo('\tprivate_dns_domain: %s' % private_dns_domain)
  click.echo('\tciap_nb_subnets: %s' % ciap_nb_subnets)
  click.echo('\tadmin_nb_subnets: %s' % admin_nb_subnets)
  click.echo('\ttech_nb_subnets: %s' % tech_nb_subnets)
  click.echo('\tproject_ocp_nb_subnets: %s' % project_ocp_nb_subnets)
  click.echo('\tkeypair: %s' % keypair)
  click.echo('\tcreate_key: %s' % create_key)
  click.echo('\tkey_path: %s' % key_path)
  click.echo('\tciap_cidr: %s' % ciap_cidr)
  click.echo('\tciap_hosting_subnet1_cidr: %s' % ciap_hosting_subnet1_cidr)
  click.echo('\tciap_hosting_subnet2_cidr: %s' % ciap_hosting_subnet2_cidr)
  click.echo('\tciap_browsing_subnet1_cidr: %s' % ciap_browsing_subnet1_cidr)
  click.echo('\tciap_browsing_subnet2_cidr: %s' % ciap_browsing_subnet2_cidr)
  click.echo('\tciap_vpn_subnet1_cidr: %s' % ciap_vpn_subnet1_cidr)
  click.echo('\tciap_vpn_subnet2_cidr: %s' % ciap_vpn_subnet2_cidr)
  click.echo('\tadmin_cidr: %s' % admin_cidr)
  click.echo('\tadmin_subnet1_cidr: %s' % admin_subnet1_cidr)
  click.echo('\tadmin_subnet2_cidr: %s' % admin_subnet2_cidr)
  click.echo('\ttech_cidr: %s' % tech_cidr)
  click.echo('\ttech_subnet1_cidr: %s' % tech_subnet1_cidr)
  click.echo('\ttech_subnet2_cidr: %s' % tech_subnet2_cidr)
  click.echo('\tproject_cidr: %s' % project_cidr)
  click.echo('\tproject_subnet_ocp_pub1_cidr: %s' % project_subnet_ocp_pub1_cidr)
  click.echo('\tproject_subnet_ocp_pub2_cidr: %s' % project_subnet_ocp_pub2_cidr)
  click.echo('\tproject_subnet_ocp_pub3_cidr: %s' % project_subnet_ocp_pub3_cidr)
  click.echo('\tproject_subnet_ocp_priv1_cidr: %s' % project_subnet_ocp_priv1_cidr)
  click.echo('\tproject_subnet_ocp_priv2_cidr: %s' % project_subnet_ocp_priv2_cidr)
  click.echo('\tproject_subnet_ocp_priv3_cidr: %s' % project_subnet_ocp_priv3_cidr)
  click.echo('\tallowed_ssh_cidr: %s' % allowed_ssh_cidr)
  click.echo('\twaf_instance_type: %s' % waf_instance_type)
  click.echo('\tnat_instance_type: %s' % nat_instance_type)
  click.echo('\tvpn_instance_type: %s' % vpn_instance_type)
  click.echo('\ts3_bucket_prefix: %s' % s3_bucket_prefix)
  click.echo('\ts3_username: %s' % s3_username)
  click.echo('\tsquid_port: %s' % squid_port)
  click.echo('\tsquid_dist: %s' % squid_dist)
  click.echo("")

  if not no_confirm:
    click.confirm('Continue using these values?', abort=True)


  #playbooks = ['playbooks/infrastructure.yaml', 'playbooks/openshift-install.yaml']
  playbooks = ['playbooks/account-setup.yaml', 'playbooks/infrastructure.yaml']

  for playbook in playbooks:

    # hide cache output unless in verbose mode
    devnull='> /dev/null'

    if verbose > 0:
      devnull=''

    # refresh the inventory cache to prevent stale hosts from
    # interferring with re-running
    if refresh_ansible_cache == True:
      command='inventory/aws/hosts/ec2.py --refresh-cache %s' % (devnull)
      os.system(command)

      # remove any cached facts to prevent stale data during a re-run
      command='rm -rf .ansible/cached_facts'
      os.system(command)

    command='ansible-playbook -i inventory/aws/hosts -e \'create_infra=%s \
    task=%s \
    region=%s \
    stack_name=%s \
    public_dns_domain=%s \
    private_dns_domain=%s \
    ciap_nb_subnets=%s \
    admin_nb_subnets=%s \
    tech_nb_subnets=%s \
    project_ocp_nb_subnets=%s \
    keypair=%s \
    create_key=%s \
    key_path=%s \
    ciap_cidr=%s \
    ciap_hosting_subnet1_cidr=%s \
    ciap_hosting_subnet2_cidr=%s \
    ciap_browsing_subnet1_cidr=%s \
    ciap_browsing_subnet2_cidr=%s \
    ciap_vpn_subnet1_cidr=%s \
    ciap_vpn_subnet2_cidr=%s \
    admin_cidr=%s \
    admin_subnet1_cidr=%s \
    admin_subnet2_cidr=%s \
    tech_cidr=%s \
    tech_subnet1_cidr=%s \
    tech_subnet2_cidr=%s \
    project_cidr=%s \
    project_subnet_ocp_pub1_cidr=%s \
    project_subnet_ocp_pub2_cidr=%s \
    project_subnet_ocp_pub3_cidr=%s \
    project_subnet_ocp_priv1_cidr=%s \
    project_subnet_ocp_priv2_cidr=%s \
    project_subnet_ocp_priv3_cidr=%s \
    allowed_ssh_cidr=%s \
    waf_instance_type=%s \
    nat_instance_type=%s \
    vpn_instance_type=%s \
    s3_bucket_prefix=%s \
    s3_username=%s \
    squid_port=%s \
    squid_dist=%s \' %s' % (create_infra,
														task,
														region,
														stack_name,
														public_dns_domain,
														private_dns_domain,
														int(ciap_nb_subnets),
														int(admin_nb_subnets),
														int(tech_nb_subnets),
														int(project_ocp_nb_subnets),
														keypair,
														create_key,
														key_path,
														ciap_cidr,
														ciap_hosting_subnet1_cidr,
														ciap_hosting_subnet2_cidr,
														ciap_browsing_subnet1_cidr,
														ciap_browsing_subnet2_cidr,
														ciap_vpn_subnet1_cidr,
														ciap_vpn_subnet2_cidr,
														admin_cidr,
														admin_subnet1_cidr,
														admin_subnet2_cidr,
														tech_cidr,
														tech_subnet1_cidr,
														tech_subnet2_cidr,
														project_cidr,
														project_subnet_ocp_pub1_cidr,
														project_subnet_ocp_pub2_cidr,
														project_subnet_ocp_pub3_cidr,
														project_subnet_ocp_priv1_cidr,
														project_subnet_ocp_priv2_cidr,
														project_subnet_ocp_priv3_cidr,
														allowed_ssh_cidr,
														waf_instance_type,
														nat_instance_type,
														vpn_instance_type,
                            s3_bucket_prefix,
                            s3_username,
														squid_port,
														squid_dist,
														playbook)


    if verbose > 0:
      command += " -" + "".join(['v']*verbose)
      click.echo('We are running: %s' % command)

    status = os.system(command)
    if os.WIFEXITED(status) and os.WEXITSTATUS(status) != 0:
      sys.exit(os.WEXITSTATUS(status))


### Run program
if __name__ == '__main__':
  # check for AWS access info
  if os.getenv('AWS_ACCESS_KEY_ID') is None or os.getenv('AWS_SECRET_ACCESS_KEY') is None:
    print 'ERROR: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY **MUST** be exported as environment variables.'
    sys.exit(1)

  launch_oil_env(auto_envvar_prefix='ITON_CIAP')

