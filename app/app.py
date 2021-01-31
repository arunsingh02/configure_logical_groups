from flask import Flask, request
import typing as t

from db_utils import MongoDBUtils
from utility import Utility

app = Flask(__name__)

utility_obj = Utility()
mongo_db_utils = MongoDBUtils()


@app.route("/hello")
def say_hello():
    return "Hello MongoDB!"


@app.route("/logical_groups", methods=["GET"])
def get_logical_groups() -> list:
    os = request.args.get("os", "")
    vm = request.args.get("vm", "")
    if os and not vm:
        filter_query = {'os': os}
        return mongo_db_utils.db_find_test(filter_query, projection={})
    elif vm and not os:
        print("os information is important to fetch vm details")
        return []
    elif os and vm:
        filter_query = {'os': os}
        document = mongo_db_utils.db_find_test(filter_query, projection={})
        print("docs: ", document)
    else:
        filter_query = {}
        return mongo_db_utils.db_find_test(filter_query, projection={})


@app.route("/logical_group", methods=["POST"])
def add_new_logical_group() -> t.Union[str, dict]:
    request_json = request.get_json(force=True)
    os = request_json.get("os", "")
    vms = request_json.get("vms", [])
    if not os:
        return "Dependency Error, Please provide new logical group."

    os_uuid = utility_obj.uuid5_converter(os)
    for vm_dict in vms:
        vm_dict["vm_uuid"] = utility_obj.uuid5_converter(f"{os}|{vm_dict['vm']}")
    data = {
        'os': os,
        'os_uuid': os_uuid,
        'vms': vms
    }
    # TODO Call insert in MongoDB
    """
        {
          "os": "Ubuntu", 
          "os_uuid": "2e59ba01-7d42-5a44-a9ef-8d0e740f77ff", 
          "vms": [
            {
              "vm": "vm1", 
              "vm_uuid": "13e95d21-0ba4-56de-ac48-bc7e4a3e6d08"
            }
          ]
        }
    """
    inserted_id = mongo_db_utils.db_insert_test(data)
    return inserted_id


@app.route("/logical_groups", methods=["DELETE"])
def delete_logical_group():
    os = request.args.get("os", "")
    vm = request.args.get("vm", "")
    if os and not vm:
        filter_query = {'os': os}
        return mongo_db_utils.db_delete_test(filter_query)
    elif vm and not os:
        print("os information is important to delete vm details")
        return
    elif os and vm:
        filter_query = {'os': os}
        document = mongo_db_utils.db_delete_test(filter_query)
        print("docs: ", document)
    else:
        filter_query = {}
        return mongo_db_utils.db_delete_test(filter_query)


if __name__ == '__main__':
    app.run(debug=True)
