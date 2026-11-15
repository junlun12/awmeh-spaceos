"""
NASA Space Life Sciences Data Fetcher (Tailored for 2026 Space Apps Challenge)
Project: Autonomous Astronaut Health & Hidden Neuro-Affective Monitoring Software (AWMEH)

Dual-Core Acquisition Modules:
1. Module A: Neuro-Affective & Behavioral Resilience (AWMEH Engine)
   - Sleep Architecture, Actigraphy, Circadian Disruption
   - Cognitive Fatigue, Psychomotor Vigilance (PVT), Stress & Neuro-inflammation
   - Isolation & Confinement Analogs (HERA, Closed Habitats)
2. Module B: Spaceflight Physiological & Environmental Baselines
   - Space Radiation Exposure & Biomarkers
   - Cardiovascular & Hemodynamic Deconditioning
   - Musculoskeletal Microgravity Adaptation (Bone & Muscle Loss)
"""

import os
import sys
import json
import time
import argparse
from urllib.parse import quote, urljoin
import requests

# Categorized Research Targets specifically aligned with the AWMEH architecture
TARGET_MODULES = {
    "Neuro-Affective & Behavioral Health": [
        "sleep",
        "circadian",
        "cognitive",
        "behavioral",
        "HERA",
        "isolation",
        "brain"
    ],
    "Physiological & Environmental Hazards": [
        "radiation",
        "cardiovascular",
        "bone loss",
        "muscle atrophy",
        "immune",
        "hemodynamic"
    ]
}

OSDR_BASE = "https://osdr.nasa.gov"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NASA-SpaceApps-AWMEH/2026",
    "Accept": "application/json, text/plain, */*",
}


