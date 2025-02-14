# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
import logging, time
import nuvolaris.openwhisk as openwhisk
import nuvolaris.config as cfg
import nuvolaris.kube as kube
import nuvolaris.util as util

def rollout(kube_name):
    try:
        logging.info(f"*** handling request to rollout {kube_name}")
        kube.rollout(kube_name)
        logging.info(f"*** handled request to rollout {kube_name}")
    except Exception as e:
        logging.error('*** failed to rollout %s: %s' % kube_name,e)

def restart_sts(sts_name):
    try:
        logging.info(f"*** handling request to redeploy {sts_name} using scaledown/scaleup")
        replicas =  1
        current_rep = kube.kubectl("get",sts_name,jsonpath="{.spec.replicas}")
        if current_rep:
            replicas = current_rep[0]
        
        kube.scale_sts(sts_name,0)
        time.sleep(5)
        logging.info(f"scaling {sts_name} to {replicas}")
        kube.scale_sts(sts_name,replicas)
        logging.info(f"*** handling request to redeploy {sts_name} using scaledown/scaleup")
    except Exception as e:
        logging.error('*** failed to scale up/down %s: %s' % sts_name,e)

def redeploy_controller(owner=None):
    try:
        logging.info("*** handling request to redeploy whisk controller")      
        msg = openwhisk.create(owner)
        logging.info(msg)
        rollout("sts/controller")
        logging.info("*** handled request to redeploy whisk controller") 
    except Exception as e:
        logging.error('*** failed to redeploy whisk controller: %s' % e) 

def restart_whisk(owner=None):
    rollout("sts/controller")

def redeploy_whisk(owner=None):
    redeploy_controller(owner)
