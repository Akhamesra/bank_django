import json
import sys

import alb
import ecs
import properties
import r53
import s3
import util
from time import sleep

print("No. of arguments:{}".format(len(sys.argv)))

ecs_obj = ecs.ECS()
alb_obj = alb.ALB()
s3_obj = s3.S3()
r53_obj = r53.R53()

try:
    ENVIRON = sys.argv[1]
    SERVICE_NAME = sys.argv[2]
    IMAGE_VERSION = sys.argv[3]
    
    
except IndexError as e:
    print(e)
    print("Arguments are not sufficient to process further operations.")
    exit(1)

if len(sys.argv) >= 5:
    is_ui_service = eval(sys.argv[4])
else:
    is_ui_service = False

if len(sys.argv) >= 6:
    b2c_mode = sys.argv[5]
else:
    b2c_mode = "disabled"

if len(sys.argv) >= 7:
    DEPLOYMENT_BY = sys.argv[6]
else:
    DEPLOYMENT_BY = "DEFAULT"



if "om-" in SERVICE_NAME.lower() or "pp-" in SERVICE_NAME.lower():
    is_oa_service = True
else:
    is_oa_service = False

# Environment related changes
# Dev Environment
print("UI Service:" + str(is_ui_service))
if ENVIRON == "npd" or ENVIRON == "npq" or ENVIRON == "npu" or ENVIRON == "prd" or ENVIRON == "n2p" or ENVIRON == "bpr" or ENVIRON == "ppd":
    ## For Linux
    print("Environment: " + ENVIRON)
    alb_obj.tg_deregistration_delay = properties.deregistration_delay_tg[ENVIRON]
    r53_obj.r53_domain_name = properties.route53_domain[ENVIRON]
    ecs_obj.ecs_task_role_arn = properties.ecs_task_role_arn[ENVIRON]
    ecs_obj.ecr_image_version = IMAGE_VERSION
    ecs_obj.environment = ENVIRON
    ecs_obj.ecs_service_name = SERVICE_NAME.lower()
    alb_obj.tg_default_port = 80
    alb_obj.tg_health_check_path = "/health"
    scale_in_threshold = properties.scale_in_threshold[ENVIRON]
    scale_out_threshold = properties.scale_out_threshold[ENVIRON]
    ecs_obj.ecs_iam_policy_role_arn = properties.iam_policy_role_arn[ENVIRON]
    # Service details from RDS.
    service_details = util.get_service_details_from_rds(ecs_obj.ecs_service_name, ecs_obj.environment, is_oa_service)
    ecs_obj.cluster_name = service_details['cluster_name']
    alb_obj.alb_name = service_details['alb_name']
    alb_obj.tg_name = service_details['tg_name']
    service_endpoints = service_details['service_endpoints']
    ecs_obj.ecs_service_desired_count = service_details['desired_count']
    ecs_obj.ecs_service_min_count = service_details['min_count']
    ecs_obj.ecs_service_max_count = service_details['max_count']
    ecs_obj.ecs_task_cpu_allocation = service_details['cpu_allocation']
    ecs_obj.ecs_task_memory_allocation = service_details['memory_allocation']
    ecs_obj.service_category = service_details['service_category']
    ecs_obj.latest_ecr_image_path = service_details['latest_ecr_image_path']
    ecs_obj.b2c_mode = b2c_mode
    service_tags = service_details['service_tags']
    formatted_json_service_details = json.dumps(service_details, indent=4, sort_keys=True)
    print(formatted_json_service_details)

else:
    print("Please correct the ENVIRON variable.")
    exit(1)

print("Application Load Balancer: " + alb_obj.alb_name)
alb_details = util.get_alb_details(alb_obj.alb_name)
alb_obj.alb_arn = alb_details['alb_arn']
alb_obj.alb_dns_name = alb_details['alb_dns_name']
alb_obj.vpc_id = alb_details['vpc_id']

if is_oa_service:
    alb_obj.tg_prefix = "tg"
    ecs_obj.cluster_prefix = ""
    ecs_obj.ecs_service_fullname = ecs_obj.environment + "-" + ecs_obj.ecs_service_name
    print("ECS Service fullname: " + ecs_obj.ecs_service_fullname)
    ecs_obj.ecr_repo_name = ecs_obj.environment + "/" + ecs_obj.ecs_service_name
    alb_obj.tg_fullname = (alb_obj.tg_prefix + '-' + properties.tg_environment[
        ecs_obj.environment] + '-' + alb_obj.tg_name)[0:31]
    print("Target Group Name:" + alb_obj.tg_fullname)