class NASASpaceHealthDataFetcher:
    def __init__(self, output_dir="./nasa_life_sciences_data", max_studies_per_topic=2):
        self.output_dir = os.path.abspath(output_dir)
        self.files_dir = os.path.join(self.output_dir, "files")
        self.max_per_topic = max_studies_per_topic
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.manifest = []

        os.makedirs(self.files_dir, exist_ok=True)

    def log(self, message):
        print(f"[{time.strftime('%H:%M:%S')}] {message}")

    def search_osdr(self, query):
        """Search NASA OSDR for studies matching specific query terms."""
        studies = []
        try:
            url = f"{OSDR_BASE}/osdr/data/search?term={quote(query)}&size={self.max_per_topic * 2}"
            resp = self.session.get(url, timeout=15)
            if resp.status_code == 200:
                hits = resp.json().get("hits", {}).get("hits", [])
                for h in hits:
                    source = h.get("_source", {})
                    acc = source.get("Accession") or source.get("Study Identifier")
                    if acc and acc.startswith("OSD-"):
                        num_id = acc.replace("OSD-", "").strip()
                        studies.append({
                            "accession": acc,
                            "numeric_id": num_id,
                            "matched_term": query,
                            "raw_source": source
                        })
                        if len(studies) >= self.max_per_topic:
                            break
        except Exception as e:
            self.log(f"⚠️ Search warning for '{query}': {e}")
        return studies

    def fetch_metadata(self, num_id):
        """Fetch descriptive title, mission context, and assay info."""
        url = f"{OSDR_BASE}/osdr/data/osd/meta/{num_id}"
        meta = {"title": None, "description": "", "mission": "Spaceflight / Ground Analog", "factors": [], "organisms": []}
        try:
            r = self.session.get(url, timeout=12)
            if r.status_code == 200:
                data = r.json()
                study_dict = data.get("study", {})
                for k, v in study_dict.items():
                    s_list = v.get("studies", [])
                    if s_list:
                        s0 = s_list[0]
                        meta["title"] = s0.get("title") or k
                        meta["description"] = s0.get("description", "")
                        if isinstance(s0.get("mission"), dict):
                            meta["mission"] = s0.get("mission", {}).get("name", meta["mission"])
                        elif s0.get("mission"):
                            meta["mission"] = str(s0.get("mission"))
                        meta["factors"] = [f.get("factorName") for f in s0.get("factors", []) if isinstance(f, dict)]
                        meta["organisms"] = [o.get("organismName") for o in s0.get("organisms", []) if isinstance(o, dict)]
                    else:
                        meta["title"] = v.get("title") or k
                        meta["description"] = v.get("description", "")
                    break
        except Exception as e:
            self.log(f"⚠️ Metadata retrieval warning for {num_id}: {e}")
        return meta

    def fetch_study_files(self, num_id):
        """Retrieve open data files list for a study."""
        url = f"{OSDR_BASE}/osdr/data/osd/files/{num_id}"
        target_files = []
        try:
            r = self.session.get(url, timeout=12)
            if r.status_code == 200:
                studies = r.json().get("studies", {})
                for s_key, s_val in studies.items():
                    for f in s_val.get("study_files", []):
                        fname = f.get("file_name", "")
                        rem_url = f.get("remote_url", "")
                        fsize = f.get("file_size", 0)

                        # Prioritize tabular data, protocol sheets, and metadata archives
                        is_target = any(fname.lower().endswith(ext) for ext in [
                            "-isa.zip", ".xlsx", ".csv", ".tsv", ".json", ".pdf", ".txt"
                        ])
                        is_huge_seq = any(fname.lower().endswith(h) for h in [
                            ".fastq.gz", ".fq.gz", ".bam", ".raw", ".tar"
                        ])

                        if is_target and not is_huge_seq and rem_url:
                            target_files.append({
                                "file_name": fname,
                                "url": urljoin(OSDR_BASE, rem_url),
                                "size": fsize
                            })
        except Exception as e:
            self.log(f"⚠️ File listing warning for {num_id}: {e}")
        return target_files

    def download_file(self, url, dest):
        """Download file with stream writing."""
        try:
            with self.session.get(url, stream=True, timeout=40) as r:
                r.raise_for_status()
                with open(dest, "wb") as f:
                    for chunk in r.iter_content(chunk_size=16384):
                        if chunk:
                            f.write(chunk)
            return True
        except Exception as e:
            self.log(f"❌ Failed download {url}: {e}")
            if os.path.exists(dest):
                os.remove(dest)
            return False

    def run(self):
        self.log("=" * 70)
        self.log("🛰️ NASA Space Life Sciences Targeted Data Fetcher Initiated")
        self.log(f"📁 Target Output: {self.files_dir}")
        self.log("=" * 70)

        seen_acc = set()
        downloaded_count = 0

        for category, keywords in TARGET_MODULES.items():
            self.log(f"\n📂 >>> Processing Category: 【{category}】")
            
            for kw in keywords:
                studies = self.search_osdr(kw)
                for st in studies:
                    acc = st["accession"]
                    num_id = st["numeric_id"]
                    if acc in seen_acc:
                        continue
                    seen_acc.add(acc)

                    meta = self.fetch_metadata(num_id)
                    title = meta["title"] or f"NASA Open Study {acc}"
                    self.log(f"   📌 [{acc}] {title[:65]}... (Matched: '{kw}')")

                    files = self.fetch_study_files(num_id)
                    downloaded_for_this = []

                    # Download top 1-2 open analytical datasets
                    for f_info in files[:2]:
                        safe_name = f"{acc}_{f_info['file_name']}"
                        dest_path = os.path.join(self.files_dir, safe_name)
                        
                        if os.path.exists(dest_path):
                            self.log(f"      ⏩ File already present: {safe_name}")
                            downloaded_for_this.append(safe_name)
                            continue

                        self.log(f"      ⬇️ Downloading: {f_info['file_name']} ({f_info['size']} bytes)...")
                        if self.download_file(f_info["url"], dest_path):
                            downloaded_for_this.append(safe_name)
                            downloaded_count += 1

                    self.manifest.append({
                        "category": category,
                        "accession": acc,
                        "title": title,
                        "keyword": kw,
                        "mission": meta["mission"],
                        "description": meta["description"],
                        "organisms": meta["organisms"],
                        "factors": meta["factors"],
                        "osdr_url": f"https://osdr.nasa.gov/bio/repo/data/studies/{acc}",
                        "nlsp_url": f"https://nlsp.nasa.gov/explore?dataType=EXPERIMENTS&id={acc}",
                        "downloaded_files": downloaded_for_this
                    })

                time.sleep(0.4)

        # Save manifest JSON
        manifest_path = os.path.join(self.output_dir, "download_manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as mf:
            json.dump(self.manifest, mf, indent=2, ensure_ascii=False)

        # Generate NASA Space Apps Project Submission Summary Markdown
        summary_path = os.path.join(self.output_dir, "NASA_DATA_SUBMISSION_SUMMARY.md")
        self.generate_submission_doc(summary_path)

        self.log("\n" + "=" * 70)
        self.log(f"🎉 Completed! Processed {len(self.manifest)} studies. Total new files downloaded: {downloaded_count}")
        self.log(f"📄 Full Submission Citation Document: {summary_path}")
        self.log("=" * 70)

    def generate_submission_doc(self, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("# NASA Data and Space Agency Resources Utilized\n\n")
            f.write("> **Directly Copyable for Submission**: Use the tables and evidence statements below in the **'NASA Data'** section of your 2026 NASA Space Apps Challenge Project Page.\n\n")
            
            f.write("## 1. System Integration: AWMEH Neuro-Affective & Physical Health Engine\n")
            f.write("Our software integrates official NASA open-science datasets into two complementary monitoring layers:\n")
            f.write("- **Layer 1: Neuro-Affective & Behavioral Resilience (AWMEH Engine)**: Passive detection of sleep disruption, neuro-inflammation, and cognitive strain in long-duration isolation (180+ days).\n")
            f.write("- **Layer 2: Spaceflight Physiological & Hazard Baselines**: Environmental radiation tracking and musculoskeletal degradation countermeasure calibration.\n\n")

            f.write("## 2. Catalog of Utilized NASA Open Science Datasets\n\n")
            f.write("| Accession ID | Architecture Module | Study Title / Research Scope | NASA Mission / Platform | Source Link |\n")
            f.write("|---|---|---|---|---|\n")
            for m in self.manifest:
                title = m["title"].replace("|", "/")
                f.write(f"| **{m['accession']}** | `{m['category']}` | {title} | {m['mission']} | [NASA OSDR]({m['osdr_url']}) / [NLSP]({m['nlsp_url']}) |\n")

            f.write("\n## 3. How NASA Data Directly Powers Our Software Features\n")
            f.write("1. **Sleep Architecture & Circadian Realignment**: Benchmarked against spaceflight and analog biological assays to detect REM latency anomalies and trigger adaptive cabin spectrum adjustments (480nm blue light).\n")
            f.write("2. **Neuro-Inflammation & Cognitive Strain Detection**: Utilizes cortical immunoassay datasets (e.g., OSD-751) to correlate physical biomarkers with psychological fatigue and emotional masking.\n")
            f.write("3. **Bone & Muscle Loss Countermeasures**: Employs spaceflight DXA microstructure data (e.g., OSD-661) to automatically calculate individual resistance exercise requirements.\n")
            f.write("4. **Radiation Risk Surveillance**: Telemetry thresholds calibrated against cosmic ray and solar particle dose-response records from NASA OSDR.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tailored NASA Life Sciences Fetcher for Space Apps 2026")
    parser.add_argument("--dir", default="./nasa_life_sciences_data", help="Output path")
    parser.add_argument("--limit", type=int, default=2, help="Max studies per keyword")

    args = parser.parse_args()
    fetcher = NASASpaceHealthDataFetcher(output_dir=args.dir, max_studies_per_topic=args.limit)
    fetcher.run()
