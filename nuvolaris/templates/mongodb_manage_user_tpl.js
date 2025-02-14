/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

conn = Mongo("mongodb://{{mongo_admin_user}}:{{mongo_admin_password}}@127.0.0.1:27017")
db = conn.getDB('admin')
db = db.getSiblingDB('{{database}}');

{% if mode == 'create'%}
db.createUser({
    user: "{{subject}}",
    pwd: "{{auth}}",
    roles: [
        {role: "readWrite", db: "{{subject}}"}
    ]
});
db.nuv_test_collection.insertOne({"message":"Welcome to nuvolaris!"});
{% endif %}

{% if mode == 'delete'%}
db.dropUser("{{subject}}", {w: "majority", wtimeout: 4000});
db.dropDatabase();
{% endif %}