else:
    alb_obj.tg_prefix = "albtg"
    ecs_obj.cluster_prefix = properties.cluster_prefix[ecs_obj.environment]
    if ecs_obj.cluster_name == "bureau":
        if ecs_obj.environment == 'npd' or ecs_obj.environment=='npq' or ecs_obj.environment=='npu':
            ecs_obj.cluster_prefix = 'BFL-NPRD-'
    ecs_obj.ecs_service_fullname = ecs_obj.environment + "-" + ecs_obj.cluster_name + "-" + ecs_obj.ecs_service_name
    print("ECS Service Fullname: " + ecs_obj.ecs_service_fullname)
    ecs_obj.ecr_repo_name = ecs_obj.environment + "-" + ecs_obj.cluster_name + "/" + ecs_obj.ecs_service_name
    alb_obj.tg_fullname = (alb_obj.tg_prefix + '-' + properties.tg_environment[
        ecs_obj.environment] + '-' + alb_obj.tg_name)[0:31]
    print("Target Group Name:" + alb_obj.tg_fullname)

if ecs_obj.ecs_service_name == "uiservice" or is_ui_service:
    alb_obj.tg_health_check_path = "/health/index.html"

successful = False

try:
    util.register_task_definition_nprd(ecs_obj)
    successful = True
except Exception as ex:
    print("Failed to register task definition." + str(ex))
    exit(1)

if successful:
    util.tag_task_definition(ecs_obj.ecs_service_fullname,DEPLOYMENT_BY)

try:
    cluster_arn_and_name = util.get_cluster_arn_and_name(ecs_obj.cluster_prefix + ecs_obj.cluster_name)
    ecs_obj.ecs_cluster_arn = cluster_arn_and_name['ecs_cluster_arn']
    ecs_obj.ecs_cluster_name = cluster_arn_and_name['ecs_cluster_name']
    print('Cluster ARN: ' + ecs_obj.ecs_cluster_arn + '\nECS Cluster Name: ' + ecs_obj.ecs_cluster_name)
except Exception as ex:
    print("Could not fetch ECS Cluster name." + str(ex))
    exit(1)

ecs_obj.ecs_task_definition_revision_number = util.get_task_definition_revision(ecs_obj.ecs_service_fullname)
print("Task Definition Revision: " + ecs_obj.ecs_task_definition_revision_number)

alb_obj.tg_arn = util.get_target_group_arn(alb_obj)
print("Target Group ARN: " + alb_obj.tg_arn)

# Add tags and modify attributes (de-registration delay) for target group.
util.add_tg_tags(alb_obj.tg_arn, ecs_obj.ecs_service_name)
util.modify_tg_attributes(alb_obj.tg_arn, alb_obj.tg_deregistration_delay)


print("ALB ARN = " + alb_obj.alb_arn)

alb_obj.alb_listener_arn = util.get_listener_arn(alb_obj.alb_arn, alb_obj.tg_default_port, alb_obj.tg_arn)
print("Listener ARN: " + alb_obj.alb_listener_arn)
print("Proceeding with Listener Rules...")

alb_obj.alb_host_header = ecs_obj.ecs_service_name.replace("-", "") + "." + r53_obj.r53_domain_name
print("Required Service Header on ALB: " + alb_obj.alb_host_header)

# Create ALB listener Rule
util.create_alb_listener_rule(alb_obj.alb_listener_arn, alb_obj.alb_host_header, alb_obj.tg_arn)

# Route53
if ecs_obj.environment == 'prd':
    r53_obj.r53_private_hosted_zone_id = 'ZOP0O9PANRLPN'
else:
    r53_obj.r53_private_hosted_zone_id = util.f(r53_obj.r53_domain_name)

r53_obj.r53_url = ecs_obj.ecs_service_name.replace("-", "") + "." + r53_obj.r53_domain_name
print("Route53 Url: " + r53_obj.r53_url)
resource_record_present = util.get_resource_record(r53_obj.r53_private_hosted_zone_id, r53_obj.r53_url)
if resource_record_present:
    print("Record set present.")
else:
    print("Record set not present. Creating one in the Private Hosted Zone...")
    util.create_r53_record_set(r53_obj.r53_private_hosted_zone_id, r53_obj.r53_url, alb_obj.alb_dns_name)
print("Service Category :", ecs_obj.service_category)
# Nginx
default_nginx_public_template = properties.default_path + ecs_obj.environment + "-default-public-service.txt"
if is_ui_service:
    default_nginx_public_template = properties.default_path + "ui-" + ecs_obj.environment + "-default-public-service.txt"
if ecs_obj.ecs_service_name == "mfapplicationservice":
    default_nginx_public_template = properties.default_path + "mf-" + ecs_obj.environment + "-default-public-service.txt"
if ecs_obj.ecs_service_name == "mfadminservice":
    default_nginx_public_template = properties.default_path + "mfadmin-" + ecs_obj.environment + "-default-public-service.txt"
