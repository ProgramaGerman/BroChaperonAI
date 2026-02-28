// ============================================================
// app.js — Controlador principal de la aplicación
// ============================================================
// Responsabilidades:
//   - Inicialización del DOM y escucha de eventos
//   - Coordinación entre el servicio de tareas y la UI
//   - Manejo del filtrado y búsqueda
//   - Apertura de modales de crear/editar/confirmar eliminación
// ============================================================

import {
  createTask,
  deleteTask,
  fetchAllTasks,
  updateTask,
} from './services/tasks.js';

import {
  clearModal,
  renderEmptyState,
  renderError,
  renderSkeleton,
  renderTaskCard,
  showModal,
  showToast,
} from './ui/components.js';

// ----------------------------------------------------------
// Estado de la aplicación
// ----------------------------------------------------------
const state = {
  filter:  'all',    // 'all' | 'completed' | 'pending'
  search:  '',
  tasks:   [],
};

// ----------------------------------------------------------
// Referencias al DOM
// ----------------------------------------------------------
const DOM = {
  get btnNew()         { return document.getElementById('btn-new-task'); },
  get filterBtns()     { return document.querySelectorAll('[data-filter]'); },
  get searchInput()    { return document.getElementById('search-input'); },
  get statsCompleted() { return document.getElementById('stat-completed'); },
  get statsPending()   { return document.getElementById('stat-pending'); },
  get statsTotal()     { return document.getElementById('stat-total'); },
  get tasksGrid()      { return document.getElementById('tasks-grid'); },
};

// ----------------------------------------------------------
// Arranque
// ----------------------------------------------------------
document.addEventListener('DOMContentLoaded', init);

async function init() {
  attachGlobalListeners();
  await loadTasks();
}

// ----------------------------------------------------------
// Carga y renderizado de tareas
// ----------------------------------------------------------

async function loadTasks() {
  DOM.tasksGrid.innerHTML = renderSkeleton();

  try {
    state.tasks = await fetchAllTasks();
    renderTasks();
    updateStats();
  } catch (error) {
    console.error('[app] Error al cargar tareas:', error);
    DOM.tasksGrid.innerHTML = renderError(error.message);
    showToast('No se pudieron cargar las tareas.', 'error');
  }
}

function renderTasks() {
  const filtered = applyFilters(state.tasks);

  if (filtered.length === 0) {
    DOM.tasksGrid.innerHTML = renderEmptyState();
    return;
  }

  DOM.tasksGrid.innerHTML = filtered.map((task) =>
    renderTaskCard(task)
  ).join('');
}

// ----------------------------------------------------------
// Filtros y búsqueda
// ----------------------------------------------------------

function applyFilters(tasks) {
  return tasks.filter((task) => {
    const matchesFilter = (
      state.filter === 'all'       ||
      (state.filter === 'completed' && task.completed)  ||
      (state.filter === 'pending'   && !task.completed)
    );

    const query = state.search.toLowerCase();
    const matchesSearch = (
      !query ||
      task.title.toLowerCase().includes(query) ||
      task.description?.toLowerCase().includes(query)
    );

    return matchesFilter && matchesSearch;
  });
}

// ----------------------------------------------------------
// Estadísticas
// ----------------------------------------------------------

function updateStats() {
  const total     = state.tasks.length;
  const completed = state.tasks.filter((t) => t.completed).length;
  const pending   = total - completed;

  DOM.statsTotal.textContent     = total;
  DOM.statsCompleted.textContent = completed;
  DOM.statsPending.textContent   = pending;
}

// ----------------------------------------------------------
// Escucha de eventos globales
// ----------------------------------------------------------

function attachGlobalListeners() {
  // Botón de nueva tarea
  DOM.btnNew.addEventListener('click', openCreateModal);

  // Filtros de estado
  DOM.filterBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      state.filter = btn.dataset.filter;
      DOM.filterBtns.forEach((b) => b.classList.remove('filter-btn--active'));
      btn.classList.add('filter-btn--active');
      renderTasks();
    });
  });

  // Búsqueda con debounce
  DOM.searchInput.addEventListener('input', debounce((e) => {
    state.search = e.target.value.trim();
    renderTasks();
  }, 250));

  // Delegación de eventos en la cuadrícula de tareas
  DOM.tasksGrid.addEventListener('click', handleGridClick);
}

function handleGridClick(event) {
  const btn = event.target.closest('[data-action]');
  if (!btn) return;

  const id     = Number(btn.dataset.id);
  const action = btn.dataset.action;

  switch (action) {
    case 'complete': handleComplete(id);   break;
    case 'delete':   handleDelete(id);     break;
    case 'edit':     handleEdit(id);       break;
    default:         break;
  }
}

// ----------------------------------------------------------
// Acciones sobre tareas
// ----------------------------------------------------------

async function handleComplete(id) {
  const task = state.tasks.find((t) => t.id === id);
  if (!task) return;

  try {
    const updated = await updateTask(id, { completed: !task.completed });
    mergeTask(updated);
    renderTasks();
    updateStats();
    showToast(
      updated.completed ? 'Tarea marcada como completada.' : 'Tarea marcada como pendiente.',
      'success'
    );
  } catch (error) {
    console.error('[app] Error al actualizar tarea:', error);
    showToast('No se pudo actualizar la tarea.', 'error');
  }
}

