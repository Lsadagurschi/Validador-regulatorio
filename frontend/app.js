const API_BASE = window.location.origin.replace(/\/$/, "");

const elements = {
  organizationForm: document.querySelector("#organization-form"),
  organizationFeedback: document.querySelector("#org-feedback"),
  organizationsTable: document.querySelector("#organizations-table"),
  refreshOrganizations: document.querySelector("#refresh-organizations"),
  validationForm: document.querySelector("#validation-form"),
  validationFeedback: document.querySelector("#validation-feedback"),
  validationResult: document.querySelector("#validation-result"),
  validationSummary: document.querySelector("#validation-summary"),
  validationIssues: document.querySelector("#validation-issues"),
  validationOrg: document.querySelector("#validation-org"),
  validationRegulator: document.querySelector("#validation-regulator"),
  validatorsContainer: document.querySelector("#validators-container"),
  refreshValidators: document.querySelector("#refresh-validators"),
};

async function request(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    const message = detail.detail || response.statusText;
    throw new Error(message);
  }
  if (response.status === 204) {
    return null;
  }
  const contentType = response.headers.get("content-type");
  if (contentType && contentType.includes("application/json")) {
    return response.json();
  }
  return response.text();
}

function setFeedback(target, message, type = "") {
  target.textContent = message;
  target.classList.remove("error", "success");
  if (type) {
    target.classList.add(type);
  }
}

function renderOrganizations(organizations) {
  elements.organizationsTable.innerHTML = "";
  elements.validationOrg.innerHTML = "";
  if (!organizations.length) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 4;
    cell.textContent = "Nenhuma organização cadastrada.";
    row.append(cell);
    elements.organizationsTable.append(row);
    const placeholder = document.createElement("option");
    placeholder.disabled = true;
    placeholder.selected = true;
    placeholder.textContent = "Cadastre uma instituição";
    elements.validationOrg.append(placeholder);
    return;
  }

  for (const org of organizations) {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${org.id}</td>
      <td>${org.name}</td>
      <td>${org.role}</td>
      <td>${org.tax_id}</td>
    `;
    elements.organizationsTable.append(row);

    const option = document.createElement("option");
    option.value = org.id;
    option.textContent = `${org.name} (#${org.id})`;
    elements.validationOrg.append(option);
  }
}

function renderValidators(validators) {
  elements.validatorsContainer.innerHTML = "";
  elements.validationRegulator.innerHTML = "";

  if (!validators.length) {
    elements.validatorsContainer.textContent = "Nenhum validador registrado.";
    return;
  }

  for (const validator of validators) {
    const card = document.createElement("article");
    card.className = "validator-card";
    const fieldItems = validator.layout.fields
      .map(
        (field) =>
          `<li><strong>${field.name}</strong> — ${field.type} ${
            field.required ? "(obrigatório)" : "(opcional)"
          }${field.max_length ? ` · máx ${field.max_length} caracteres` : ""}</li>`
      )
      .join("");
    card.innerHTML = `
      <h3>${validator.layout.name} · versão ${validator.layout.version}</h3>
      <p><strong>Regulador:</strong> ${validator.regulator}</p>
      <p><strong>Chave para API:</strong> <code>${validator.key}</code></p>
      <ul class="validator-fields">${fieldItems}</ul>
    `;
    elements.validatorsContainer.append(card);

    const option = document.createElement("option");
    option.value = validator.key;
    option.textContent = `${validator.regulator} · ${validator.layout.name}`;
    elements.validationRegulator.append(option);
  }
}

async function loadOrganizations() {
  try {
    const organizations = await request(`${API_BASE}/organizations`);
    renderOrganizations(organizations);
    setFeedback(elements.organizationFeedback, "", "");
  } catch (error) {
    renderOrganizations([]);
    setFeedback(elements.organizationFeedback, error.message, "error");
  }
}

async function loadValidators() {
  try {
    const validators = await request(`${API_BASE}/validators`);
    renderValidators(validators);
    setFeedback(elements.validationFeedback, "", "");
  } catch (error) {
    elements.validatorsContainer.textContent = "Erro ao carregar validadores.";
    setFeedback(elements.validationFeedback, error.message, "error");
  }
}

elements.organizationForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(elements.organizationForm);
  const payload = Object.fromEntries(formData.entries());
  setFeedback(elements.organizationFeedback, "Enviando…");
  try {
    const created = await request(`${API_BASE}/organizations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    setFeedback(
      elements.organizationFeedback,
      `Instituição "${created.name}" registrada com sucesso!`,
      "success"
    );
    elements.organizationForm.reset();
    await loadOrganizations();
  } catch (error) {
    setFeedback(elements.organizationFeedback, error.message, "error");
  }
});

elements.refreshOrganizations.addEventListener("click", loadOrganizations);

elements.refreshValidators.addEventListener("click", loadValidators);

elements.validationForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(elements.validationForm);
  if (!formData.get("file")) {
    setFeedback(elements.validationFeedback, "Selecione um arquivo.", "error");
    return;
  }
  setFeedback(elements.validationFeedback, "Validando arquivo…");
  elements.validationResult.hidden = true;
  elements.validationIssues.innerHTML = "";

  try {
    const response = await request(`${API_BASE}/validations`, {
      method: "POST",
      body: formData,
    });
    const { validation, issues } = response;
    elements.validationResult.hidden = false;
    elements.validationSummary.textContent = validation.summary || "Sem resumo.";
    if (!issues.length) {
      elements.validationIssues.innerHTML = `<tr><td colspan="4">Sem inconsistências detectadas.</td></tr>`;
    } else {
      for (const issue of issues) {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${issue.line_number ?? "-"}</td>
          <td>${issue.column_name ?? "-"}</td>
          <td>${issue.severity}</td>
          <td>${issue.message}</td>
        `;
        elements.validationIssues.append(row);
      }
    }
    setFeedback(elements.validationFeedback, "Validação concluída.", "success");
  } catch (error) {
    setFeedback(elements.validationFeedback, error.message, "error");
  }
});

(async function bootstrap() {
  await Promise.all([loadOrganizations(), loadValidators()]);
})();
