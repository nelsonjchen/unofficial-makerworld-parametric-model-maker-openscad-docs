(function () {
  const ROOT_ID = "pmm-font-index";
  const PAGE_SIZE = 120;
  const DATA_URL = new URL("font-index-data.json", document.currentScript.src).toString();
  const loadedCss = new Set();

  const SAMPLE_PRESETS = {
    makerworld: "MakerWorld PMM",
    alphabet: "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz",
    pangram: "The quick brown fox jumps over the lazy dog.",
    digits: "OpenSCAD text() 0123456789",
    label: "Customizable model label",
    single: "Aa",
  };

  const COLLECTIONS = [
    {
      id: "all",
      label: "All Fonts",
      description: "Every family found in PMM's public font inventories.",
      predicate: () => true,
    },
    {
      id: "installed",
      label: "Installed Runtime",
      description: "Families present in PMM's runtime font list, closest to what OpenSCAD can use.",
      predicate: (family) => family.installed,
    },
    {
      id: "broad",
      label: "Broad Catalog",
      description: "Families from PMM's broader display/catalog list; not always runtime-confirmed.",
      predicate: (family) => family.broad,
    },
    {
      id: "previewable",
      label: "Previewable",
      description: "Families this docs site can preview with Google Fonts CSS or a verified alias.",
      predicate: (family) => family.previewStatuses.has("google-css"),
    },
    {
      id: "caveats",
      label: "Warnings",
      description: "Families with licensing, alias, redistribution, or preview caveats.",
      predicate: (family) => family.hasCaveat,
    },
    {
      id: "unknown",
      label: "Unknown",
      description: "Families without enough source evidence for a confident license/provenance label.",
      predicate: (family) => family.licenseConfidences.has("unknown"),
    },
  ];

  const SORTS = [
    { id: "styles-desc", label: "Most styles" },
    { id: "family-az", label: "Family A-Z" },
    { id: "family-za", label: "Family Z-A" },
    { id: "installed-first", label: "Installed first" },
    { id: "warnings-first", label: "Warnings first" },
    { id: "previewable-first", label: "Previewable first" },
    { id: "shuffle", label: "Shuffle" },
  ];

  const PMM_FILTERS = [
    { key: "Expressive", label: "Feeling" },
    { key: "Theme", label: "Appearance" },
    { key: "Script", label: "Calligraphy" },
    { key: "Serif", label: "Serif" },
    { key: "Sans", label: "Sans Serif" },
    { key: "Seasonal", label: "Seasonal" },
  ];

  function option(value, label) {
    const el = document.createElement("option");
    el.value = value;
    el.textContent = label;
    return el;
  }

  function button(label, className) {
    const el = document.createElement("button");
    el.type = "button";
    el.className = className;
    el.textContent = label;
    return el;
  }

  function labeledControl(label, control, className) {
    const wrap = document.createElement("label");
    wrap.className = className || "pmm-font-book__control";
    const text = document.createElement("span");
    text.className = "pmm-font-book__control-label";
    text.textContent = label;
    wrap.append(text, control);
    return wrap;
  }

  function badge(text, tone) {
    const span = document.createElement("span");
    span.className = "pmm-font-book__badge" + (tone ? ` pmm-font-book__badge--${tone}` : "");
    span.textContent = text;
    return span;
  }

  function licenseTone(confidence) {
    if (confidence === "conflicting" || confidence === "restricted-redistribution") return "danger";
    if (confidence === "custom-license" || confidence === "unknown") return "warn";
    return "";
  }

  function ensureCss(record) {
    if (!record.google_css_url || loadedCss.has(record.google_css_url)) return;
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = record.google_css_url;
    document.head.appendChild(link);
    loadedCss.add(record.google_css_url);
  }

  function sampleText(state) {
    if (state.sampleMode === "custom") return state.customSample || SAMPLE_PRESETS.makerworld;
    return SAMPLE_PRESETS[state.sampleMode] || SAMPLE_PRESETS.makerworld;
  }

  function sortRecords(a, b) {
    const installedDelta = Number(b.in_installed_inventory) - Number(a.in_installed_inventory);
    if (installedDelta) return installedDelta;
    const regularDelta = Number(b.style === "Regular") - Number(a.style === "Regular");
    if (regularDelta) return regularDelta;
    return a.pmm_name.localeCompare(b.pmm_name);
  }

  function stringHash(value) {
    let hash = 2166136261;
    for (let index = 0; index < value.length; index += 1) {
      hash ^= value.charCodeAt(index);
      hash = Math.imul(hash, 16777619);
    }
    return hash >>> 0;
  }

  function applyPreviewStyle(element, record, state) {
    element.style.fontFamily = record.preview_family
      ? `"${record.preview_family}", ${record.fallback_stack}`
      : record.fallback_stack;
    element.style.fontSize = `${state.sampleSize}px`;
    if (record.weight) element.style.fontWeight = record.weight;
    if (record.italic) element.style.fontStyle = "italic";
  }

  function buildFamilies(fonts) {
    const families = new Map();
    fonts.forEach((record) => {
      let family = families.get(record.family);
      if (!family) {
        family = {
          family: record.family,
          records: [],
          previewStatuses: new Set(),
          licenseConfidences: new Set(),
          installed: false,
          broad: false,
          hasCaveat: false,
          pmmFilters: Object.fromEntries(PMM_FILTERS.map((filter) => [filter.key, new Set()])),
          pmmSubsets: new Set(),
          pmmCategories: new Set(),
        };
        families.set(record.family, family);
      }
      family.records.push(record);
      family.previewStatuses.add(record.preview_status);
      family.licenseConfidences.add(record.license_confidence);
      family.installed = family.installed || record.in_installed_inventory;
      family.broad = family.broad || record.in_broad_catalog;
      family.hasCaveat =
        family.hasCaveat ||
        record.preview_status !== "google-css" ||
        !["clean", "likely-clean"].includes(record.license_confidence);
      const metadata = record.pmm_metadata || {};
      if (metadata.category) family.pmmCategories.add(metadata.category);
      if (metadata.stroke) family.pmmCategories.add(metadata.stroke);
      (metadata.subsets || []).forEach((subset) => family.pmmSubsets.add(subset));
      PMM_FILTERS.forEach((filter) => {
        ((metadata.filters || {})[filter.key] || []).forEach((value) => family.pmmFilters[filter.key].add(value));
      });
    });

    return Array.from(families.values())
      .map((family) => {
        family.records.sort(sortRecords);
        family.demoRecord =
          family.records.find((record) => record.in_installed_inventory && record.style === "Regular" && record.preview_status === "google-css") ||
          family.records.find((record) => record.style === "Regular" && record.preview_status === "google-css") ||
          family.records.find((record) => record.in_installed_inventory) ||
          family.records[0];
        family.searchText = [
          family.family,
          family.records.map((record) => `${record.pmm_name} ${record.style} ${record.preview_family || ""} ${record.license_summary || ""}`).join(" "),
          Array.from(family.pmmCategories).join(" "),
          Array.from(family.pmmSubsets).join(" "),
          PMM_FILTERS.map((filter) => Array.from(family.pmmFilters[filter.key]).join(" ")).join(" "),
        ].join(" ").toLowerCase();
        family.shuffleKey = stringHash(family.family);
        return family;
      })
      .sort((a, b) => a.family.localeCompare(b.family));
  }

  function familyMatches(family, state) {
    if (!COLLECTIONS.find((collection) => collection.id === state.collection).predicate(family)) return false;
    if (state.query && !family.searchText.includes(state.query)) return false;
    if (state.style && !family.records.some((record) => record.style.toLowerCase().includes(state.style))) return false;
    if (state.preview && !family.previewStatuses.has(state.preview)) return false;
    if (state.license && !family.licenseConfidences.has(state.license)) return false;
    if (state.subset && !family.pmmSubsets.has(state.subset)) return false;
    if (PMM_FILTERS.some((filter) => state.pmmFilters[filter.key] && !family.pmmFilters[filter.key].has(state.pmmFilters[filter.key]))) return false;
    return true;
  }

  function byName(a, b) {
    return a.family.localeCompare(b.family);
  }

  function sortFamilies(families, state) {
    const sorted = families.slice();
    sorted.sort((a, b) => {
      if (state.sort === "family-za") return b.family.localeCompare(a.family);
      if (state.sort === "installed-first") {
        const installedDelta = Number(b.installed) - Number(a.installed);
        if (installedDelta) return installedDelta;
        return byName(a, b);
      }
      if (state.sort === "warnings-first") {
        const caveatDelta = Number(b.hasCaveat) - Number(a.hasCaveat);
        if (caveatDelta) return caveatDelta;
        const unknownDelta = Number(b.licenseConfidences.has("unknown")) - Number(a.licenseConfidences.has("unknown"));
        if (unknownDelta) return unknownDelta;
        return byName(a, b);
      }
      if (state.sort === "previewable-first") {
        const previewDelta = Number(b.previewStatuses.has("google-css")) - Number(a.previewStatuses.has("google-css"));
        if (previewDelta) return previewDelta;
        return byName(a, b);
      }
      if (state.sort === "shuffle") {
        const shuffleDelta =
          stringHash(`${a.family}:${state.shuffleSeed}`) -
          stringHash(`${b.family}:${state.shuffleSeed}`);
        if (shuffleDelta) return shuffleDelta;
        return byName(a, b);
      }
      if (state.sort === "styles-desc") {
        const styleDelta = b.records.length - a.records.length;
        if (styleDelta) return styleDelta;
        const installedDelta = Number(b.installed) - Number(a.installed);
        if (installedDelta) return installedDelta;
        return byName(a, b);
      }
      return byName(a, b);
    });
    return sorted;
  }

  function renderFamilyBadges(family) {
    const wrap = document.createElement("div");
    wrap.className = "pmm-font-book__badges";
    if (family.installed) wrap.appendChild(badge("installed"));
    if (family.broad) wrap.appendChild(badge("broad"));
    Array.from(family.previewStatuses).sort().forEach((status) => {
      wrap.appendChild(badge(status, status === "fallback-only" ? "warn" : ""));
    });
    Array.from(family.licenseConfidences).sort().forEach((confidence) => {
      wrap.appendChild(badge(confidence, licenseTone(confidence)));
    });
    return wrap;
  }

  function familyInventoryLabel(family) {
    if (family.installed && family.broad) return "installed runtime + broad catalog";
    if (family.installed) return "installed runtime";
    if (family.broad) return "broad catalog";
    return "unclassified";
  }

  function familyCaveatLabel(family) {
    const licenses = Array.from(family.licenseConfidences).sort().join(", ");
    const previews = Array.from(family.previewStatuses).sort().join(", ");
    return `preview: ${previews}; license/provenance: ${licenses}`;
  }

  function pmmMetadataLines(family) {
    const lines = [];
    if (family.pmmCategories.size) lines.push(`PMM category: ${Array.from(family.pmmCategories).sort().join(", ")}`);
    PMM_FILTERS.forEach((filter) => {
      const values = Array.from(family.pmmFilters[filter.key]).sort();
      if (values.length) lines.push(`${filter.label}: ${values.join(", ")}`);
    });
    const subsets = Array.from(family.pmmSubsets).sort();
    if (subsets.length) lines.push(`Writing systems: ${subsets.slice(0, 10).map(subsetLabel).join(", ")}${subsets.length > 10 ? `, +${subsets.length - 10} more` : ""}`);
    return lines;
  }

  function formatFamilyLine(family) {
    return `- ${family.family} (${family.records.length} PMM string${family.records.length === 1 ? "" : "s"}; ${familyInventoryLabel(family)}; ${familyCaveatLabel(family)})`;
  }

  function formatPmmStringLine(record) {
    const inventory = [
      record.in_installed_inventory ? "installed runtime" : "",
      record.in_broad_catalog ? "broad catalog" : "",
    ].filter(Boolean).join(" + ") || "unclassified";
    return `- ${record.pmm_name} (${record.style}; ${inventory}; preview: ${record.preview_status}; license/provenance: ${record.license_confidence})`;
  }

  function subsetLabel(value) {
    return value
      .split("-")
      .map((part) => part ? part[0].toUpperCase() + part.slice(1) : part)
      .join(" ");
  }

  function selectedPmmFilterLabels(state) {
    const selected = [];
    if (state.subset) selected.push(`writing system: ${subsetLabel(state.subset)}`);
    PMM_FILTERS.forEach((filter) => {
      if (state.pmmFilters[filter.key]) selected.push(`${filter.label}: ${state.pmmFilters[filter.key]}`);
    });
    return selected;
  }

  function exportFamilies(families) {
    return families.map(formatFamilyLine).join("\n");
  }

  function exportPmmStrings(families) {
    return families
      .flatMap((family) => family.records.map(formatPmmStringLine))
      .join("\n");
  }

  function exportAgentPrompt(families, state, collection) {
    const filters = [
      `collection: ${collection.label}`,
      state.query ? `search: ${state.queryDisplay}` : "",
      state.style ? `style filter: ${state.styleDisplay}` : "",
      state.preview ? `preview filter: ${state.preview}` : "",
      state.license ? `license/provenance filter: ${state.license}` : "",
      ...selectedPmmFilterLabels(state),
      `sort: ${SORTS.find((sort) => sort.id === state.sort)?.label || state.sort}`,
    ].filter(Boolean).join("; ");

    return [
      "I am choosing a MakerWorld Parametric Model Maker OpenSCAD text() font.",
      "Please narrow the list below to a few good typeface candidates for my model, and explain the tradeoffs.",
      "Prefer exact PMM family names from the list. Treat warnings, unknown provenance, and fallback-only previews as caveats.",
      "",
      `Current PMM font index scope: ${collection.description}`,
      `Current filters: ${filters}`,
      `Candidate families: ${families.length}`,
      "",
      "Families:",
      exportFamilies(families),
    ].join("\n");
  }

  async function copyText(text, status, label) {
    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(text);
      } else {
        const textarea = document.createElement("textarea");
        textarea.value = text;
        textarea.setAttribute("readonly", "");
        textarea.style.position = "fixed";
        textarea.style.left = "-9999px";
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        textarea.remove();
      }
      status.textContent = `Copied ${label}.`;
    } catch (error) {
      status.textContent = `Could not copy automatically: ${error.message}`;
    }
  }

  function countFor(collection, families) {
    return families.filter(collection.predicate).length;
  }

  function renderSidebar(sidebar, families, state, render) {
    sidebar.replaceChildren();
    const title = document.createElement("div");
    title.className = "pmm-font-book__sidebar-title";
    title.textContent = "PMM Fonts";
    const subtitle = document.createElement("div");
    subtitle.className = "pmm-font-book__sidebar-subtitle";
    subtitle.textContent = `${families.length.toLocaleString()} families`;
    sidebar.append(title, subtitle);

    const nav = document.createElement("nav");
    nav.className = "pmm-font-book__nav";
    COLLECTIONS.forEach((collection) => {
      const item = button("", "pmm-font-book__nav-button");
      item.dataset.active = String(state.collection === collection.id);
      const labelWrap = document.createElement("span");
      labelWrap.className = "pmm-font-book__nav-label";
      const label = document.createElement("span");
      label.textContent = collection.label;
      const description = document.createElement("span");
      description.className = "pmm-font-book__nav-description";
      description.textContent = collection.description;
      const count = document.createElement("span");
      count.className = "pmm-font-book__nav-count";
      count.textContent = countFor(collection, families).toLocaleString();
      labelWrap.append(label, description);
      item.append(labelWrap, count);
      item.addEventListener("click", () => {
        state.collection = collection.id;
        state.visible = PAGE_SIZE;
        render();
      });
      nav.appendChild(item);
    });
    sidebar.appendChild(nav);

    const links = document.createElement("div");
    links.className = "pmm-font-book__sidebar-links";
    links.innerHTML = '<a href="../">Docs home</a><a href="../font-provenance-notes/">Provenance notes</a>';
    sidebar.appendChild(links);
  }

  function renderToolbar(toolbar, state, render) {
    toolbar.replaceChildren();

    const search = document.createElement("input");
    search.type = "search";
    search.value = state.queryDisplay;
    search.placeholder = "Search families, styles, exact PMM strings...";
    search.className = "pmm-font-book__search";
    search.addEventListener("input", () => {
      state.queryDisplay = search.value;
      state.query = search.value.trim().toLowerCase();
      state.visible = PAGE_SIZE;
      render();
    });

    const searchWrap = labeledControl("Search", search, "pmm-font-book__control pmm-font-book__control--search");

    const viewGroup = document.createElement("div");
    viewGroup.className = "pmm-font-book__segmented";
    viewGroup.setAttribute("aria-label", "View");
    ["grid", "list"].forEach((view) => {
      const item = button(view === "grid" ? "Grid" : "List", "pmm-font-book__segment");
      item.dataset.active = String(state.view === view);
      item.addEventListener("click", () => {
        state.view = view;
        render();
      });
      viewGroup.appendChild(item);
    });
    const viewWrap = document.createElement("div");
    viewWrap.className = "pmm-font-book__control pmm-font-book__control--view";
    const viewLabel = document.createElement("span");
    viewLabel.className = "pmm-font-book__control-label";
    viewLabel.textContent = "View";
    viewWrap.append(viewLabel, viewGroup);

    const sample = document.createElement("select");
    sample.className = "pmm-font-book__select";
    sample.append(option("makerworld", "MakerWorld PMM"));
    sample.append(option("single", "Aa"));
    sample.append(option("alphabet", "Alphabet"));
    sample.append(option("pangram", "Pangram"));
    sample.append(option("digits", "Digits and code"));
    sample.append(option("label", "Model label"));
    sample.append(option("custom", "Custom"));
    sample.value = state.sampleMode;
    sample.addEventListener("change", () => {
      state.sampleMode = sample.value;
      render();
    });
    const sampleWrap = labeledControl("Preview text", sample);

    const sort = document.createElement("select");
    sort.className = "pmm-font-book__select";
    SORTS.forEach((item) => sort.append(option(item.id, item.label)));
    sort.value = state.sort;
    sort.addEventListener("change", () => {
      state.sort = sort.value;
      if (state.sort === "shuffle") state.shuffleSeed = Math.random().toString(36).slice(2);
      state.visible = PAGE_SIZE;
      render();
    });
    const sortWrap = labeledControl("Sort", sort);

    const random = button("Random mix", "pmm-font-book__random");
    random.title = "Show a fresh random spread of font families";
    random.addEventListener("click", () => {
      state.sort = "shuffle";
      state.shuffleSeed = Math.random().toString(36).slice(2);
      state.visible = PAGE_SIZE;
      state.selectedFamily = "";
      render();
    });
    const randomWrap = labeledControl("Explore", random, "pmm-font-book__control pmm-font-book__control--random");

    const custom = document.createElement("input");
    custom.type = "text";
    custom.className = "pmm-font-book__custom";
    custom.placeholder = "Custom preview text";
    custom.value = state.customSample;
    custom.hidden = state.sampleMode !== "custom";
    custom.addEventListener("input", () => {
      state.customSample = custom.value;
      render();
    });
    const customWrap = labeledControl("Custom text", custom);
    customWrap.hidden = state.sampleMode !== "custom";

    const size = document.createElement("input");
    size.type = "range";
    size.min = "28";
    size.max = "92";
    size.value = String(state.sampleSize);
    size.className = "pmm-font-book__size";
    size.addEventListener("input", () => {
      state.sampleSize = Number(size.value);
      render();
    });
    const sizeWrap = labeledControl("Preview size", size, "pmm-font-book__control pmm-font-book__control--size");

    toolbar.append(searchWrap, viewWrap, sortWrap, randomWrap, sampleWrap, customWrap, sizeWrap);
  }

  function renderFilters(filters, state, render, payload) {
    filters.replaceChildren();

    const style = document.createElement("input");
    style.type = "search";
    style.placeholder = "Style: Regular, Bold, Italic...";
    style.value = state.styleDisplay;
    style.addEventListener("input", () => {
      state.styleDisplay = style.value;
      state.style = style.value.trim().toLowerCase();
      state.visible = PAGE_SIZE;
      render();
    });

    const preview = document.createElement("select");
    preview.append(option("", "All preview sources"));
    preview.append(option("google-css", "Google CSS previews"));
    preview.append(option("external-preview", "External preview only"));
    preview.append(option("fallback-only", "Fallback only"));
    preview.value = state.preview;
    preview.addEventListener("change", () => {
      state.preview = preview.value;
      state.visible = PAGE_SIZE;
      render();
    });

    const license = document.createElement("select");
    license.append(option("", "All license confidence"));
    ["clean", "likely-clean", "custom-license", "restricted-redistribution", "conflicting", "unknown"].forEach((value) => {
      license.append(option(value, value));
    });
    license.value = state.license;
    license.addEventListener("change", () => {
      state.license = license.value;
      state.visible = PAGE_SIZE;
      render();
    });

    const pmmTitle = document.createElement("div");
    pmmTitle.className = "pmm-font-book__filter-title";
    pmmTitle.textContent = "PMM font dialog filters";
    const pmmNote = document.createElement("div");
    pmmNote.className = "pmm-font-book__filter-note";
    pmmNote.textContent = "Mirrors MakerWorld's filter metadata from fonts-0.9.0. PMM's Language menu uses a larger language-to-family map; this page exposes the lighter writing-system subset.";

    const subset = document.createElement("select");
    subset.append(option("", "All writing systems"));
    (payload.pmm_filter_options?.subsets || []).forEach((value) => subset.append(option(value, subsetLabel(value))));
    subset.value = state.subset;
    subset.addEventListener("change", () => {
      state.subset = subset.value;
      state.visible = PAGE_SIZE;
      render();
    });

    const pmmControls = document.createElement("div");
    pmmControls.className = "pmm-font-book__pmm-filters";
    pmmControls.append(labeledControl("Writing system", subset, "pmm-font-book__control"));
    PMM_FILTERS.forEach((filter) => {
      const select = document.createElement("select");
      select.append(option("", `All ${filter.label.toLowerCase()}`));
      (payload.pmm_filter_options?.[filter.key] || []).forEach((value) => select.append(option(value, value)));
      select.value = state.pmmFilters[filter.key] || "";
      select.addEventListener("change", () => {
        state.pmmFilters[filter.key] = select.value;
        state.visible = PAGE_SIZE;
        render();
      });
      pmmControls.append(labeledControl(filter.label, select, "pmm-font-book__control"));
    });

    filters.append(
      labeledControl("Style", style, "pmm-font-book__control"),
      labeledControl("Preview source", preview, "pmm-font-book__control"),
      labeledControl("License confidence", license, "pmm-font-book__control"),
      pmmTitle,
      pmmNote,
      pmmControls,
    );
  }

  function renderExportPanel(panel, families, state, collection) {
    panel.replaceChildren();

    const text = document.createElement("div");
    text.className = "pmm-font-book__export-text";
    const title = document.createElement("strong");
    title.textContent = "Agent export";
    const summary = document.createElement("span");
    summary.textContent = `Copy the current ${families.length.toLocaleString()} matching families, including unloaded infinite-scroll results.`;
    text.append(title, summary);

    const actions = document.createElement("div");
    actions.className = "pmm-font-book__export-actions";
    const status = document.createElement("span");
    status.className = "pmm-font-book__copy-status";
    status.setAttribute("aria-live", "polite");

    const familiesButton = button("Copy families", "pmm-font-book__copy");
    familiesButton.addEventListener("click", () => {
      copyText(exportFamilies(families), status, `${families.length.toLocaleString()} families`);
    });

    const stringsButton = button("Copy PMM strings", "pmm-font-book__copy");
    stringsButton.addEventListener("click", () => {
      copyText(exportPmmStrings(families), status, "exact PMM strings");
    });

    const promptButton = button("Copy agent prompt", "pmm-font-book__copy pmm-font-book__copy--primary");
    promptButton.addEventListener("click", () => {
      copyText(exportAgentPrompt(families, state, collection), status, "agent prompt");
    });

    actions.append(promptButton, familiesButton, stringsButton, status);
    panel.append(text, actions);
  }

  function renderFamilyCards(container, families, state, selectFamily) {
    container.replaceChildren();
    container.dataset.view = state.view;
    const text = sampleText(state);
    families.forEach((family) => {
      const record = family.demoRecord;
      ensureCss(record);

      const card = button("", "pmm-font-book__card");
      card.dataset.selected = String(state.selectedFamily === family.family);
      card.addEventListener("click", () => selectFamily(family.family));

      const sample = document.createElement("div");
      sample.className = "pmm-font-book__sample";
      sample.textContent = text;
      applyPreviewStyle(sample, record, state);

      const body = document.createElement("div");
      body.className = "pmm-font-book__card-body";
      const name = document.createElement("div");
      name.className = "pmm-font-book__family-name";
      name.textContent = family.family;
      const meta = document.createElement("div");
      meta.className = "pmm-font-book__muted";
      meta.textContent = `${family.records.length.toLocaleString()} PMM string${family.records.length === 1 ? "" : "s"}`;
      body.append(name, meta, renderFamilyBadges(family));

      card.append(sample, body);
      container.appendChild(card);
    });
  }

  function renderInspector(inspector, family, state, closeInspector) {
    inspector.replaceChildren();
    if (!family) {
      inspector.dataset.open = "false";
      return;
    }
    inspector.dataset.open = "true";

    const head = document.createElement("div");
    head.className = "pmm-font-book__inspector-head";
    const close = button("Close", "pmm-font-book__close");
    close.addEventListener("click", closeInspector);

    const title = document.createElement("h2");
    title.textContent = family.family;
    head.append(title, close);
    const meta = document.createElement("p");
    meta.className = "pmm-font-book__muted";
    meta.textContent = `${family.records.length.toLocaleString()} exact PMM font string${family.records.length === 1 ? "" : "s"}`;
    inspector.append(head, meta, renderFamilyBadges(family));

    const text = sampleText(state);
    const preview = document.createElement("div");
    preview.className = "pmm-font-book__inspector-sample";
    preview.textContent = text;
    ensureCss(family.demoRecord);
    applyPreviewStyle(preview, family.demoRecord, { ...state, sampleSize: Math.max(state.sampleSize, 56) });
    inspector.appendChild(preview);

    const note = document.createElement("p");
    note.className = "pmm-font-book__muted";
    note.textContent = family.demoRecord.preview_family
      ? family.demoRecord.preview_family === family.family
        ? "Preview uses the matching Google Fonts family."
        : `Preview alias: ${family.demoRecord.preview_family}; exact PMM names remain below.`
      : "Fallback preview only; this site is not loading a matching webfont.";
    inspector.appendChild(note);

    const pmmLines = pmmMetadataLines(family);
    if (pmmLines.length) {
      const pmmMeta = document.createElement("div");
      pmmMeta.className = "pmm-font-book__pmm-meta";
      const pmmTitle = document.createElement("strong");
      pmmTitle.textContent = "PMM filter metadata";
      const pmmList = document.createElement("ul");
      pmmLines.forEach((line) => {
        const item = document.createElement("li");
        item.textContent = line;
        pmmList.appendChild(item);
      });
      pmmMeta.append(pmmTitle, pmmList);
      inspector.appendChild(pmmMeta);
    }

    const list = document.createElement("div");
    list.className = "pmm-font-book__styles";
    family.records.forEach((record) => {
      ensureCss(record);
      const item = document.createElement("article");
      item.className = "pmm-font-book__style";
      const styleName = document.createElement("div");
      styleName.className = "pmm-font-book__style-name";
      styleName.textContent = record.style;
      const exact = document.createElement("code");
      exact.textContent = record.pmm_name;
      const stylePreview = document.createElement("div");
      stylePreview.className = "pmm-font-book__style-preview";
      stylePreview.textContent = text;
      applyPreviewStyle(stylePreview, record, { ...state, sampleSize: 24 });
      const summary = document.createElement("p");
      summary.className = "pmm-font-book__muted";
      summary.textContent = record.license_summary;
      item.append(styleName, exact, stylePreview, renderFamilyBadges({ ...family, records: [record], previewStatuses: new Set([record.preview_status]), licenseConfidences: new Set([record.license_confidence]), installed: record.in_installed_inventory, broad: record.in_broad_catalog }), summary);
      list.appendChild(item);
    });
    inspector.appendChild(list);
  }

  function init(root, payload) {
    const allFamilies = buildFamilies(payload.fonts);
    const state = {
      collection: "all",
      query: "",
      queryDisplay: "",
      style: "",
      styleDisplay: "",
      preview: "",
      license: "",
      subset: "",
      pmmFilters: Object.fromEntries(PMM_FILTERS.map((filter) => [filter.key, ""])),
      sampleMode: "makerworld",
      customSample: "",
      sampleSize: 34,
      view: "grid",
      sort: "styles-desc",
      shuffleSeed: "initial",
      visible: PAGE_SIZE,
      filteredCount: 0,
      selectedFamily: "",
    };

    root.replaceChildren();
    const shell = document.createElement("section");
    shell.className = "pmm-font-book";

    const sidebar = document.createElement("aside");
    sidebar.className = "pmm-font-book__sidebar";
    const main = document.createElement("main");
    main.className = "pmm-font-book__main";
    const header = document.createElement("header");
    header.className = "pmm-font-book__header";
    const titleBlock = document.createElement("div");
    titleBlock.className = "pmm-font-book__title-block";
    const title = document.createElement("h2");
    title.textContent = "All Fonts";
    const meta = document.createElement("div");
    meta.className = "pmm-font-book__muted";
    titleBlock.append(title, meta);
    const toolbar = document.createElement("div");
    toolbar.className = "pmm-font-book__toolbar";
    header.append(titleBlock, toolbar);
    const filters = document.createElement("div");
    filters.className = "pmm-font-book__filters";
    const exportPanel = document.createElement("div");
    exportPanel.className = "pmm-font-book__export";
    const gallery = document.createElement("div");
    gallery.className = "pmm-font-book__gallery";
    const infiniteStatus = document.createElement("div");
    infiniteStatus.className = "pmm-font-book__infinite-status";
    infiniteStatus.setAttribute("aria-live", "polite");
    const loadMore = button("Show more", "pmm-font-book__more");
    const sentinel = document.createElement("div");
    sentinel.className = "pmm-font-book__sentinel";
    sentinel.setAttribute("aria-hidden", "true");
    const inspector = document.createElement("aside");
    inspector.className = "pmm-font-book__inspector";

    main.append(header, filters, exportPanel, gallery, infiniteStatus, loadMore, sentinel);
    shell.append(sidebar, main, inspector);
    root.appendChild(shell);

    function selectFamily(familyName) {
      state.selectedFamily = familyName;
      render();
    }

    loadMore.addEventListener("click", () => {
      state.visible += PAGE_SIZE;
      render();
    });

    if ("IntersectionObserver" in window) {
      const observer = new IntersectionObserver(
        (entries) => {
          if (!entries.some((entry) => entry.isIntersecting)) return;
          const canLoadMore = state.visible < state.filteredCount;
          if (!canLoadMore) return;
          state.visible += PAGE_SIZE;
          render();
        },
        { rootMargin: "700px 0px 700px 0px" },
      );
      observer.observe(sentinel);
    }

    function render() {
      const collection = COLLECTIONS.find((item) => item.id === state.collection) || COLLECTIONS[0];
      const filtered = allFamilies.filter((family) => familyMatches(family, state));
      if (state.selectedFamily && !filtered.some((family) => family.family === state.selectedFamily)) {
        state.selectedFamily = "";
      }
      const sorted = sortFamilies(filtered, state);
      const selected = allFamilies.find((family) => family.family === state.selectedFamily);
      const visible = sorted.slice(0, state.visible);
      state.filteredCount = filtered.length;

      title.textContent = collection.label;
      meta.textContent = `${filtered.length.toLocaleString()} families; ${filtered.reduce((sum, family) => sum + family.records.length, 0).toLocaleString()} PMM font strings. ${collection.description}`;
      renderSidebar(sidebar, allFamilies, state, render);
      renderToolbar(toolbar, state, render);
      renderFilters(filters, state, render, payload);
      renderExportPanel(exportPanel, sorted, state, collection);
      renderFamilyCards(gallery, visible, state, selectFamily);
      renderInspector(inspector, selected, state, () => {
        state.selectedFamily = "";
        render();
      });
      const allVisible = visible.length >= filtered.length;
      infiniteStatus.textContent = allVisible
        ? `${visible.length.toLocaleString()} families shown.`
        : `Showing ${visible.length.toLocaleString()} of ${filtered.length.toLocaleString()} families. Scroll for more.`;
      loadMore.hidden = allVisible;
      sentinel.hidden = allVisible;
    }

    render();
  }

  document.addEventListener("DOMContentLoaded", () => {
    const root = document.getElementById(ROOT_ID);
    if (!root) return;
    fetch(DATA_URL)
      .then((response) => response.json())
      .then((payload) => init(root, payload))
      .catch((error) => {
        root.textContent = `Unable to load generated font index: ${error}`;
      });
  });
})();
