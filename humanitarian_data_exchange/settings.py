import os

CKAN_URL = os.getenv("CKAN_URL", "https://data.humdata.org/")

CKAN_TAG_IDS = [
    "2bfc754f-deee-4e10-a85c-61ad8b8983f3",
    "a0fbb23a-6aad-4ccc-8062-e9ef9f20e5d2",
    "ec53893c-6dba-4656-978b-4a32289ea2eb",
]

CKAN_CAVEATS = 'Information originates from multiple IATI reporting organisations, and has not been centrally vetted or audited for accuracy or consistency.  \r\n\r\nIncludes only those activities from the [IATI Registry](https://iatiregistry.org/) that are included in [D-Portal](http://www.d-portal.org) and have the status "Implementing".\r\n\r\nThe total number of activities may include duplicates, if (for example) a donor and an implementing partner both report the same activity under different IATI identifiers.\r\n\r\nStart and end dates of activities within the dataset will differ.'

CKAN_TITLE_START = "Current IATI aid activities in "

CKAN_RESOURCE_V1_DESCRIPTION_START = "Currently-active IATI activities in "
CKAN_RESOURCE_V1_DESCRIPTION_END = ", in 3W/4W style with HXL hashtags. This dataset has one row for each unique activity/sector/location, so the same IATI activity may occupy multiple rows: use the #activity+id column to count unique activities."
CKAN_RESOURCE_V1_URL_SCHEME = "https"
CKAN_RESOURCE_V1_URL_NETLOC = "proxy.hxlstandard.org"
CKAN_RESOURCE_V1_URL_PATH = "/data/download/{name}.csv"
CKAN_RESOURCE_V1_URL_PARAMS = ""
CKAN_RESOURCE_V1_URL_FRAGMENT = ""
CKAN_RESOURCE_V1_URL_QUERY_PARSED = {
    "filter01": ["cut"],
    "cut-skip-untagged01": ["on"],
    "filter02": ["add"],
    "add-tag02": ["#country+code+v_iso3"],
    # "add-value02": ["UMI"],      This changes per data set
    "add-header02": ["iso3"],
    "filter03": ["add"],
    "add-tag03": ["#country+code+v_iso2"],
    # "add-value03": ["UM"],      This changes per data set
    "add-header03": ["iso2"],
    "filter04": ["add"],
    "add-tag04": ["#activity+url"],
    "add-value04": ["{{#activity+id}}"],
    "add-header04": ["activity_id"],
    "filter05": ["replace"],
    "replace-pattern05": ["^.*aid=(.+)$"],
    "replace-regex05": ["on"],
    "replace-value05": ["\\1"],
    "replace-tags05": ["#activity+id"],
    "tagger-match-all": ["on"],
    "tagger-01-header": ["aid"],
    "tagger-01-tag": ["#activity+id"],
    "tagger-02-header": ["reporting"],
    "tagger-02-tag": ["#org+reporting+name"],
    "tagger-03-header": ["reporting_ref"],
    "tagger-03-tag": ["#org+reporting+id"],
    "tagger-04-header": ["funder_ref"],
    "tagger-04-tag": ["#org+funder+id"],
    "tagger-05-header": ["title"],
    "tagger-05-tag": ["#activity+title"],
    "tagger-07-header": ["status_code"],
    "tagger-07-tag": ["#status"],
    "tagger-08-header": ["day_start"],
    "tagger-08-tag": ["#date+start"],
    "tagger-09-header": ["day_end"],
    "tagger-09-tag": ["#date+end"],
    "tagger-11-header": ["description"],
    "tagger-11-tag": ["#description"],
    "tagger-12-header": ["commitment"],
    "tagger-12-tag": ["#value+committed+usd"],
    "tagger-13-header": ["spend"],
    "tagger-13-tag": ["#value+spent+usd"],
    "tagger-14-header": ["commitment_eur"],
    "tagger-14-tag": ["#value+committed+eur"],
    "tagger-15-header": ["spend_eur"],
    "tagger-15-tag": ["#value+spent+eur"],
    "tagger-16-header": ["commitment_gbp"],
    "tagger-16-tag": ["#value+committed+gbp"],
    "tagger-17-header": ["spend_gbp"],
    "tagger-17-tag": ["#value+spent+gbp"],
    "tagger-18-header": ["commitment_cad"],
    "tagger-18-tag": ["#value+committed+cad"],
    "tagger-19-header": ["spend_cad"],
    "tagger-19-tag": ["#value+spent+cad"],
    "tagger-21-header": ["country_code"],
    "tagger-21-tag": ["#country+name"],
    "tagger-22-header": ["country_percent"],
    "tagger-22-tag": ["#indicator+country_allocation+pct"],
    "tagger-23-header": ["sector_group"],
    "tagger-23-tag": ["#sector"],
    "tagger-24-header": ["sector_code"],
    "tagger-24-tag": ["#subsector"],
    "tagger-25-header": ["sector_percent"],
    "tagger-25-tag": ["#indicator+subsector_allocation+pct"],
    "tagger-26-header": ["location_code"],
    "tagger-26-tag": ["#loc+code"],
    "tagger-29-header": ["location_name"],
    "tagger-29-tag": ["#loc+name"],
    "tagger-30-header": ["location_longitude"],
    "tagger-30-tag": ["#geo+lon"],
    "tagger-31-header": ["location_latitude"],
    "tagger-31-tag": ["#geo+lat"],
    "tagger-32-header": ["location_precision"],
    "tagger-32-tag": ["#geo+precision+code"],
    "tagger-33-header": ["location_percent"],
    "tagger-33-tag": ["#indicator+location_allocation+pct"],
    "header-row": ["1"],
    # "url": "...",      This changes per data set
}
CKAN_RESOURCE_V1_DPORTAL_URL = "http://d-portal.org/dquery?form=csv&human=1&sql=select * from act left join country using (aid) left join sector using (aid) left join location using (aid) where status_code%3D2 and country.country_code%3D'{country_iso_2char}' and day_end >%3D floor(extract(epoch from now())%2F(60*60*24)) order by day_start%2C day_end%2C reporting&_gl=1*avmz6m*_ga*MTQ0Nzk3MzM5OS4xNjY3MjI2ODk2*_ga_E60ZNX2F68*MTY4MTc0NjM3OC43OS4xLjE2ODE3NDYzODkuNDkuMC4w"

DATASETS_DIRECTORY = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "..", "datasets"
)
