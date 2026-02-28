// ============================================================
// components.js — Funciones de renderizado de componentes UI
// ============================================================
// Funciones exportadas (orden alfabético):
//   - clearModal()
//   - renderEmptyState()
//   - renderError(message)
//   - renderSkeleton()
//   - renderTaskCard(task, handlers)
//   - showModal(options)
//   - showToast(message, type)
// ============================================================

// ----------------------------------------------------------
// clearModal — Limpia y oculta el modal activo
// ----------------------------------------------------------
function clearModal() {
  const modal   = document.getElementById('modal-overlay');
  const content = document.getElementById('modal-content');

  if (!modal) return;

  modal.classList.remove('modal--visible');
  setTimeout(() => { content.innerHTML = ''; }, 300);
}

// ----------------------------------------------------------
// renderEmptyState — Mensaje cuando no hay tareas
// ----------------------------------------------------------
function renderEmptyState() {
  return /* html */`
    <div class="empty-state" id="empty-state">
      <div class="empty-state__icon">📋</div>
      <h2 class="empty-state__title">Sin tareas aún</h2>
      <p class="empty-state__subtitle">
        Crea tu primera tarea usando el botón <strong>+ Nueva Tarea</strong>.
      </p>
    </div>
  `;
}

// ----------------------------------------------------------
// renderError — Muestra un error en el contenedor principal
// ----------------------------------------------------------
function renderError(message) {
  return /* html */`
    <div class="error-state" id="error-state">
      <div class="error-state__icon">⚠️</div>
      <h2 class="error-state__title">Ocurrió un error</h2>
      <p class="error-state__message">${message}</p>
    </div>
  `;
}

// ----------------------------------------------------------
// renderSkeleton — Skeletons de carga (×3)
// ----------------------------------------------------------
function renderSkeleton() {
  const skeleton = /* html */`
    <div class="skeleton-card">
      <div class="skeleton skeleton--title"></div>
      <div class="skeleton skeleton--line"></div>
      <div class="skeleton skeleton--line skeleton--line-short"></div>
      <div class="skeleton skeleton--footer"></div>
    </div>
  `;
  return skeleton.repeat(3);
}

// ----------------------------------------------------------
// renderTaskCard — Tarjeta individual de tarea
// ----------------------------------------------------------
/**
 * @param {Object} task     - Datos de la tarea desde Supabase
 * @param {Object} handlers - { onComplete, onDelete, onEdit }
 * @returns {string} HTML de la tarjeta
 */
function renderTaskCard(task, handlers) {
  const {
    completed,
    created_at,
    description,
    id,
    priority,
    title,
  } = task;

  const date          = new Date(created_at).toLocaleDateString('es-ES', {
    day:   'numeric',
    month: 'short',
    year:  'numeric',
  });
  const priorityLabel = { alta: '🔴 Alta', baja: '🟢 Baja', media: '🟡 Media' };
  const statusClass   = completed ? 'task-card--completed' : '';
  const statusIcon    = completed ? '✅' : '⏳';

  return /* html */`
    <article
      class="task-card ${statusClass}"
      data-id="${id}"
      id="task-${id}"
    >
      <header class="task-card__header">
        <span class="task-card__priority badge badge--${priority}">
          ${priorityLabel[priority] ?? priority}
        </span>
        <span class="task-card__status">${statusIcon}</span>
      </header>

      <h3 class="task-card__title">${escapeHtml(title)}</h3>

      ${description
        ? `<p class="task-card__description">${escapeHtml(description)}</p>`
        : ''}

      <footer class="task-card__footer">
        <time class="task-card__date" datetime="${created_at}">${date}</time>

        <div class="task-card__actions">
          <button
            aria-label="Marcar como ${completed ? 'pendiente' : 'completada'}"
            class="btn btn--icon btn--success"
            data-action="complete"
            data-id="${id}"
            title="${completed ? 'Marcar pendiente' : 'Marcar como hecha'}"
            type="button"
          >
            ${completed ? '↩' : '✓'}
          </button>

          <button
            aria-label="Editar tarea"
            class="btn btn--icon btn--warning"
            data-action="edit"
            data-id="${id}"
            title="Editar"
            type="button"
          >
            ✏️
          </button>

          <button
            aria-label="Eliminar tarea"
            class="btn btn--icon btn--danger"
            data-action="delete"
            data-id="${id}"
            title="Eliminar"
            type="button"
          >
            🗑
          </button>
        </div>
      </footer>
    </article>
  `;
}

// ----------------------------------------------------------
// showModal — Despliega el modal con contenido dinámico
// ----------------------------------------------------------
/**
 * @param {{ body: string, onConfirm?: Function, title: string }} options
 */
function showModal({ body, onConfirm, title }) {
  const modal   = document.getElementById('modal-overlay');
  const content = document.getElementById('modal-content');

  content.innerHTML = /* html */`
    <div class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <header class="modal__header">
        <h2 class="modal__title" id="modal-title">${title}</h2>
        <button
          class="modal__close btn btn--icon"
          id="modal-close-btn"
          type="button"
          aria-label="Cerrar"
        >✕</button>
      </header>
      <div class="modal__body">${body}</div>
    </div>
  `;

  modal.classList.add('modal--visible');

  document.getElementById('modal-close-btn')
    .addEventListener('click', clearModal);

  modal.addEventListener('click', (e) => {
    if (e.target === modal) clearModal();
  }, { once: true });

  if (typeof onConfirm === 'function') {
    const confirmBtn = document.getElementById('modal-confirm-btn');
    confirmBtn?.addEventListener('click', () => {
      onConfirm();
      clearModal();
    });
  }
}

// ----------------------------------------------------------
// showToast — Notificación ephemeral (tipo snackbar)
// ----------------------------------------------------------
/**
 * @param {string} message
 * @param {'error' | 'info' | 'success' | 'warning'} type
 */
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast--${type}`;
  toast.setAttribute('role', 'status');
  toast.innerHTML = /* html */`
    <span class="toast__icon">${toastIcon(type)}</span>
    <span class="toast__message">${message}</span>
  `;

  container.appendChild(toast);

  // Animación de entrada
  requestAnimationFrame(() => toast.classList.add('toast--visible'));

  // Animación de salida y limpieza
  setTimeout(() => {
    toast.classList.remove('toast--visible');
    toast.addEventListener('transitionend', () => toast.remove(), { once: true });
  }, 3500);
}

// ----------------------------------------------------------
// Helpers privados
// ----------------------------------------------------------

/** Escapa caracteres HTML para prevenir XSS. */
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

/** Ícono según el tipo de toast. */
function toastIcon(type) {
  const icons = { error: '❌', info: 'ℹ️', success: '✅', warning: '⚠️' };
  return icons[type] ?? 'ℹ️';
}

// ----------------------------------------------------------
// Exportaciones
// ----------------------------------------------------------
export {
  clearModal,
  renderEmptyState,
  renderError,
  renderSkeleton,
  renderTaskCard,
  showModal,
  showToast,
};
