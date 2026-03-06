interface Provider {
  id: string;
  name: string;
  type: string;
  city: string;
  state: string;
  teleconsult: string;
  fee_range: string;
  last_verified: string;
  verification_tier: string;
  adult_adhd: string;
  child_adhd: string;
  adolescent_adhd: string;
  assessment_style: string;
  med_mgmt: string;
  stimulant_comfort: string;
  comorbidities: string[];
  languages: string[];
  tags: string[];
  flags: string[];
}

declare global {
  interface Window {
    __PROVIDERS__: Provider[];
  }
}

const providers: Provider[] = window.__PROVIDERS__;

const searchInput = document.getElementById("search-input") as HTMLInputElement;
const filterCity = document.getElementById("filter-city") as HTMLSelectElement;
const filterState = document.getElementById("filter-state") as HTMLSelectElement;
const filterTeleconsult = document.getElementById("filter-teleconsult") as HTMLSelectElement;
const filterAdult = document.getElementById("filter-adult") as HTMLSelectElement;
const filterChild = document.getElementById("filter-child") as HTMLSelectElement;
const filterMed = document.getElementById("filter-med") as HTMLSelectElement;
const filterLanguage = document.getElementById("filter-language") as HTMLSelectElement;
const filterVerifiedWithin = document.getElementById("filter-verified-within") as HTMLSelectElement;
const filterStimulant = document.getElementById("filter-stimulant") as HTMLSelectElement;
const filterAssessment = document.getElementById("filter-assessment") as HTMLSelectElement;
const filterType = document.getElementById("filter-type") as HTMLSelectElement;
const filterComorbidity = document.getElementById("filter-comorbidity") as HTMLSelectElement;
const sortBy = document.getElementById("sort-by") as HTMLSelectElement;
const clearBtn = document.getElementById("clear-filters") as HTMLButtonElement;
const advancedToggle = document.getElementById("advanced-toggle") as HTMLButtonElement;
const advancedFilters = document.getElementById("advanced-filters") as HTMLDivElement;
const resultsCount = document.getElementById("results-count") as HTMLParagraphElement;
const providerList = document.getElementById("provider-list") as HTMLDivElement;
const noResults = document.getElementById("no-results") as HTMLParagraphElement;

// Read URL params on load
function readUrlParams() {
  const params = new URLSearchParams(window.location.search);
  if (params.get("city")) filterCity.value = params.get("city")!;
  if (params.get("state")) filterState.value = params.get("state")!;
  if (params.get("tele")) filterTeleconsult.value = params.get("tele")!;
  if (params.get("adult")) filterAdult.value = params.get("adult")!;
  if (params.get("child")) filterChild.value = params.get("child")!;
  if (params.get("med")) filterMed.value = params.get("med")!;
  if (params.get("lang")) filterLanguage.value = params.get("lang")!;
  if (params.get("q")) searchInput.value = params.get("q")!;
}

function applyFilters() {
  const query = searchInput.value.toLowerCase().trim();
  const city = filterCity.value;
  const state = filterState.value;
  const teleconsult = filterTeleconsult.value;
  const adult = filterAdult.value;
  const child = filterChild.value;
  const med = filterMed.value;
  const language = filterLanguage.value;
  const verifiedWithin = filterVerifiedWithin.value;
  const stimulant = filterStimulant.value;
  const assessment = filterAssessment.value;
  const providerType = filterType.value;
  const comorbidity = filterComorbidity.value;

  const now = new Date();

  let filtered = providers.filter((p) => {
    if (query) {
      const searchable = `${p.name} ${p.city} ${p.state} ${p.tags.join(" ")} ${p.languages.join(" ")}`.toLowerCase();
      if (!searchable.includes(query)) return false;
    }
    if (city && p.city !== city) return false;
    if (state && p.state !== state) return false;
    if (teleconsult && p.teleconsult !== teleconsult) return false;
    if (adult && p.adult_adhd !== adult) return false;
    if (child && p.child_adhd !== child) return false;
    if (med && p.med_mgmt !== med) return false;
    if (language && !p.languages.includes(language)) return false;
    if (stimulant && p.stimulant_comfort !== stimulant) return false;
    if (assessment && p.assessment_style !== assessment) return false;
    if (providerType && p.type !== providerType) return false;
    if (comorbidity && !p.comorbidities.includes(comorbidity)) return false;

    if (verifiedWithin) {
      const months = parseInt(verifiedWithin);
      const cutoff = new Date(now);
      cutoff.setMonth(cutoff.getMonth() - months);
      if (new Date(p.last_verified) < cutoff) return false;
    }

    return true;
  });

  // Sort
  const sort = sortBy.value;
  if (sort === "verified") {
    filtered.sort((a, b) => b.last_verified.localeCompare(a.last_verified));
  } else if (sort === "name") {
    filtered.sort((a, b) => a.name.localeCompare(b.name));
  } else if (sort === "city") {
    filtered.sort((a, b) => a.city.localeCompare(b.city) || a.name.localeCompare(b.name));
  }

  // Update visibility
  const cards = providerList.querySelectorAll<HTMLElement>("[data-provider-id]");
  const visibleIds = new Set(filtered.map((p) => p.id));

  cards.forEach((card) => {
    const id = card.dataset.providerId;
    card.style.display = id && visibleIds.has(id) ? "" : "none";
  });

  // Sort DOM order
  const sortedIds = filtered.map((p) => p.id);
  sortedIds.forEach((id) => {
    const card = providerList.querySelector(`[data-provider-id="${id}"]`);
    if (card) providerList.appendChild(card);
  });

  resultsCount.textContent = `${filtered.length} provider${filtered.length !== 1 ? "s" : ""} found`;
  noResults.classList.toggle("hidden", filtered.length > 0);
}

// Event listeners
const allFilters = [filterCity, filterState, filterTeleconsult, filterAdult, filterChild, filterMed, filterLanguage, filterVerifiedWithin, filterStimulant, filterAssessment, filterType, filterComorbidity, sortBy];

allFilters.forEach((el) => el.addEventListener("change", applyFilters));

let searchTimeout: ReturnType<typeof setTimeout>;
searchInput.addEventListener("input", () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(applyFilters, 200);
});

advancedToggle.addEventListener("click", () => {
  const isOpen = advancedFilters.classList.toggle("open");
  advancedToggle.textContent = isOpen ? "Hide advanced filters" : "Show advanced filters";
});

clearBtn.addEventListener("click", () => {
  searchInput.value = "";
  allFilters.forEach((el) => { if (el !== sortBy) el.value = ""; });
  applyFilters();
  // Clear URL params
  window.history.replaceState({}, "", window.location.pathname);
});

// Init
readUrlParams();
applyFilters();
