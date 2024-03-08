"""CXGenius Search JIRA ingestion script """
from datetime import datetime
import gzip
from io import BytesIO
import json
import logging
from multiprocessing.dummy import Pool
import pprint
import re
import traceback
import zipfile
import requests
from rapidfuzz.distance import Levenshtein
from ingestion.downstream_client import get_client
from conf.config import Configuration
from entities.document import DocumentSchema



class PubDocumentIngestion:
    """Docs ingestion"""
    conf = Configuration()
    logger = logging.getLogger(__name__)
    pp = pprint.PrettyPrinter(indent=4)
    documents = None
    path_vs_hash = {}

    useless_patterns = ["/licensefiles/","/common/", "/apps/settings/", "/content/dam/","/other/Licenses/topics/"]
    version_pattern = re.compile(r"^(\D*\d+[\.-]\d+(?:[\.-]\d+){0,2}\D*|cloud|latest|saas|upgrade)$")

    def get_product_and_version(self, doc):
        ret = {"product": None, "version": None}
        lib_ver = None
        lib_name = None
        url_ver = None
        url_name = None
        if doc.get("library"):
            lib_arr = doc.get("library").split("/")
            if len(lib_arr[0])>0:
                lib_name = lib_arr[0]
            if len(lib_arr[1])>0:
                lib_ver = lib_arr[1]
        url_arr = doc["id"].split("/")
        if len(url_arr)>1:
            for i, part in enumerate(url_arr):
                if self.version_pattern.search(part):
                    if i>0:
                        url_name = url_arr[i-1]
                    url_ver = part
                    break
        ret["product"] = str(doc.get("product") or (lib_name or (url_name or '')))
        ret["version"] = str(doc.get("release") or (lib_ver or (url_ver or '')))
        return ret

    def avoid_redirections(self, doc):
        if doc.get("ptext") and doc.get("ptext").startswith("Redirecting..."):
            return None
        return doc

    def avoid_useless(self, doc):
        for pat in self.useless_patterns:
            if doc.get("id") and doc.get("id").find(pat)>-1:
                return None
        return doc

    def no_empty(self, doc):
        if doc.get("text") and len(doc.get("text"))>10:
            return doc
        return None

    def no_repeated(self, doc):
        if self.options.get("deduplication"):
            for d in self.documents:
                for scrap in d["scraps"]:
                    if scrap["scrap_text"] != doc["text"]:
                        dist = Levenshtein.distance(scrap["scrap_text"], doc["text"], score_cutoff=10)
                        if dist>10:
                            continue
                    # update already-present doc to add versions since text is close enough
                    p_n_v = self.get_product_and_version(doc)
                    if d["product_name"] == p_n_v["product"]:
                        d["crv"].append(p_n_v["version"])
                        return None
        return doc


    cleanup_pipeline = [no_empty, avoid_redirections, avoid_useless, no_repeated]

    def __init__(self, options=None):
        self.options = options

    def download_file(self, url):
        file_data = None
        response = requests.get(url,  timeout=60)
        if response.status_code == 200:
            file_data = response.content
        else:
            self.logger.error('Error downloading data %s', response.text)
        return BytesIO(file_data)

    def pre_process_doc(self, doc):
        for func in self.cleanup_pipeline:
            doc = func(self, doc)
            if doc is None:
                break
        return doc

    def get_meta_from_url(self, url):
        """Transform url into a comma separted list of contextual information"""
        noise = ["documentation", "topics", "other", "shared", "licensefiles"]
        meta = url
        for n in noise:
            meta = meta.replace(f"/{n}/", "/")

        meta = meta.replace("/",", ").replace("-"," ")
        end = len(meta)
        if meta.rfind(".htm")>0:
            end = meta.rindex(".htm")
        return meta[:end]

    def process_doc(self, doc_obj, timestamp):
        created_at = timestamp
        updated_at = created_at
        # do any cleanup or skipping based on our desired data
        doc = self.pre_process_doc(doc_obj)
        if not doc:
            return None
        key = doc["id"]
        scraps = []
        p_n_v = self.get_product_and_version(doc)
        url = str(doc.get("url") or key)
        url_meta = self.get_meta_from_url(url)

        context = f"{ url_meta }"
        title_description = {
            "doc_id": key,
            "type_name": "title_description",
            "scrap_text": context + "\n" + str(doc.get("booktitle") or '') + "\n" + str(doc.get("title") or '') + "\n" + str(doc.get("ptext") or ''),
            "created_at": created_at,
            "updated_at": updated_at
        }
        cdm = {
            "doc_id": key,
            "type_name": "doc_body",
            "scrap_text": context + "\n" + str(doc.get("text") or '') ,
            "created_at": created_at,
            "updated_at": updated_at
        }
        scraps.append(title_description)
        scraps.append(cdm)

        doc_to_post = DocumentSchema().load({
            "id": key,
            "ref_id": str(doc.get("url") or key),
            "type_name": "doc",
            "product_name": [p_n_v["product"]],
            "crv": [p_n_v["version"]],
            "computed_hash": str(self.path_vs_hash.get(doc.get("url") or key) or ''),
            "created_at": created_at,
            "updated_at": updated_at,
            "scraps": scraps
        })
        self.documents.append(doc_to_post)
        return doc_to_post


    def fetch_documents(self):
        """Fetch from the CLDR public docs and return a document array"""

        self.logger.info("FetchDocuments from Cloudera Public Docs")
        manifest = None
        self.path_vs_hash = {}
        self.logger.info("Trying to download document manifest")
        local_manifest_data = self.download_file(self.conf.cloudera_public_docs["manifest_url"])
        with gzip.GzipFile(fileobj=local_manifest_data) as mygzip:
            manifest = mygzip.read()

        if not manifest:
            self.logger.warning("Manifest file not accessible, which means the hashes won't be used for checking if document changed or not")
        else:
            for line in manifest.splitlines():
                line = str(line, 'UTF-8')
                first_space = line.find(' ')
                if first_space == -1:
                    continue
                file_hash = line[0:first_space]
                path = line[first_space+1:]
                if path.endswith('.htm') or path.endswith('.html'):
                    self.path_vs_hash[path] = file_hash
            self.logger.info("Using a hash of %s documents", len(self.path_vs_hash.keys()))

        self.logger.info("Trying to download documents JSON")
        local_json_data = self.download_file(self.conf.cloudera_public_docs["json_url"])
        self.documents = []
        curr_count = 0
        skipped = 0
        timestamp = datetime.now().isoformat()
        processed_docs = []

        with Pool(processes=20) as pool:
            with zipfile.ZipFile(local_json_data) as myzip:
                for name in myzip.namelist():
                    data = myzip.read(name)
                    try:
                        doc_obj = json.loads(data)
                    except json.decoder.JSONDecodeError:
                        self.logger.warning("Could not decode document: %s", name)
                        continue
                    # processing done on multithread pool
                    processed_docs.append(pool.apply_async(self.process_doc, (doc_obj,timestamp)))
            self.logger.debug("Submitted all document to processing pool, now getting the responses")
            for future in processed_docs:
                try:
                    data = future.get()
                    if data:
                        curr_count += 1
                    else:
                        skipped += 1
                    if ( curr_count % 100 ) == 0:
                        self.logger.info("curr %d skipped %d", curr_count, skipped)

                except Exception as exc:
                    self.logger.warning('Worker generated an exception: %s', exc)
                    self.logger.warning("Traceback: %s", traceback.format_exc())

        self.logger.info(
            "Total # of documents to be processed: %d", len(self.documents))
        return self.documents

    def push(self, docs):
        """Pushes docs downstream using client"""
        self.logger.info("Pushing documents downstream")
        client = get_client()
        r = client.store(docs)

        self.logger.info(
            "Successfully pushed a total of %d documents downstream", r["success"])
        self.logger.info("Failed to push a total of %d documents", r["failure"])

    def ingest(self):
        """Fetches docs from the JSON text-only archive and pushes to downstream"""
        docs = self.fetch_documents()
        self.push(docs)

