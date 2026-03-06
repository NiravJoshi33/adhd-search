const REPO_URL = "https://github.com/user/adhd-search";

const form = document.getElementById("submit-form") as HTMLFormElement;

form.addEventListener("submit", (e) => {
  e.preventDefault();

  const get = (id: string) => (document.getElementById(id) as HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement).value.trim();

  const name = get("name");
  const type = get("type");
  const city = get("city");
  const state = get("state");
  const address = get("address");
  const website = get("website");
  const contact = get("contact");
  const bookingLink = get("booking_link");
  const languages = get("languages");
  const teleconsult = get("teleconsult");
  const feeRange = get("fee_range");
  const waitTime = get("wait_time");
  const adultAdhd = get("adult_adhd");
  const childAdhd = get("child_adhd");
  const adolescentAdhd = get("adolescent_adhd");
  const assessmentStyle = get("assessment_style");
  const medMgmt = get("med_mgmt");
  const stimulantComfort = get("stimulant_comfort");
  const source = get("source");
  const notes = get("notes");

  const comorbidities = Array.from(document.querySelectorAll<HTMLInputElement>('input[name="comorbidities"]:checked'))
    .map((cb) => cb.value);

  const tags = Array.from(document.querySelectorAll<HTMLInputElement>('input[name="tags"]:checked'))
    .map((cb) => cb.value);

  const title = `New listing: ${name} (${city})`;

  const body = `### Provider Information

| Field | Value |
|-------|-------|
| **Name** | ${name} |
| **Type** | ${type} |
| **City** | ${city} |
| **State** | ${state} |
| **Address** | ${address || "N/A"} |
| **Website** | ${website || "N/A"} |
| **Contact** | ${contact || "N/A"} |
| **Booking Link** | ${bookingLink || "N/A"} |
| **Languages** | ${languages} |
| **Teleconsult** | ${teleconsult} |
| **Fee Range** | ${feeRange || "N/A"} |
| **Wait Time** | ${waitTime || "N/A"} |

### ADHD-Specific

| Field | Value |
|-------|-------|
| **Adult ADHD** | ${adultAdhd} |
| **Child ADHD** | ${childAdhd} |
| **Adolescent ADHD** | ${adolescentAdhd} |
| **Assessment Style** | ${assessmentStyle} |
| **Medication Management** | ${medMgmt} |
| **Stimulant Comfort** | ${stimulantComfort} |
| **Comorbidities** | ${comorbidities.join(", ") || "N/A"} |
| **Tags** | ${tags.join(", ") || "N/A"} |

### Source
${source}

### Notes
${notes || "None"}`;

  const issueUrl = `${REPO_URL}/issues/new?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}&labels=new-listing`;

  window.open(issueUrl, "_blank");
});
