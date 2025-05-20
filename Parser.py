import yaml
import json

class Parser:

    @staticmethod
    def parse_raml(path):
        with open(path, "r") as f:
            return yaml.safe_load(f)

    @staticmethod
    def build_url_object(base_url, path, query_params=None, path_params=None):
        path_segments = []
        url_variables = []

        for seg in path.strip("/").split("/"):
            if seg.startswith("{") and seg.endswith("}"):
                var_name = seg[1:-1]
                path_segments.append(f"{{{var_name}}}")
                url_variables.append({
                    "key": var_name,
                    "value": "<value>",
                    "description": f"Path parameter {var_name}"
                })
            else:
                path_segments.append(seg)

        url = {
            "raw": f"{base_url}{path}",
            "host": [base_url],
            "path": path_segments
        }

        if url_variables:
            url["variable"] = url_variables

        if query_params:
            url["query"] = []
            for k, v in query_params.items():
                url["query"].append({
                    "key": k,
                    "value": str(v.get("example", {}).get("value", "")) if v.get("example") and "value" in v.get("example") else "",
                    "description": v.get("description",""),
                    "disabled": not v.get("required")
                })

        return url

    @staticmethod
    def build_request_item(method, path, method_data, base_url, uri_params=None):
        headers = [
            {"key": "client_id", "value": "<string>", "description": "Authentication Client ID"},
            {"key": "client_secret", "value": "<string>", "description": "Authentication Client Secret"}
        ]

        if "headers" in method_data:
            for k, v in method_data["headers"].items():
                headers.append({
                    "key": k,
                    "value": "<value>",
                    "description": v.get("description", ""),
                    "disabled": not v.get("required", False)
                })

        query_params = method_data.get("queryParameters")
        url = Parser.build_url_object(base_url, path, query_params, uri_params)

        body = None
        if "body" in method_data:
            mime_types = list(method_data["body"].keys())
            if mime_types:
                mime = mime_types[0]
                example = method_data["body"][mime].get("example") or method_data["body"][mime].get("schema")
                if example:
                    body = {
                        "mode": "raw",
                        "raw": example,
                        "options": {
                            "raw": {"language": "json" if "json" in mime else "text"}
                        }
                    }

        responses = []
        if "responses" in method_data:
            for code, resp in method_data["responses"].items():
                content = None
                headers_resp = []
                if "body" in resp:
                    mime_types = list(resp["body"].keys())
                    if mime_types:
                        mime = mime_types[0]
                        example_obj = resp["body"][mime].get("example")
                        if isinstance(example_obj, dict) and "value" in example_obj:
                            content = json.dumps(example_obj["value"], indent=2)
                        headers_resp.append({"key": "Content-Type", "value": mime})

                responses.append({
                    "name": f"Response {code}",
                    "originalRequest": {
                        "method": method.upper(),
                        "header": headers,
                        "url": url
                    },
                    "status": resp.get("description", ""),
                    "code": int(code) if code.isdigit() else 0,
                    "body": content or "",
                    "header": headers_resp
                })

        return {
            "name": f"{path}",
            "request": {
                "method": method.upper(),
                "header": headers,
                "body": body,
                "url": url,
                "description": method_data.get("description", "")
            },
            "response": responses,
            "protocolProfileBehavior": {"disableBodyPruning": True}
        }

    @staticmethod
    def build_postman_collection(raml, base_url="{{baseUrl}}"):
        def insert_item_in_hierarchy(root, segments, request_item):
            current_level = root
            for seg in segments:
                existing = next((item for item in current_level if item["name"] == seg and "item" in item), None)
                if not existing:
                    new_folder = {"name": seg, "item": []}
                    current_level.append(new_folder)
                    existing = new_folder
                current_level = existing["item"]
            current_level.append(request_item)

        root_items = []

        for path, data in raml.items():
            if not path.startswith("/"):
                continue

            uri_parameters = data.get("uriParameters", {})

            path_segments = [seg for seg in path.strip("/").split("/") if seg]
            path_segments.pop()
            for method, method_data in data.items():
                if method.lower() not in ["get", "post", "put", "delete", "patch", "options", "head"]:
                    continue
                request_item = Parser.build_request_item(method, path, method_data, base_url, uri_params=uri_parameters)
                insert_item_in_hierarchy(root_items, path_segments, request_item)

        return root_items
