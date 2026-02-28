// ============================================================
// tasks.js — Servicio CRUD para la tabla "tasks" en Supabase
// ============================================================
// Métodos exportados (orden alfabético):
//   - createTask(data)        → Inserta una nueva tarea
//   - deleteTask(id)          → Elimina una tarea por ID
//   - fetchAllTasks()         → Obtiene todas las tareas ordenadas
//   - updateTask(id, changes) → Actualiza campos de una tarea
// ============================================================

import { SUPABASE_ANON_KEY, SUPABASE_URL } from '../config.js';

// ----------------------------------------------------------
// Constantes internas
// ----------------------------------------------------------
const HEADERS = {
  'apikey':         SUPABASE_ANON_KEY,
  'Authorization':  `Bearer ${SUPABASE_ANON_KEY}`,
  'Content-Type':   'application/json',
  'Prefer':         'return=representation',
};

const TABLE_URL = `${SUPABASE_URL}/rest/v1/tasks`;

// ----------------------------------------------------------
// Helpers privados
// ----------------------------------------------------------

/**
 * Lanza un Error descriptivo si la respuesta HTTP no es exitosa.
 * @param {Response} response
 */
async function assertOk(response) {
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.message || `HTTP ${response.status}`);
  }
}

// ----------------------------------------------------------
// Métodos públicos
// ----------------------------------------------------------

/**
 * Inserta una nueva tarea en la base de datos.
 * @param {{ description: string, priority: string, title: string }} data
 * @returns {Promise<Object>} Tarea creada
 */
async function createTask(data) {
  const payload = {
    completed:   false,
    created_at:  new Date().toISOString(),
    description: data.description ?? '',
    priority:    data.priority    ?? 'media',
    title:       data.title,
  };

  const response = await fetch(TABLE_URL, {
    body:    JSON.stringify(payload),
    headers: HEADERS,
    method:  'POST',
  });

  await assertOk(response);
  const [task] = await response.json();
  return task;
}

/**
 * Elimina una tarea por su ID.
 * @param {number} id
 * @returns {Promise<void>}
 */
async function deleteTask(id) {
  const response = await fetch(`${TABLE_URL}?id=eq.${id}`, {
    headers: HEADERS,
    method:  'DELETE',
  });

  await assertOk(response);
}

/**
 * Obtiene todas las tareas ordenadas por fecha de creación descendente.
 * @returns {Promise<Array>} Lista de tareas
 */
async function fetchAllTasks() {
  const url      = `${TABLE_URL}?order=created_at.desc&select=*`;
  const response = await fetch(url, {
    headers: { ...HEADERS, 'Prefer': 'count=exact' },
    method:  'GET',
  });

  await assertOk(response);
  return response.json();
}

/**
 * Actualiza campos específicos de una tarea existente.
 * @param {number}  id      - ID de la tarea
 * @param {Object}  changes - Campos a actualizar
 * @returns {Promise<Object>} Tarea actualizada
 */
async function updateTask(id, changes) {
  const payload = {
    ...changes,
    updated_at: new Date().toISOString(),
  };

  const response = await fetch(`${TABLE_URL}?id=eq.${id}`, {
    body:    JSON.stringify(payload),
    headers: HEADERS,
    method:  'PATCH',
  });

  await assertOk(response);
  const [task] = await response.json();
  return task;
}

// ----------------------------------------------------------
// Exportaciones
// ----------------------------------------------------------
export {
  createTask,
  deleteTask,
  fetchAllTasks,
  updateTask,
};