if ecs_obj.ecs_service_name == "amcapplicationservice":
    default_nginx_public_template = properties.default_path + "amc-" + ecs_obj.environment + "-default-public-service.txt"
if ecs_obj.ecs_service_name == "amcadminservice":
    default_nginx_public_template = properties.default_path + "amcadmin-" + ecs_obj.environment + "-default-public-service.txt"
if ecs_obj.service_category == "php":
    default_nginx_public_template = properties.default_path + "php-" + ecs_obj.environment + "-default-public-service.txt"
    print("default_nginx_public_template Name:", default_nginx_public_template)
if ecs_obj.ecs_service_name == "om-partners-collectionmoduleservice":
    default_nginx_public_template = properties.default_path + "thirdparty-" + ecs_obj.environment + "-default-public-service.txt"
    print("default_nginx_public_template Name:", default_nginx_public_template)
if ecs_obj.ecs_service_name == "om-common-decustomer360service" : 
    default_nginx_public_template = properties.default_path + "omcommondecustomer360service-" + ecs_obj.environment + "-default-public-service.txt"
    print("default_nginx_public_template Name:", default_nginx_public_template)     
if ecs_obj.ecs_service_name != "uiservice":
    util.create_and_upload_nginx_rules(service_endpoints, is_ui_service, ecs_obj.ecs_service_name, ecs_obj.environment,
                                       default_nginx_public_template)

# ECS - Check if service is already present on the cluster
service_in_cluster_present = util.check_service_in_cluster(ecs_obj.ecs_cluster_name, ecs_obj.ecs_service_fullname)

if service_in_cluster_present:
    print("Service " + ecs_obj.ecs_service_fullname + " is present on " + ecs_obj.ecs_cluster_name + ".")
    util.ecs_update_service(ecs_obj.ecs_cluster_name, ecs_obj.ecs_service_fullname, ecs_obj.ecs_service_desired_count,
                            ecs_obj.ecs_task_definition_revision_number, service_tags)
else:
    print("Service " + ecs_obj.ecs_service_fullname + " is not present on " + ecs_obj.ecs_cluster_name + ".")
    util.ecs_create_service(ecs_obj.ecs_cluster_name, ecs_obj.ecs_service_desired_count, ecs_obj.ecs_service_fullname,
                            alb_obj.tg_arn, ecs_obj.ecs_task_definition_revision_number, ecs_obj.environment, service_tags)
    if ecs_obj.environment == "prd" or ecs_obj.environment == "bpr":
        util.ecs_register_scalable_target(ecs_obj.ecs_cluster_name,
                                          ecs_obj.ecs_service_fullname,
                                          ecs_obj.ecs_service_min_count,
                                          ecs_obj.ecs_service_max_count,
                                          ecs_obj.ecs_iam_policy_role_arn)

        # For Scale-out policy and alarm
        ecs_scale_out_policy_arn = util.get_ecs_scale_out_policy(ecs_obj.ecs_cluster_name, ecs_obj.ecs_service_fullname)
        if ecs_scale_out_policy_arn is None:
            ecs_scale_out_policy_arn = util.create_ecs_scale_out_policy(ecs_obj.ecs_cluster_name,
                                                                        ecs_obj.ecs_service_fullname)
        sleep(5)
        print("ecs_scale_out_policy_arn: "+str(ecs_scale_out_policy_arn))
        util.create_high_memory_utilization_metric_cw_alarm(ecs_obj.ecs_cluster_name, ecs_obj.ecs_service_fullname,
                                                            scale_out_threshold, ecs_scale_out_policy_arn)

        # For Scale-in policy and alarm
        ecs_scale_in_policy_arn = util.get_ecs_scale_in_policy(ecs_obj.ecs_cluster_name, ecs_obj.ecs_service_fullname)
        if ecs_scale_in_policy_arn is None:
            ecs_scale_in_policy_arn = util.create_ecs_scale_in_policy(ecs_obj.ecs_cluster_name,
                                                                      ecs_obj.ecs_service_fullname)
        sleep(5)
        print("ecs_scale_in_policy_arn: " + str(ecs_scale_in_policy_arn))
        util.create_low_memory_utilization_metric_cw_alarm(ecs_obj.ecs_cluster_name, ecs_obj.ecs_service_fullname,
                                                           scale_in_threshold, ecs_scale_in_policy_arn)

# update the status and log level for prod deployments
if ecs_obj.environment == 'prd':
    print("Updating Status in database .....")
    util.update_log_level_rds(ecs_obj.ecs_service_name, ecs_obj.environment)


# wait for the service to get stable
print("Sleeping for 60 seconds")
sleep(60)
print("Start waiting for service to stabilize")
util.wait_service_stable(ecs_obj.ecs_cluster_name, ecs_obj.ecs_service_fullname)