async function handleDelete(id) {
  showModal({
    body: /* html */`
      <p class="modal__confirm-text">
        ¿Estás seguro de que deseas eliminar esta tarea?
        Esta acción <strong>no se puede deshacer</strong>.
      </p>
      <div class="modal__actions">
        <button class="btn btn--secondary" id="modal-cancel-btn" type="button">
          Cancelar
        </button>
        <button class="btn btn--danger" id="modal-confirm-btn" type="button">
          Sí, eliminar
        </button>
      </div>
    `,
    onConfirm: async () => {
      try {
        await deleteTask(id);
        state.tasks = state.tasks.filter((t) => t.id !== id);
        renderTasks();
        updateStats();
        showToast('Tarea eliminada correctamente.', 'success');
      } catch (error) {
        console.error('[app] Error al eliminar tarea:', error);
        showToast('No se pudo eliminar la tarea.', 'error');
      }
    },
    title: 'Confirmar eliminación',
  });

  document.getElementById('modal-cancel-btn')
    ?.addEventListener('click', clearModal);
}

function handleEdit(id) {
  const task = state.tasks.find((t) => t.id === id);
  if (!task) return;
  openEditModal(task);
}

// ----------------------------------------------------------
// Modales de formulario
// ----------------------------------------------------------

function buildTaskForm(task = null) {
  const isEdit = task !== null;

  return /* html */`
    <form class="task-form" id="task-form" novalidate>

      <div class="form-group">
        <label class="form-label" for="form-title">
          Título <span class="form-required">*</span>
        </label>
        <input
          autocomplete="off"
          class="form-input"
          id="form-title"
          maxlength="120"
          placeholder="Ej. Completar informe mensual"
          required
          type="text"
          value="${isEdit ? task.title : ''}"
        />
        <span class="form-error" id="form-title-error" role="alert"></span>
      </div>

      <div class="form-group">
        <label class="form-label" for="form-description">Descripción</label>
        <textarea
          class="form-input form-textarea"
          id="form-description"
          maxlength="500"
          placeholder="Detalle opcional de la tarea..."
          rows="3"
        >${isEdit ? task.description : ''}</textarea>
      </div>

      <div class="form-group">
        <label class="form-label" for="form-priority">Prioridad</label>
        <select class="form-input form-select" id="form-priority">
          <option value="alta"  ${isEdit && task.priority === 'alta'  ? 'selected' : ''}>🔴 Alta</option>
          <option value="media" ${!isEdit || task.priority === 'media' ? 'selected' : ''}>🟡 Media</option>
          <option value="baja"  ${isEdit && task.priority === 'baja'  ? 'selected' : ''}>🟢 Baja</option>
        </select>
      </div>

      <div class="modal__actions">
        <button class="btn btn--secondary" id="modal-cancel-btn" type="button">
          Cancelar
        </button>
        <button class="btn btn--primary" id="form-submit-btn" type="submit">
          ${isEdit ? 'Guardar cambios' : 'Crear tarea'}
        </button>
      </div>

    </form>
  `;
}

function openCreateModal() {
  showModal({
    body:  buildTaskForm(),
    title: '✨ Nueva Tarea',
  });

  document.getElementById('modal-cancel-btn')
    ?.addEventListener('click', clearModal);

  document.getElementById('task-form')
    .addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = readFormValues();
      if (!validateForm(data)) return;

      const submitBtn = document.getElementById('form-submit-btn');
      submitBtn.disabled = true;
      submitBtn.textContent = 'Guardando…';

      try {
        const created = await createTask(data);
        state.tasks.unshift(created);
        clearModal();
        renderTasks();
        updateStats();
        showToast('¡Tarea creada exitosamente!', 'success');
      } catch (error) {
        console.error('[app] Error al crear tarea:', error);
        showToast('No se pudo crear la tarea.', 'error');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Crear tarea';
      }
    });
}

function openEditModal(task) {
  showModal({
    body:  buildTaskForm(task),
    title: '✏️ Editar Tarea',
  });

  document.getElementById('modal-cancel-btn')
    ?.addEventListener('click', clearModal);

  document.getElementById('task-form')
    .addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = readFormValues();
      if (!validateForm(data)) return;

      const submitBtn = document.getElementById('form-submit-btn');
      submitBtn.disabled = true;
      submitBtn.textContent = 'Guardando…';

      try {
        const updated = await updateTask(task.id, data);
        mergeTask(updated);
        clearModal();
        renderTasks();
        updateStats();
        showToast('Tarea actualizada correctamente.', 'success');
      } catch (error) {
        console.error('[app] Error al editar tarea:', error);
        showToast('No se pudo actualizar la tarea.', 'error');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Guardar cambios';
      }
    });
}

// ----------------------------------------------------------
// Helpers de formulario
// ----------------------------------------------------------

function readFormValues() {
  return {
    description: document.getElementById('form-description').value.trim(),
    priority:    document.getElementById('form-priority').value,
    title:       document.getElementById('form-title').value.trim(),
  };
}

function validateForm({ title }) {
  const errorEl = document.getElementById('form-title-error');
  errorEl.textContent = '';

  if (!title) {
    errorEl.textContent = 'El título es obligatorio.';
    document.getElementById('form-title').focus();
    return false;
  }
  return true;
}

// ----------------------------------------------------------
// Helpers de estado
// ----------------------------------------------------------

/** Reemplaza una tarea en el array de estado local. */
function mergeTask(updated) {
  const idx = state.tasks.findIndex((t) => t.id === updated.id);
  if (idx !== -1) state.tasks[idx] = updated;
}

// ----------------------------------------------------------
// Utilidades generales
// ----------------------------------------------------------

/**
 * Crea una versión debounced de la función recibida.
 * @param {Function} fn
 * @param {number}   delay - milisegundos
 */
function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}
