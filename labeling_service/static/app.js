(() => {
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("fileInput");
  const browseBtn = document.getElementById("browseBtn");
  const fileInfo = document.getElementById("fileInfo");
  const preview = document.getElementById("preview");
  const previewTable = document.querySelector("#previewTable tbody");
  const startBtn = document.getElementById("startBtn");
  const exportBlockUpload = document.getElementById("exportBlockUpload");
  const exportBlockLlm = document.getElementById("exportBlockLlm");
  const openManualBtn = document.getElementById("openManualBtn");
  const onlyEmpty = document.getElementById("onlyEmpty");
  const resume = document.getElementById("resume");
  const progressFill = document.getElementById("progressFill");
  const progressText = document.getElementById("progressText");
  const batchStatus = document.getElementById("batchStatus");
  const log = document.getElementById("log");
  const statRu = document.getElementById("statRu");
  const statKz = document.getElementById("statKz");
  const statMixed = document.getElementById("statMixed");
  const statEta = document.getElementById("statEta");
  const headerBadges = document.getElementById("headerBadges");

  let jobId = null;
  let eventSource = null;
  let exportMode = "full";
  let exportCounts = null;

  function switchTab(name) {
    document.querySelectorAll(".tab").forEach((t) => {
      t.classList.toggle("active", t.dataset.tab === name);
    });
    document.querySelectorAll(".tab-panel").forEach((p) => {
      p.classList.toggle("hidden", p.id !== `tab-${name}`);
    });
  }

  document.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", () => switchTab(tab.dataset.tab));
  });
  document.querySelectorAll("[data-goto]").forEach((btn) => {
    btn.addEventListener("click", () => switchTab(btn.dataset.goto));
  });

  function getExportMode() {
    const sel = document.querySelector(".export-mode");
    return sel?.value || exportMode;
  }

  function setExportMode(mode) {
    exportMode = mode;
    document.querySelectorAll(".export-mode").forEach((sel) => {
      sel.value = mode;
    });
    updateExportHints();
  }

  function formatExportHint(counts, mode) {
    if (!counts) return "—";
    const total = counts.total.toLocaleString();
    const labeled = counts.labeled.toLocaleString();
    const manual = counts.manual.toLocaleString();
    if (mode === "full") {
      return `Will download all ${total} rows (labeled + unlabeled).`;
    }
    if (mode === "labeled") {
      return `Will download ${labeled} language-labeled rows (of ${total} total).`;
    }
    if (mode === "manual") {
      return `Will download ${manual} language manual gold rows (of ${total} total).`;
    }
    if (mode === "tone_labeled") {
      const n = (counts.tone_labeled ?? 0).toLocaleString();
      return `Will download ${n} rows with positive/negative tone (of ${total} total).`;
    }
    if (mode === "tone_manual") {
      const n = (counts.tone_manual ?? 0).toLocaleString();
      return `Will download ${n} manual tone gold rows (of ${total} total).`;
    }
    return `Will download ${manual} manual gold rows (of ${total} total).`;
  }

  function updateExportHints() {
    const mode = getExportMode();
    const text = formatExportHint(exportCounts, mode);
    document.querySelectorAll(".export-hint").forEach((el) => {
      el.textContent = text;
    });
  }

  async function refreshExportInfo() {
    if (!jobId) return;
    try {
      const res = await fetch(`/api/jobs/${jobId}/export/info`);
      if (!res.ok) return;
      const data = await res.json();
      exportCounts = data.counts;
      if (data.default_mode === "labeled" && exportCounts.labeled > 0 && exportCounts.labeled < exportCounts.total) {
        setExportMode("labeled");
      } else {
        updateExportHints();
      }
    } catch {
      /* ignore */
    }
  }

  function downloadCsv() {
    if (!jobId) return;
    const mode = getExportMode();
    window.location.href = `/api/jobs/${jobId}/download?mode=${encodeURIComponent(mode)}`;
  }

  document.querySelectorAll(".download-btn").forEach((btn) => {
    btn.addEventListener("click", downloadCsv);
  });
  document.querySelectorAll(".export-mode").forEach((sel) => {
    sel.addEventListener("change", () => setExportMode(sel.value));
  });

  openManualBtn?.addEventListener("click", () => {
    switchTab("manual");
    if (jobId && window.ManualLabeler) window.ManualLabeler.start(jobId);
  });

  async function loadProviderBadges() {
    try {
      const res = await fetch("/api/health");
      const info = await res.json();
      headerBadges.innerHTML = `
        <span class="badge ${info.configured ? "ok" : "warn"}">${info.provider || "—"}</span>
        <span class="badge muted">${info.model || ""}</span>
        <span class="badge muted">${info.quality || ""}</span>`;
    } catch {
      headerBadges.innerHTML = `<span class="badge warn">offline</span>`;
    }
  }

  function appendLog(text, cls = "") {
    const line = document.createElement("div");
    line.className = `line ${cls}`.trim();
    line.textContent = text;
    log.appendChild(line);
    log.scrollTop = log.scrollHeight;
  }

  function clearLog() {
    log.innerHTML = "";
  }

  function updateStats(stats) {
    if (!stats) return;
    statRu.textContent = stats.ru ?? 0;
    statKz.textContent = stats.kz ?? 0;
    statMixed.textContent = stats.mixed ?? 0;
  }

  function updateProgress(processed, total, percent) {
    const pct = percent ?? (total ? (100 * processed) / total : 0);
    progressFill.style.width = `${Math.min(100, pct)}%`;
    progressText.textContent = `${processed} / ${total} (${pct.toFixed ? pct.toFixed(1) : pct}%)`;
  }

  function showExportBlocks() {
    exportBlockUpload?.classList.remove("hidden");
    exportBlockLlm?.classList.remove("hidden");
  }

  async function uploadFile(file) {
    if (!file.name.toLowerCase().endsWith(".csv")) {
      alert("Please upload a CSV file.");
      return;
    }

    const form = new FormData();
    form.append("file", file);

    startBtn.disabled = true;
    exportBlockUpload?.classList.add("hidden");
    exportBlockLlm?.classList.add("hidden");
    openManualBtn?.classList.add("hidden");
    batchStatus.textContent = "Uploading…";

    try {
      const res = await fetch("/api/upload", { method: "POST", body: form });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Upload failed");

      jobId = data.job_id;
      fileInfo.classList.remove("hidden");
      const ls = data.language_stats || {};
      fileInfo.innerHTML = `
        <strong>${file.name}</strong><br>
        ${data.total_rows.toLocaleString()} rows · empty language: ${data.empty_language.toLocaleString()}
        · filled (LLM hint): ${(data.filled_language ?? 0).toLocaleString()}
        ${data.filled_language ? `<br>LLM labels saved as hint: ru=${ls.ru || 0}, kz=${ls.kz || 0}, mixed=${ls.mixed || 0}` : ""}
        ${data.warn_large ? "<br><span style='color:var(--warn)'>Large file — manual labeling recommended.</span>" : ""}
      `;

      preview.classList.remove("hidden");
      previewTable.innerHTML = "";
      (data.preview || []).forEach((row) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `<td>${escapeHtml(row.text)}</td><td>${escapeHtml(row.language)}</td><td>${escapeHtml(row.label)}</td>`;
        previewTable.appendChild(tr);
      });

      startBtn.disabled = false;
      batchStatus.textContent = "Ready — use Manual review tab for gold labels.";
      appendLog(`Uploaded job ${jobId}: ${data.total_rows} rows`, "batch");
      showExportBlocks();
      openManualBtn?.classList.remove("hidden");
      await refreshExportInfo();

      switchTab("manual");
      if (window.ManualLabeler) await window.ManualLabeler.start(jobId);
    } catch (err) {
      batchStatus.textContent = "Upload error.";
      appendLog(`Error: ${err.message}`, "error");
    }
  }

  function escapeHtml(s) {
    const d = document.createElement("div");
    d.textContent = s ?? "";
    return d.innerHTML;
  }

  function startLabeling() {
    if (!jobId) return;
    if (eventSource) eventSource.close();

    clearLog();
    startBtn.disabled = true;

    const params = new URLSearchParams({
      only_empty: onlyEmpty.checked ? "true" : "false",
      resume: resume.checked ? "true" : "false",
    });

    eventSource = new EventSource(`/api/jobs/${jobId}/label?${params}`);
    appendLog("Connecting to labeling stream…", "batch");

    eventSource.addEventListener("batch_start", (e) => {
      const d = JSON.parse(e.data);
      batchStatus.textContent = `Batch ${d.batch} / ${d.total_batches} (${d.rows.length} rows)`;
      appendLog(`▶ Batch ${d.batch}/${d.total_batches} — rows ${d.rows.join(", ")}`, "batch");
    });

    eventSource.addEventListener("llm_chunk", (e) => {
      const d = JSON.parse(e.data);
      appendLog(d.text, "chunk");
    });

    eventSource.addEventListener("batch_done", (e) => {
      const d = JSON.parse(e.data);
      appendLog(`✓ Batch ${d.batch} done (${d.labels_count} labels)`, "batch");
    });

    eventSource.addEventListener("row_labeled", (e) => {
      const d = JSON.parse(e.data);
      appendLog(`  row ${d.row_id} → ${d.language} (conf=${d.confidence})`, "row");
    });

    eventSource.addEventListener("progress", (e) => {
      const d = JSON.parse(e.data);
      updateProgress(d.processed, d.total, d.percent);
      updateStats(d.stats);
      if (d.eta_seconds != null) {
        const m = Math.floor(d.eta_seconds / 60);
        const s = Math.round(d.eta_seconds % 60);
        statEta.textContent = m > 0 ? `${m}m ${s}s` : `${s}s`;
      }
    });

    eventSource.addEventListener("done", (e) => {
      const d = JSON.parse(e.data);
      batchStatus.textContent = d.message || `Done — ${d.processed} rows labeled.`;
      appendLog(`Finished. Stats: ru=${d.stats.ru}, kz=${d.stats.kz}, mixed=${d.stats.mixed}`, "done");
      if (d.message) appendLog(d.message, "batch");
      eventSource.close();
      eventSource = null;
      startBtn.disabled = false;
      showExportBlocks();
      refreshExportInfo();
      if (window.ManualLabeler) window.ManualLabeler.refreshMetrics?.();
    });

    eventSource.addEventListener("label_error", (e) => {
      const d = JSON.parse(e.data);
      appendLog(`Error: ${d.message}`, "error");
      batchStatus.textContent = d.message;
      eventSource.close();
      eventSource = null;
      startBtn.disabled = false;
    });

    eventSource.onerror = () => {
      if (eventSource?.readyState === EventSource.CLOSED) {
        appendLog("Connection closed.", "error");
        startBtn.disabled = false;
      }
    };
  }

  browseBtn.addEventListener("click", () => fileInput.click());
  dropzone.addEventListener("click", (e) => {
    if (e.target !== browseBtn) fileInput.click();
  });
  fileInput.addEventListener("change", () => {
    if (fileInput.files[0]) uploadFile(fileInput.files[0]);
  });

  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  });
  dropzone.addEventListener("dragleave", () => dropzone.classList.remove("dragover"));
  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
    const file = e.dataTransfer.files[0];
    if (file) uploadFile(file);
  });

  startBtn.addEventListener("click", startLabeling);
  loadProviderBadges();

  window.LabelerExport = {
    refreshExportInfo,
    updateExportHints,
  };
})();
