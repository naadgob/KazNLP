(() => {
  const BATCH = 40;
  const SHUFFLE_BATCH = 20;
  const CONSUMING_FILTERS = new Set([
    "unlabeled",
    "llm_mixed",
    "needs_review",
    "suspicious",
    "ru_but_kazakh",
    "kaz_letters_in_ru_text",
    "mixed_false_positive",
    "kz_no_signal",
    "unlabeled_kazakh",
    "low_signal",
  ]);
  const TONE_CONSUMING_FILTERS = new Set(["unlabeled_tone", "mixed_unlabeled_tone"]);

  const state = {
    jobId: null,
    labelingMode: "language",
    mode: "sequential",
    queueTotal: 0,
    queuePos: 0,
    currentRowId: null,
    filter: "unlabeled",
    classFilter: "any",
    domainFilter: "any",
    search: "",
    saving: false,
    loading: false,
    consumingFilters: CONSUMING_FILTERS,
    rowByPos: new Map(),
    prefetching: false,
    shuffleRows: [],
    shufflePos: 0,
    shuffleInitial: 0,
    autoTranslate: localStorage.getItem("labeler_auto_translate") !== "0",
    translateAbort: null,
  };

  const els = {
    empty: document.getElementById("manualEmpty"),
    workspace: document.getElementById("manualWorkspace"),
    metricGrid: document.getElementById("metricGrid"),
    distBar: document.getElementById("distBar"),
    sessionClassCounts: document.getElementById("sessionClassCounts"),
    sessionDistBar: document.getElementById("sessionDistBar"),
    sessionBalanceHint: document.getElementById("sessionBalanceHint"),
    manualClassCounts: document.getElementById("manualClassCounts"),
    manualDistBar: document.getElementById("manualDistBar"),
    manualBalanceHint: document.getElementById("manualBalanceHint"),
    sessionStrip: document.getElementById("sessionStrip"),
    queueFilter: document.getElementById("queueFilter"),
    domainFilter: document.getElementById("domainFilter"),
    classFilter: document.getElementById("classFilter"),
    queueSearch: document.getElementById("queueSearch"),
    languageActions: document.getElementById("languageActions"),
    sentimentActions: document.getElementById("sentimentActions"),
    shortcutHint: document.getElementById("shortcutHint"),
    domainHint: document.getElementById("domainHint"),
    toneHint: document.getElementById("toneHint"),
    queueInfo: document.getElementById("queueInfo"),
    rowPosition: document.getElementById("rowPosition"),
    rowMeta: document.getElementById("rowMeta"),
    manualProgressFill: document.getElementById("manualProgressFill"),
    manualProgressText: document.getElementById("manualProgressText"),
    textCard: document.getElementById("textCard"),
    translateBlock: document.getElementById("translateBlock"),
    translateCard: document.getElementById("translateCard"),
    translateBtn: document.getElementById("translateBtn"),
    autoTranslate: document.getElementById("autoTranslate"),
    hintRow: document.getElementById("hintRow"),
    llmHint: document.getElementById("llmHint"),
    kazCharsHint: document.getElementById("kazCharsHint"),
    realMixedHint: document.getElementById("realMixedHint"),
    qualityHint: document.getElementById("qualityHint"),
    disagreeHint: document.getElementById("disagreeHint"),
    mismatchList: document.getElementById("mismatchList"),
    flagReview: document.getElementById("flagReview"),
    saveStatus: document.getElementById("saveStatus"),
  };

  function api(path, opts = {}) {
    return fetch(path, opts).then(async (res) => {
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.detail || res.statusText);
      return data;
    });
  }

  function queueUrl(position, batch = BATCH) {
    const p = new URLSearchParams({
      filter: state.filter,
      search: state.search,
      class_filter: state.classFilter,
      domain_filter: state.domainFilter,
      position: String(position),
      batch: String(batch),
      lite: "true",
      include_row: "true",
    });
    return `/api/jobs/${state.jobId}/manual/queue?${p}`;
  }

  function actionButtons() {
    return state.labelingMode === "sentiment"
      ? ".btn-tone, #undoBtn, #prevBtn, #nextBtn, #skipBtn, #shuffleBtn"
      : ".btn-lang, #undoBtn, #prevBtn, #nextBtn, #skipBtn, #shuffleBtn";
  }

  function setLoading(on) {
    state.loading = on;
    document.querySelectorAll(actionButtons()).forEach((btn) => {
      btn.disabled = on || state.saving;
    });
  }

  function applyLabelingMode(mode) {
    state.labelingMode = mode;
    document.querySelectorAll(".mode-btn").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.mode === mode);
    });
    const sentiment = mode === "sentiment";
    els.languageActions?.classList.toggle("hidden", sentiment);
    els.sentimentActions?.classList.toggle("hidden", !sentiment);
    document.querySelectorAll(".filter-language-only").forEach((el) => {
      el.classList.toggle("hidden", sentiment);
    });
    document.querySelectorAll(".filter-sentiment-only").forEach((el) => {
      el.classList.toggle("hidden", !sentiment);
    });
    document.querySelectorAll(".language-only").forEach((el) => {
      el.classList.toggle("hidden", sentiment);
    });
    if (els.shortcutHint) {
      els.shortcutHint.innerHTML = sentiment
        ? "Hotkeys: <kbd>1</kbd>/<kbd>P</kbd> positive · <kbd>2</kbd>/<kbd>N</kbd> negative · <kbd>3</kbd>/<kbd>X</kbd> skip · <kbd>T</kbd> перевод · <kbd>Z</kbd> undo · <kbd>←</kbd><kbd>→</kbd> nav · <kbd>S</kbd> shuffle"
        : "Hotkeys: <kbd>1</kbd>/<kbd>R</kbd> ru · <kbd>2</kbd>/<kbd>K</kbd> kz · <kbd>3</kbd>/<kbd>M</kbd> mixed · <kbd>T</kbd> перевод · <kbd>Z</kbd> undo · <kbd>←</kbd><kbd>→</kbd> nav · <kbd>S</kbd> shuffle";
    }
    if (sentiment) {
      els.queueFilter.value = "mixed_unlabeled_tone";
      els.classFilter.value = "mixed";
    } else if (els.queueFilter.value.startsWith("tone_") || els.queueFilter.value.includes("unlabeled_tone") || els.queueFilter.value.startsWith("domain_")) {
      els.queueFilter.value = "unlabeled";
    }
  }

  function setShuffleActive(on) {
    document.getElementById("shuffleBtn")?.classList.toggle("active", on);
  }

  function classDistBar(counts, total) {
    if (!total) {
      return `<div class="dist-seg empty" style="width:100%" title="empty"></div>`;
    }
    return ["ru", "kz", "mixed"]
      .map(
        (key) =>
          `<div class="dist-seg ${key}" style="width:${(100 * counts[key]) / total}%" title="${key} ${counts[key]}"></div>`
      )
      .join("");
  }

  function classCountChips(counts, total) {
    const pct = (n) => (total ? Math.round((100 * n) / total) : 0);
    return ["ru", "kz", "mixed"]
      .map(
        (key) =>
          `<span class="class-chip ${key}"><span class="class-chip-k">${key.toUpperCase()}</span><span class="class-chip-v">${counts[key] ?? 0}</span><span class="class-chip-p">${pct(counts[key] ?? 0)}%</span></span>`
      )
      .join("");
  }

  function balanceHint(counts, emptyText) {
    const total = (counts.ru ?? 0) + (counts.kz ?? 0) + (counts.mixed ?? 0);
    if (!total) return emptyText;
    const ideal = total / 3;
    const entries = [
      ["ru", counts.ru ?? 0],
      ["kz", counts.kz ?? 0],
      ["mixed", counts.mixed ?? 0],
    ];
    entries.sort((a, b) => a[1] - b[1]);
    const [lagKey, lagCount] = entries[0];
    const [leadKey, leadCount] = entries[2];
    const lagGap = Math.round(ideal - lagCount);
    if (lagGap <= 1 && leadCount - lagCount <= 2) {
      return "Balanced (~33% each)";
    }
    const labels = { ru: "RU", kz: "KZ", mixed: "MIXED" };
    return `Add more ${labels[lagKey]} (+${Math.max(lagGap, 1)} vs avg) · heavy on ${labels[leadKey]}`;
  }

  function renderClassBalance(m) {
    const session = m.session_distribution || { ru: 0, kz: 0, mixed: 0 };
    const manual = m.manual_distribution || { ru: 0, kz: 0, mixed: 0 };
    const sessionTotal = session.ru + session.kz + session.mixed;
    const manualTotal = manual.ru + manual.kz + manual.mixed;

    if (els.sessionClassCounts) {
      els.sessionClassCounts.innerHTML = classCountChips(session, sessionTotal);
    }
    if (els.sessionDistBar) {
      els.sessionDistBar.innerHTML = classDistBar(session, sessionTotal);
    }
    if (els.sessionBalanceHint) {
      els.sessionBalanceHint.textContent = balanceHint(session, "Label rows to track session balance");
    }

    if (els.manualClassCounts) {
      els.manualClassCounts.innerHTML = classCountChips(manual, manualTotal);
    }
    if (els.manualDistBar) {
      els.manualDistBar.innerHTML = classDistBar(manual, manualTotal);
    }
    if (els.manualBalanceHint) {
      els.manualBalanceHint.textContent = balanceHint(
        manual,
        `${m.manual_count ?? 0} manual labels total`
      );
    }

    if (els.sessionStrip) {
      if (!sessionTotal) {
        els.sessionStrip.innerHTML =
          '<span class="session-strip-label">Session:</span><span class="session-strip-muted">RU 0 · KZ 0 · MIXED 0</span>';
      } else {
        els.sessionStrip.innerHTML = `<span class="session-strip-label">Session balance</span>${classCountChips(session, sessionTotal)}<span class="session-strip-hint">${balanceHint(session, "")}</span>`;
      }
    }
  }

  function renderMetrics(m) {
    if (!m) return;
    const h = m.heuristics || {};
    const td = m.tone_distribution || {};
    const md = m.mixed_domain_distribution || {};
    const items =
      state.labelingMode === "sentiment"
        ? [
            ["Tone labeled", `${m.tone_labeled ?? 0} / ${m.total}`, `${m.tone_labeled_pct ?? 0}%`],
            ["Pos / Neg", `${td.positive ?? 0} / ${td.negative ?? 0}`, `skip ${td.skip ?? 0}`],
            ["Unlabeled tone", td.unlabeled ?? 0, "empty label"],
            ["Mixed domains", `R${md.review ?? 0}`, `L${md.logistics ?? 0} · O${md.other ?? 0}`],
            ["Tone manual", m.tone_manual_count ?? 0, "gold labels"],
            ["Session tone", m.sentiment_session_labeled ?? 0, m.tone_labels_per_hour ? `${m.tone_labels_per_hour}/h` : "this run"],
            ["Mixed rows", m.distribution?.mixed ?? 0, "language=mixed"],
            ["Language done", `${m.labeled_pct ?? 0}%`, "LID coverage"],
          ]
        : [
            ["Labeled", `${m.labeled} / ${m.total}`, `${m.labeled_pct}%`],
            ["Real mixed", h.potential_real_mixed, "RU+KZ signals"],
            ["Suspicious", h.suspicious_labeled, "label ≠ text"],
            ["RU+ә/ң", h.ru_with_kazakh_letters, "maybe mixed/kz"],
            ["False mixed", h.mixed_false_positive, "weak signal"],
            ["Unlbl+ә/ң", h.unlabeled_kazakh, "quick wins"],
            ["Session", m.session_labeled, m.labels_per_hour ? `${m.labels_per_hour}/h` : "this run"],
            ["Disagree LLM", m.disagree_count, "you vs LLM"],
          ];
    els.metricGrid.innerHTML = items
      .map(
        ([k, v, sub]) =>
          `<div class="metric-item"><span class="metric-k">${k}</span><span class="metric-v">${v ?? 0}</span>${sub ? `<span class="metric-sub">${sub}</span>` : ""}</div>`
      )
      .join("");

    const d = m.distribution;
    const total = m.total || 1;
    els.distBar.innerHTML = `
      <div class="dist-seg ru" style="width:${(100 * d.ru) / total}%" title="ru ${d.ru}"></div>
      <div class="dist-seg kz" style="width:${(100 * d.kz) / total}%" title="kz ${d.kz}"></div>
      <div class="dist-seg mixed" style="width:${(100 * d.mixed) / total}%" title="mixed ${d.mixed}"></div>
      <div class="dist-seg empty" style="width:${(100 * m.unlabeled) / total}%" title="empty ${m.unlabeled}"></div>`;

    if (state.labelingMode === "sentiment") {
      els.manualProgressFill.style.width = `${m.tone_labeled_pct ?? 0}%`;
      els.manualProgressText.textContent = `${m.tone_labeled_pct ?? 0}% tone labeled · mixed ${m.distribution?.mixed ?? 0}`;
      renderToneBalance(m);
    } else {
      els.manualProgressFill.style.width = `${m.labeled_pct}%`;
      els.manualProgressText.textContent = `${m.labeled_pct}% labeled · real mixed ${h.potential_real_mixed ?? 0}`;
      renderClassBalance(m);
    }
  }

  function renderToneBalance(m) {
    const session = m.sentiment_session_distribution || { positive: 0, negative: 0, skip: 0 };
    const manual = m.manual_tone_distribution || { positive: 0, negative: 0, skip: 0 };
    const sessionTotal = (session.positive ?? 0) + (session.negative ?? 0) + (session.skip ?? 0);
    const manualTotal = (manual.positive ?? 0) + (manual.negative ?? 0) + (manual.skip ?? 0);
    const toneBar = (counts, total) => {
      if (!total) return `<div class="dist-seg empty" style="width:100%"></div>`;
      return ["positive", "negative", "skip"]
        .map(
          (key) =>
            `<div class="dist-seg ${key}" style="width:${(100 * (counts[key] ?? 0)) / total}%" title="${key} ${counts[key] ?? 0}"></div>`
        )
        .join("");
    };
    const toneChips = (counts, total) => {
      const pct = (n) => (total ? Math.round((100 * n) / total) : 0);
      return ["positive", "negative", "skip"]
        .map(
          (key) =>
            `<span class="class-chip ${key}"><span class="class-chip-k">${key.toUpperCase()}</span><span class="class-chip-v">${counts[key] ?? 0}</span><span class="class-chip-p">${pct(counts[key] ?? 0)}%</span></span>`
        )
        .join("");
    };
    if (els.sessionClassCounts) els.sessionClassCounts.innerHTML = toneChips(session, sessionTotal);
    if (els.sessionDistBar) els.sessionDistBar.innerHTML = toneBar(session, sessionTotal);
    if (els.sessionBalanceHint) {
      els.sessionBalanceHint.textContent = sessionTotal
        ? `Session: +${session.positive ?? 0} / −${session.negative ?? 0} / skip ${session.skip ?? 0}`
        : "Label tone to track session balance";
    }
    if (els.manualClassCounts) els.manualClassCounts.innerHTML = toneChips(manual, manualTotal);
    if (els.manualDistBar) els.manualDistBar.innerHTML = toneBar(manual, manualTotal);
    if (els.manualBalanceHint) {
      els.manualBalanceHint.textContent = `${m.tone_manual_count ?? 0} manual tone labels total`;
    }
    if (els.sessionStrip) {
      els.sessionStrip.innerHTML = sessionTotal
        ? `<span class="session-strip-label">Tone session</span>${toneChips(session, sessionTotal)}`
        : `<span class="session-strip-label">Tone session:</span><span class="session-strip-muted">POS 0 · NEG 0 · SKIP 0</span>`;
    }
  }

  async function refreshMetrics() {
    if (!state.jobId) return;
    const m = await api(`/api/jobs/${state.jobId}/metrics`);
    renderMetrics(m);
    return m;
  }

  function updateQueueInfo() {
    const classPart = state.classFilter !== "any" ? ` · class: ${state.classFilter}` : "";
    const domainPart = state.domainFilter !== "any" ? ` · domain: ${state.domainFilter}` : "";
    const modePart = state.mode === "shuffle" ? " · shuffle" : "";
    els.queueInfo.textContent = `${state.queueTotal.toLocaleString()} in queue · ${state.filter}${classPart}${domainPart}${modePart}`;
  }

  function ingestBatch(q) {
    if (q.consuming_filters) state.consumingFilters = new Set(q.consuming_filters);
    state.queueTotal = q.total || 0;
    for (const item of q.rows || []) {
      if (item.row) state.rowByPos.set(item.position, item.row);
    }
    updateQueueInfo();
  }

  function currentRow() {
    return state.rowByPos.get(state.queuePos) || null;
  }

  function showPos(pos) {
    const row = state.rowByPos.get(pos);
    if (!row) return false;
    state.queuePos = pos;
    state.currentRowId = row.row_id;
    renderRow(row, pos);
    return true;
  }

  async function prefetch(position, { clear = false } = {}) {
    if (clear) state.rowByPos.clear();
    const q = await api(queueUrl(position, BATCH));
    ingestBatch(q);
    return q;
  }

  function prefetchAhead(pos) {
    if (state.prefetching) return;
    const lastCached = Math.max(...state.rowByPos.keys(), -1);
    if (lastCached >= pos + 15 || lastCached >= state.queueTotal - 1) return;
    state.prefetching = true;
    api(queueUrl(lastCached + 1, BATCH))
      .then(ingestBatch)
      .catch(() => {})
      .finally(() => {
        state.prefetching = false;
      });
  }

  async function loadQueue(position = 0) {
    if (!state.jobId) return;
    state.mode = "sequential";
    state.shuffleRows = [];
    state.shufflePos = 0;
    state.shuffleInitial = 0;
    setShuffleActive(false);
    state.filter = els.queueFilter.value;
    state.classFilter = els.classFilter.value;
    state.domainFilter = els.domainFilter?.value || "any";
    state.search = els.queueSearch.value.trim();
    setLoading(true);
    els.textCard.textContent = "Loading sample…";
    try {
      await prefetch(position, { clear: true });
      if (!showPos(Math.min(position, Math.max(0, state.queueTotal - 1)))) {
        renderRow(null, 0);
        await refreshMetrics();
      }
    } catch (err) {
      els.textCard.textContent = `Error loading queue: ${err.message}`;
    } finally {
      setLoading(false);
    }
  }

  function shuffleUrl() {
    const p = new URLSearchParams({
      filter: state.filter,
      search: state.search,
      class_filter: state.classFilter,
      domain_filter: state.domainFilter,
      batch: String(SHUFFLE_BATCH),
      lite: "true",
    });
    return `/api/jobs/${state.jobId}/manual/shuffle?${p}`;
  }

  function shufflePositionLabel(rowId) {
    return `Shuffle ${state.shufflePos + 1}/${state.shuffleInitial} · pool ${state.queueTotal.toLocaleString()} · row #${rowId}`;
  }

  function renderShuffleRow() {
    const item = state.shuffleRows[state.shufflePos];
    if (!item?.row) return;
    state.currentRowId = item.row_id;
    renderRow(item.row, state.shufflePos, shufflePositionLabel(item.row_id));
  }

  async function loadShuffle() {
    if (!state.jobId) return;
    state.filter = els.queueFilter.value;
    state.classFilter = els.classFilter.value;
    state.domainFilter = els.domainFilter?.value || "any";
    state.search = els.queueSearch.value.trim();
    state.mode = "shuffle";
    state.rowByPos.clear();
    setShuffleActive(true);
    setLoading(true);
    els.textCard.textContent = "Loading random batch…";
    try {
      const q = await api(shuffleUrl());
      if (q.consuming_filters) state.consumingFilters = new Set(q.consuming_filters);
      state.queueTotal = q.total || 0;
      state.shuffleRows = q.rows || [];
      state.shuffleInitial = q.batch_size || state.shuffleRows.length;
      state.shufflePos = 0;
      updateQueueInfo();
      if (!state.shuffleRows.length) {
        renderRow(null, 0);
      } else {
        renderShuffleRow();
      }
      els.saveStatus.textContent = `Shuffle batch: ${state.shuffleInitial} random samples`;
    } catch (err) {
      els.textCard.textContent = `Error loading shuffle: ${err.message}`;
    } finally {
      setLoading(false);
    }
  }

  function isConsumingFilter(name) {
    if (TONE_CONSUMING_FILTERS.has(name)) return true;
    return state.consumingFilters.has(name);
  }

  function advanceShuffleAfterLabel() {
    state.shuffleRows.splice(state.shufflePos, 1);
    if (isConsumingFilter(state.filter) && state.queueTotal > 0) {
      state.queueTotal -= 1;
    }
    updateQueueInfo();
    if (!state.shuffleRows.length) {
      return loadShuffle();
    }
    if (state.shufflePos >= state.shuffleRows.length) {
      state.shufflePos = state.shuffleRows.length - 1;
    }
    renderShuffleRow();
    els.flagReview.checked = false;
  }

  async function navShuffle(delta) {
    if (!state.shuffleRows.length || state.loading || state.saving) return;
    const newPos = state.shufflePos + delta;
    if (newPos < 0) return;
    if (newPos >= state.shuffleRows.length) {
      if (delta > 0) await loadShuffle();
      return;
    }
    state.shufflePos = newPos;
    renderShuffleRow();
  }

  function highlightKazakhLetters(text) {
    const chars = "әіңғүұқөһӘІҢҒҮҰҚӨҺ";
    let out = "";
    for (const ch of text) {
      if (chars.includes(ch)) {
        out += `<mark class="kz-char">${ch}</mark>`;
      } else {
        out += ch.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
      }
    }
    return out;
  }

  function apiErrorDetail(data, fallback) {
    const d = data?.detail;
    if (Array.isArray(d)) return d.map((x) => x.msg || x).join("; ");
    if (d) return String(d);
    return fallback;
  }

  function translationForce(row) {
    if (state.labelingMode === "sentiment") return true;
    const lang = row?.language;
    return lang === "kz" || lang === "mixed";
  }

  async function fetchTranslation(text, { force = false, row = null } = {}) {
    if (state.translateAbort) state.translateAbort.abort();
    const ctrl = new AbortController();
    state.translateAbort = ctrl;
    const tryForce = force || translationForce(row);
    els.translateBlock.classList.remove("hidden");
    els.translateCard.className = "translate-card loading";
    els.translateCard.textContent = "Перевод…";
    try {
      const res = await fetch("/api/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, force: tryForce }),
        signal: ctrl.signal,
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(apiErrorDetail(data, res.statusText));
      if (ctrl.signal.aborted) return;
      els.translateCard.className = "translate-card";
      if (data.skipped && data.note) {
        els.translateCard.textContent = data.note;
      } else {
        const tag = data.cached ? " · cache" : "";
        els.translateCard.textContent = `${data.translated}${tag ? ` (${tag.trim()})` : ""}`;
      }
    } catch (err) {
      if (err.name === "AbortError") return;
      els.translateCard.className = "translate-card error";
      els.translateCard.textContent = err.message || "Ошибка перевода";
    } finally {
      if (state.translateAbort === ctrl) state.translateAbort = null;
    }
  }

  const TRANSLATE_IDLE = "↻ или T — перевести вручную";

  function showTranslatePanel(idle = true) {
    els.translateBlock?.classList.remove("hidden");
    if (!idle || !els.translateCard) return;
    els.translateCard.className = "translate-card idle";
    els.translateCard.textContent = TRANSLATE_IDLE;
  }

  function maybeAutoTranslate(text, row) {
    showTranslatePanel(true);
    if (!els.autoTranslate?.checked) return;
    fetchTranslation(text, { row });
  }

  function renderRow(row, posInQueue, positionLabel) {
    if (!row) {
      els.textCard.textContent = "Queue empty — change filter or download CSV.";
      els.rowPosition.textContent = "—";
      els.hintRow.classList.add("hidden");
      els.mismatchList.classList.add("hidden");
      els.translateBlock?.classList.add("hidden");
      return;
    }

    els.rowPosition.textContent =
      positionLabel ||
      `Queue ${posInQueue + 1} / ${state.queueTotal.toLocaleString()} · row #${row.row_id}`;
    const src = row.label_source ? row.label_source : "—";
    const lang = row.language ? row.language : "—";
    const tonePart = row.tone ? ` · tone: ${row.tone}` : "";
    els.rowMeta.textContent = `lang: ${lang} · source: ${src}${tonePart} · ${row.word_count} words`;
    if (state.translateAbort) state.translateAbort.abort();
    els.textCard.innerHTML = highlightKazakhLetters(row.text);
    maybeAutoTranslate(row.text, row);

    els.hintRow.classList.remove("hidden");
    els.llmHint.textContent = row.llm_language ? `LLM: ${row.llm_language}` : "LLM: —";
    els.llmHint.className = `pill llm-${row.llm_language || "none"}`;

    const sigParts = [];
    if (row.has_kazakh_chars) sigParts.push("ә/ң letters");
    if (row.has_russian_signal) sigParts.push("RU text");
    els.kazCharsHint.textContent = sigParts.length ? sigParts.join(" · ") : "no bilingual signals";
    els.kazCharsHint.className = `pill ${row.has_kazakh_chars ? "ok" : "muted"}`;

    if (row.domain && els.domainHint) {
      const labels = { review: "review/product", logistics: "logistics", other: "other" };
      els.domainHint.textContent = `domain: ${labels[row.domain] || row.domain}`;
      els.domainHint.className = `pill domain-${row.domain}`;
      els.domainHint.classList.remove("hidden");
    } else {
      els.domainHint?.classList.add("hidden");
    }
    if (els.toneHint) {
      if (row.tone) {
        els.toneHint.textContent = `tone: ${row.tone}`;
        els.toneHint.className = `pill tone-${row.tone}`;
        els.toneHint.classList.remove("hidden");
      } else {
        els.toneHint.classList.add("hidden");
      }
    }

    if (row.potential_real_mixed) {
      els.realMixedHint.textContent = "✓ potential real mixed";
      els.realMixedHint.className = "pill ok strong";
      els.realMixedHint.classList.remove("hidden");
    } else {
      els.realMixedHint.classList.add("hidden");
    }
    els.qualityHint.classList.add("hidden");
    els.disagreeHint.classList.toggle("hidden", !row.disagree_llm);
    els.mismatchList.classList.add("hidden");

    document.querySelectorAll(".btn-lang").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.lang === row.language);
      btn.disabled = state.loading || state.saving;
    });
    document.querySelectorAll(".btn-tone").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.tone === row.tone);
      btn.disabled = state.loading || state.saving;
    });
    els.flagReview.checked = row.needs_review;
  }

  async function submitSentiment(tone) {
    if (!state.jobId || state.currentRowId == null || state.saving || state.loading) return;
    const rowId = state.currentRowId;
    state.saving = true;
    setLoading(true);
    els.saveStatus.textContent = "Saving…";
    try {
      const res = await api(`/api/jobs/${state.jobId}/manual/sentiment-label`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          row_id: rowId,
          tone,
          queue_filter: state.filter,
          queue_class: state.classFilter,
          queue_search: state.search,
          queue_domain: state.domainFilter,
          queue_position: state.queuePos,
        }),
      });
      renderMetrics(res.metrics);
      els.saveStatus.textContent = `Saved #${rowId} → ${tone} · export to flush CSV`;

      if (state.mode === "shuffle") {
        await advanceShuffleAfterLabel();
        return;
      }

      if (res.next?.row && res.next.row_id !== rowId && res.next.row.row_id !== rowId) {
        state.queueTotal = res.next.total || 0;
        state.queuePos = res.next.position || 0;
        state.currentRowId = res.next.row_id ?? res.next.row.row_id;
        state.rowByPos.clear();
        state.rowByPos.set(state.queuePos, res.next.row);
        updateQueueInfo();
        renderRow(res.next.row, res.next.position);
        prefetchAhead(state.queuePos);
      } else {
        state.rowByPos.clear();
        await loadQueue(state.queuePos);
      }
    } catch (err) {
      els.saveStatus.textContent = `Error: ${err.message}`;
    } finally {
      state.saving = false;
      setLoading(false);
    }
  }

  async function submitLabel(lang) {
    if (!state.jobId || state.currentRowId == null || state.saving || state.loading) return;
    const rowId = state.currentRowId;
    state.saving = true;
    setLoading(true);
    els.saveStatus.textContent = "Saving…";
    try {
      const res = await api(`/api/jobs/${state.jobId}/manual/label`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          row_id: rowId,
          language: lang,
          needs_review: els.flagReview.checked,
          queue_filter: state.filter,
          queue_class: state.classFilter,
          queue_search: state.search,
          queue_domain: state.domainFilter,
          queue_position: state.queuePos,
        }),
      });
      renderMetrics(res.metrics);
      els.saveStatus.textContent = `Saved #${rowId} → ${lang} · export to flush CSV`;

      if (state.mode === "shuffle") {
        await advanceShuffleAfterLabel();
        return;
      }

      if (res.next?.row && res.next.row_id !== rowId && res.next.row.row_id !== rowId) {
        state.queueTotal = res.next.total || 0;
        state.queuePos = res.next.position || 0;
        state.currentRowId = res.next.row.row_id ?? res.next.row_id;
        state.rowByPos.clear();
        state.rowByPos.set(state.queuePos, res.next.row);
        updateQueueInfo();
        renderRow(res.next.row, res.next.position);
        els.flagReview.checked = false;
        prefetchAhead(state.queuePos);
      } else {
        state.rowByPos.clear();
        await loadQueue(state.queuePos);
      }
    } catch (err) {
      els.saveStatus.textContent = `Error: ${err.message}`;
    } finally {
      state.saving = false;
      setLoading(false);
    }
  }

  async function undo() {
    if (!state.jobId || state.loading) return;
    try {
      const res = await api(`/api/jobs/${state.jobId}/manual/undo`, { method: "POST" });
      renderMetrics(res.metrics);
      els.saveStatus.textContent = `Undo row #${res.row_id}`;
      await loadQueue(state.queuePos);
    } catch (err) {
      els.saveStatus.textContent = err.message;
    }
  }

  async function nav(delta) {
    if (state.mode === "shuffle") {
      await navShuffle(delta);
      return;
    }
    if (!state.queueTotal || state.loading || state.saving) return;
    const newPos = state.queuePos + delta;
    if (newPos < 0 || newPos >= state.queueTotal) return;

    if (showPos(newPos)) {
      prefetchAhead(newPos);
      return;
    }

    setLoading(true);
    try {
      await prefetch(newPos, { clear: true });
      showPos(newPos);
      prefetchAhead(newPos);
    } finally {
      setLoading(false);
    }
  }

  function bindUi() {
    document.querySelectorAll(".mode-btn").forEach((btn) => {
      btn.addEventListener("click", async () => {
        if (btn.dataset.mode === state.labelingMode) return;
        applyLabelingMode(btn.dataset.mode);
        await refreshMetrics();
        await loadQueue(0);
      });
    });
    document.querySelectorAll(".btn-lang").forEach((btn) => {
      btn.addEventListener("click", () => submitLabel(btn.dataset.lang));
    });
    document.querySelectorAll(".btn-tone").forEach((btn) => {
      btn.addEventListener("click", () => submitSentiment(btn.dataset.tone));
    });
    document.getElementById("undoBtn")?.addEventListener("click", undo);
    document.getElementById("shuffleBtn")?.addEventListener("click", () => loadShuffle());
    els.autoTranslate?.addEventListener("change", () => {
      localStorage.setItem("labeler_auto_translate", els.autoTranslate.checked ? "1" : "0");
      const row = currentRow();
      if (row?.text) maybeAutoTranslate(row.text, row);
    });
    if (els.autoTranslate) els.autoTranslate.checked = state.autoTranslate;
    els.translateBtn?.addEventListener("click", () => {
      const row = currentRow();
      if (row?.text) fetchTranslation(row.text, { force: true, row });
    });
    document.getElementById("prevBtn")?.addEventListener("click", () => nav(-1));
    document.getElementById("nextBtn")?.addEventListener("click", () => nav(1));
    document.getElementById("skipBtn")?.addEventListener("click", () => nav(1));
    els.queueFilter.addEventListener("change", () => loadQueue(0));
    els.domainFilter?.addEventListener("change", () => loadQueue(0));
    els.classFilter.addEventListener("change", () => loadQueue(0));
    els.queueSearch.addEventListener("keydown", (e) => {
      if (e.key === "Enter") loadQueue(0);
    });

    document.addEventListener("keydown", (e) => {
      const manualTab = document.getElementById("tab-manual");
      if (!state.jobId || manualTab?.classList.contains("hidden")) return;
      if (state.loading || state.saving) return;
      const tag = document.activeElement?.tagName;
      if (tag === "INPUT" || tag === "SELECT" || tag === "TEXTAREA") return;

      const k = e.key.toLowerCase();
      if (state.labelingMode === "sentiment") {
        if (k === "1" || k === "p") {
          e.preventDefault();
          submitSentiment("positive");
        } else if (k === "2" || k === "n") {
          e.preventDefault();
          submitSentiment("negative");
        } else if (k === "3" || k === "x") {
          e.preventDefault();
          submitSentiment("skip");
        }
      } else if (k === "1" || k === "r") {
        e.preventDefault();
        submitLabel("ru");
      } else if (k === "2" || k === "k") {
        e.preventDefault();
        submitLabel("kz");
      } else if (k === "3" || k === "m") {
        e.preventDefault();
        submitLabel("mixed");
      }
      if (k === "z") {
        e.preventDefault();
        undo();
      } else if (k === "arrowleft") {
        e.preventDefault();
        nav(-1);
      } else if (k === "arrowright") {
        e.preventDefault();
        nav(1);
      } else if (k === "s") {
        e.preventDefault();
        loadShuffle();
      } else if (k === "t") {
        e.preventDefault();
        const row = currentRow();
        if (row?.text) fetchTranslation(row.text, { force: true, row });
      }
    });
  }

  async function pickInitialFilter(jobId) {
    const m = await api(`/api/jobs/${jobId}/metrics`);
    if (state.labelingMode === "sentiment") {
      els.queueFilter.value = "mixed_unlabeled_tone";
      els.classFilter.value = "mixed";
      els.domainFilter.value = "any";
      return;
    }
    if (m.total > 50000) {
      els.queueFilter.value = "unlabeled";
      return;
    }
    const h = m.heuristics || {};
    if (m.unlabeled > 0) {
      els.queueFilter.value = h.unlabeled_kazakh > 0 ? "unlabeled_kazakh" : "unlabeled";
    }
  }

  window.ManualLabeler = {
    async start(jobId) {
      state.jobId = jobId;
      state.queuePos = 0;
      state.rowByPos.clear();
      els.empty.classList.add("hidden");
      els.workspace.classList.remove("hidden");
      els.textCard.textContent = "Loading metrics…";
      await refreshMetrics();
      await pickInitialFilter(jobId);
      await loadQueue(0);
      els.textCard.focus();
    },
    refreshMetrics,
  };

  bindUi();
})();
