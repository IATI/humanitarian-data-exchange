import json
import os.path

import requests
import settings
import yaml
import urllib.parse


def pull_and_check_ckan():
    # Setup
    r = requests.get(
        settings.CKAN_URL
        + "/api/3/action/package_search?fq=organization:iati&rows=1000"
    )
    r.raise_for_status()
    data = r.json()
    problems = []
    # Loop
    for ckan_dataset in data.get("result").get("results"):
        out_data, dataset_problems = _process_ckan_dataset(ckan_dataset)
        with open(
            os.path.join(
                settings.DATASETS_DIRECTORY, ckan_dataset.get("name") + ".yaml"
            ),
            "w",
        ) as fp:
            yaml.dump(out_data, fp, indent=4, sort_keys=True)
        for dataset_problem in dataset_problems:
            problems.append(
                "Resource " + ckan_dataset.get("name") + ": " + dataset_problem
            )
    # return
    return problems


def _process_ckan_dataset(ckan_dataset):
    problems = []
    # Handy Print Debugging
    # print("------------------------------------------------")
    # print(json.dumps(ckan_dataset, indent=2))
    # Check data
    if ckan_dataset.get("caveats") != settings.CKAN_CAVEATS:
        problems.append("wrong caveat")
    tag_ids = [x.get("id") for x in ckan_dataset["tags"]]
    for tag_id in settings.CKAN_TAG_IDS:
        if tag_id not in tag_ids:
            problems.append("does not have the expected tag " + tag_id)
    # Make out data
    out_data = {
        "id": ckan_dataset.get("id"),
        "country": {
            "iso_2char": None,
            "iso_3char": None,
            "title": ckan_dataset.get("title"),
        },
        "resources": [],
        "tags": [],
    }
    if out_data["country"]["title"].startswith(settings.CKAN_TITLE_START):
        out_data["country"]["title"] = out_data["country"]["title"][
            len(settings.CKAN_TITLE_START) :
        ]
    else:
        problems.append("starts with a different title")
    if len(ckan_dataset.get("resources")) != 1:
        problems.append("Does not have exactly 1 resource")
    for ckan_resource in ckan_dataset.get("resources"):
        description = ckan_resource.get("description")
        if description.startswith(settings.CKAN_RESOURCE_V1_DESCRIPTION_START):
            description = description[
                len(settings.CKAN_RESOURCE_V1_DESCRIPTION_START) :
            ]
        else:
            problems.append("resource starts with a different description")
        if description.endswith(settings.CKAN_RESOURCE_V1_DESCRIPTION_END):
            description = description[: -len(settings.CKAN_RESOURCE_V1_DESCRIPTION_END)]
        else:
            problems.append("resource ends with a different description")
        if description != out_data["country"]["title"]:
            problems.append(
                "resource description country does not match title: " + description
            )
        if ckan_resource.get("url") != ckan_resource.get("download_url"):
            problems.append("resource has different url and download_url")
        if ckan_resource.get("url") != ckan_resource.get("hdx_rel_url"):
            problems.append("resource has different url and hdx_rel_url")
        url_bits = urllib.parse.urlparse(ckan_resource.get("url"))
        url_query_bits = urllib.parse.parse_qs(url_bits.query)
        out_data["country"]["iso_2char"] = url_query_bits.get("add-value03", []).pop()
        out_data["country"]["iso_3char"] = url_query_bits.get("add-value02", []).pop()
        if url_bits.scheme != settings.CKAN_RESOURCE_V1_URL_SCHEME:
            problems.append("resource url has wrong scheme " + url_bits.scheme)
        if url_bits.netloc != settings.CKAN_RESOURCE_V1_URL_NETLOC:
            problems.append("resource url has wrong netloc " + url_bits.netloc)
        if url_bits.path != settings.CKAN_RESOURCE_V1_URL_PATH.format(
            name=ckan_dataset["name"]
        ):
            problems.append("resource url has wrong path " + url_bits.path)
        if url_bits.params != settings.CKAN_RESOURCE_V1_URL_PARAMS:
            problems.append("resource url has wrong params " + url_bits.path)
        if url_bits.fragment != settings.CKAN_RESOURCE_V1_URL_FRAGMENT:
            problems.append("resource url has wrong fragment " + url_bits.fragment)
        for key, value in settings.CKAN_RESOURCE_V1_URL_QUERY_PARSED.items():
            if url_query_bits.get(key) != value:
                problems.append(
                    "resource url has wrong query bit "
                    + key
                    + " Value is "
                    + str(value)
                )
        dportal_url = url_query_bits.get("url", []).pop()
        if dportal_url != settings.CKAN_RESOURCE_V1_DPORTAL_URL.format(
            country_iso_2char=out_data["country"]["iso_2char"]
        ):
            problems.append("Resource D-Portal URL is wrong!")
        out_resource = {"id": ckan_resource["id"]}
        out_data["resources"].append(out_resource)
    for ckan_tag in ckan_dataset.get("tags"):
        if ckan_tag.get("id") not in settings.CKAN_TAG_IDS:
            out_tag = {"id": ckan_tag.get("id"), "name": ckan_tag.get("name")}
            out_data["tags"].append(out_tag)
    ckan_dataset_solr_additions = json.loads(ckan_dataset.get("solr_additions", "{}"))
    # Check data (after processing has been done)
    if ckan_dataset_solr_additions.get("countries") != [out_data["country"]["title"]]:
        problems.append(
            "has a different solr_additions/countries! "
            + str(ckan_dataset_solr_additions.get("countries"))
        )
    # Return
    return out_data, problems


if __name__ == "__main__":
    problems = pull_and_check_ckan()
    if problems:
        print("PROBLEMS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        for problem in problems:
            print(problem)
